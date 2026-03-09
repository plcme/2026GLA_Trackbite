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

from google import genai
from google.genai import types

# 初始化 Client 并指定使用 Vertex AI
client = genai.Client(
    vertexai=True, 
    project='project-e7712b89-68ab-42ce-ba8', 
    location='us-central1' # 或者其他支持的 Region
)

# 发送请求
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="请解释什么是量子纠缠？"
)

# for model in client.models.list():
#     print(model.name)

print(response.text)