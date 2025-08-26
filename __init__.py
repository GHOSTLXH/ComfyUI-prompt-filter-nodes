"""
This file makes the nodes in this directory available to ComfyUI.
"""

# 从 prompt_filter_from_file.py 文件中导入节点映射
from .prompt_filter_from_file import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 这是一个好习惯，明确声明此模块对外暴露的变量
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']