# import vertexai
# from vertexai.generative_models import GenerativeModel

# # 初始化
# vertexai.init(project="project-e7712b89-68ab-42ce-ba8", location="us-central1")

# # 加载 Gemini 模型（使用 gemini-1.5-flash 作为测试模型）
# model = GenerativeModel("gemini-2.5-flash")

# # 生成测试
# try:
#     print("--- 正在发送测试请求 ---")
#     response = model.generate_content("你好，Gemini！请确认你已连接。")
#     print(f"响应内容: {response.text}")
# except Exception as e:
#     print(f"发生错误: {e}")

import google.generativeai as genai

# 设置你的 API Key
genai.configure(api_key="YOUR_API_KEY")

# 列出所有支持 generateContent 的模型
print("可用模型列表：")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"ID: {m.name} | 名称: {m.display_name}")