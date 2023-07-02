import openai

from app.apikey import OPENAI_API_KEY

# def ChatGPT(prompt, engine = 'text-davinci-003'):
#     # api key 세팅
#     openai.api_key = OPENAI_API_KEY

#     # ChatGPT API 호출 및 최신 언어 모델인 text-davinci-003을 가져옴
#     completion = openai.Completion.create(
#         engine=engine
#         , prompt=prompt
#         , temperature=0.5
#         , max_tokens=1024
#         , top_p=1
#         , frequency_penalty=0
#         , presence_penalty=0)

#     return completion['choices'][0]['text']


def ChatGPT(messages, model = "gpt-3.5-turbo"):
    # api key 세팅
    openai.api_key = OPENAI_API_KEY
    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response['choices'][0]['message']['content']