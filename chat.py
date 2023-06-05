import openai
import config,requests
import json

# 设置代理
proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
}

# 设置OpenAI API的访问密钥
openai.api_key = config.api_key
api_endpoint = "https://api.openai.com/v1/chat/completions"

# 设置header
headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
}

# 初始化会话列表
conversation = []

# 添加用户输入和ChatGPT的回复到会话
def add_user_messages(user_input, conversation):
    conversation.append({'role': 'user', 'content': user_input})

def add_assistant_messages(assistant_response, conversation):
    conversation.append({'role': 'assistant', 'content': assistant_response})

# 调用ChatGPT API
def call_chatgpt_api(conversation):
    data = {
        "model": "gpt-3.5-turbo-0301",
        "messages": conversation,
        "max_tokens": 400,
        "temperature": 0.6,
    }
    response = requests.post(api_endpoint, headers=headers, data=json.dumps(data), proxies=proxies)

    return response.json()


cov = 1
assistant_response = ""

while cov == 1:

    # 用户输入
    user_input = input("user: ")
    
    # 输入判断
    if user_input == "quit" or user_input == "q":
        cov = 0
    else:

        # 将用户输入和ChatGPT的回复添加到会话中
        add_user_messages(user_input, conversation)

        # 调用ChatGPT API
        api_response = call_chatgpt_api(conversation)

        # 将ChatGPT的回复添加到会话中
        assistant_response = api_response["choices"][0]["message"]["content"]
        add_assistant_messages(assistant_response, conversation)

        # 打印ChatGPT的回复
        print("ChatGPT: " + assistant_response)
