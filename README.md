# ComfyUI-prompt-filter-nodes
这是几个依据写有需要识别的特定内容（每个内容只占一行）的txt文件来对输入的提示词内容进行特定内容的识别，并对识别到的内容添加特殊的前缀（作为标记）并放回原有提示词内容中的节点。

These nodes identifies specific content in the input prompt (each content occupies only one line) based on txt files containing predefined content that needs to be recognized. It then adds a special prefix (as a marker) to the identified content and inserts it back into the original prompt.

节点功能与示意工作流：（nodes function and workflow examples）

（1）filter prompt by txt file node

![filter prompt by txt file node](picture/wechat_2025-08-26_212326_507.png)

这个节点内容为“1girl”的文本框内用于输入整体prompt内容（可以从其他文件内导入），file_path内输入用于筛选特定内容的txt文件所在路径（其中识别txt文件路径需要为Windows的绝对路径，且txt文件的格式需要为一个内容一行的方式编排！）。join_with_comma启用后会使用逗号分隔识别结果（如果不启用则会以空格分隔识别结果）

This node contains a text box labeled "1girl" for inputting the overall prompt content (which can be imported from other files). The "file_path" field is used to input the path to the txt file containing the specific content for filtering (the path to the recognition txt file must be an absolute Windows path, and the txt file must be formatted with one content entry per line!). Enabling "join_with_comma" will separate the recognition results with commas (if not enabled, the results will be separated by spaces).

（2）Concatenate_Strings（Multi）node

![Concatenate_Strings（Multi）node](picture/wechat_2025-08-26_212342_699.png)





























