# prompt_filter_from_file.py

import os

class PromptFilterByFile:
    """
    一个ComfyUI节点，可以根据指定的TXT文件内容，从输入的提示词字符串中筛选出匹配的关键词。
    (V2 - 支持自动检测多种文件编码)
    A ComfyUI node that filters keywords from an input prompt string based on a specified TXT file.
    (V2 - With multi-encoding auto-detection support)
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_text": ("STRING", {"multiline": True, "default": "1girl, solo, masterpiece, best quality, red dress, smiling, beautiful detailed eyes"}),
                "file_path": ("STRING", {"multiline": False, "default": "C:\\path\\to\\your\\keywords.txt"}),
                "join_with_comma": ("BOOLEAN", {"default": True, "label_on": "使用逗号分隔", "label_off": "使用空格分隔"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "filter_prompt"
    CATEGORY = "text/filtering"

    def filter_prompt(self, prompt_text, file_path, join_with_comma):
        # 检查文件路径是否有效
        if not file_path or not os.path.exists(file_path):
            print(f"警告 (PromptFilterByFile): 筛选文件未找到路径 '{file_path}'。将返回空字符串。")
            return ("",)

        # --- 智能读取模块开始 ---
        keywords_from_file = set()
        encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'shift_jis', 'latin-1']
        successful_encoding = None

        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    keywords_from_file = {line.strip() for line in f if line.strip()}
                successful_encoding = encoding
                print(f"提示 (PromptFilterByFile): 成功使用 '{encoding}' 编码读取文件。")
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"错误 (PromptFilterByFile): 读取文件时发生意料之外的错误: {e}")
                return ("",)

        if successful_encoding is None:
            print(f"错误 (PromptFilterByFile): 无法使用任何支持的编码格式 ({', '.join(encodings_to_try)}) 读取文件 '{file_path}'。请检查文件编码。")
            return ("",)
        # --- 智能读取模块结束 ---

        if not keywords_from_file:
            print(f"警告 (PromptFilterByFile): 文件 '{file_path}' 中没有找到任何关键词。将返回空字符串。")
            return ("",)

        input_tags = [tag.strip() for tag in prompt_text.split(',')]
        found_matches = [tag for tag in input_tags if tag in keywords_from_file]
        
        separator = "," if join_with_comma else " "
        result_string = separator.join(found_matches)
        
        print(f"提示 (PromptFilterByFile): 从文件中加载关键词数量: {len(keywords_from_file)}")
        print(f"提示 (PromptFilterByFile): 找到的匹配项: {found_matches}")
        print(f"提示 (PromptFilterByFile): 最终输出字符串: '{result_string}'")

        return (result_string,)


class ApplyMultiplePrefixesToKeywords:
    """
    一个ComfyUI节点，它接收原始文本、多组筛选出的关键词(每行一组)和对应的多个前缀(每行一个)，
    为匹配的关键词添加对应的前缀，并输出修改后的完整文本。
    A ComfyUI node that takes original text, multiple sets of filtered keywords (one per line),
    and their corresponding prefixes (one per line), adds the correct prefix to each matched keyword,
    and outputs the modified full text.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "original_text": ("STRING", {"multiline": True, "default": "hatsune miku, misaki kurehito, masterpiece, best quality, red dress"}),
                "filtered_keywords_list": ("STRING", {"multiline": True, "default": "hatsune miku\nmisaki kurehito"}),
                "prefixes": ("STRING", {"multiline": True, "default": "#\n@"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "apply_prefixes"
    CATEGORY = "text/filtering"

    def apply_prefixes(self, original_text, filtered_keywords_list, prefixes):
        keywords_lines = [line.strip() for line in filtered_keywords_list.splitlines() if line.strip()]
        prefixes_list = [line.strip() for line in prefixes.splitlines() if line.strip()]

        if not keywords_lines or not prefixes_list:
            print(f"警告 (ApplyMultiplePrefixes): 关键词列表或前缀列表为空，将返回原始文本。")
            return (original_text,)

        tag_to_prefix_map = {}
        num_pairs = min(len(keywords_lines), len(prefixes_list))
        if len(keywords_lines) != len(prefixes_list):
            print(f"警告 (ApplyMultiplePrefixes): 关键词行数({len(keywords_lines)})与前缀行数({len(prefixes_list)})不匹配。将只处理前 {num_pairs} 对。")

        for i in range(num_pairs):
            prefix = prefixes_list[i]
            tags_in_line = [tag.strip() for tag in keywords_lines[i].split(',') if tag.strip()]
            for tag in tags_in_line:
                tag_to_prefix_map[tag] = prefix

        if not tag_to_prefix_map:
            print(f"警告 (ApplyMultiplePrefixes): 未能从输入中解析出任何有效的 关键词-前缀 对。")
            return (original_text,)

        original_tags = [tag.strip() for tag in original_text.split(',')]
        modified_tags = []
        applied_tags = set()

        for tag in original_tags:
            if tag in tag_to_prefix_map:
                modified_tags.append(tag_to_prefix_map[tag] + tag)
                applied_tags.add(tag)
            else:
                modified_tags.append(tag)
        
        result_string = ", ".join(modified_tags)
        
        print(f"提示 (ApplyMultiplePrefixes): 已成功应用 {len(applied_tags)} 个关键词的前缀。")
        print(f"提示 (ApplyMultiplePrefixes): 最终输出字符串: '{result_string}'")

        return (result_string,)

# -------------------------- 新增的连接器节点 --------------------------

class StringListConcatenate:
    """
    一个通用的ComfyUI节点，用于将多个输入的字符串用指定的分隔符连接成一个单一的字符串。
    非常适合为需要多行输入的节点准备数据。
    A general-purpose ComfyUI node to concatenate multiple string inputs into a single string
    using a specified separator. Ideal for preparing data for nodes that require multi-line input.
    """
    @classmethod
    def INPUT_TYPES(s):
        # 定义一个必需的输入和多个可选的输入，让用户可以连接任意数量的源
        inputs = {
            "required": {
                # 使用转义字符 \n 表示换行符
                "separator": ("STRING", {"default": "\\n", "multiline": False}),
                "string_1": ("STRING", {"forceInput": True, "multiline": False}),
            },
            "optional": {}
        }
        # 添加多个可选的字符串输入端口
        for i in range(2, 9): # 添加 string_2 到 string_8
            inputs["optional"][f"string_{i}"] = ("STRING", {"forceInput": True, "multiline": False})
        
        return inputs

    RETURN_TYPES = ("STRING",)
    FUNCTION = "concatenate_strings"
    CATEGORY = "text/utils" # 放在一个新的 "utils" 类别下，更清晰

    def concatenate_strings(self, separator, string_1, **kwargs):
        # Python 会自动将 "\\n" 这样的字符串解释为换行符
        # 但为了稳健，我们手动处理用户可能输入的 "\n"
        separator = separator.replace('\\n', '\n').replace('\\r', '\r')

        # 将所有有效的、非空的输入字符串收集到一个列表中
        strings_to_join = []
        if string_1:
            strings_to_join.append(string_1)

        # 按顺序检查可选参数 kwargs
        for i in range(2, 9):
            key = f"string_{i}"
            if key in kwargs and kwargs[key]:
                strings_to_join.append(kwargs[key])

        # 使用指定的分隔符连接字符串
        result_string = separator.join(strings_to_join)
        
        print(f"提示 (Concatenate Strings): 连接了 {len(strings_to_join)} 个字符串。")
        print(f"提示 (Concatenate Strings): 输出结果:\n---\n{result_string}\n---")

        return (result_string,)

# ---------------------------------------------------------------------

# 注册所有节点到ComfyUI
NODE_CLASS_MAPPINGS = {
    "PromptFilterByFile": PromptFilterByFile,
    "ApplyMultiplePrefixesToKeywords": ApplyMultiplePrefixesToKeywords,
    "StringListConcatenate": StringListConcatenate, # 注册新的连接器节点
}

# 设置所有节点在菜单中显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptFilterByFile": "Filter Prompt by TXT File",
    "ApplyMultiplePrefixesToKeywords": "Apply Multiple Prefixes to Keywords",
    "StringListConcatenate": "Concatenate Strings (Multi)", # 为新节点设置显示名称
}