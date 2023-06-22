import os
import openai
from utils import en_to_ko, save_txt_file
from os import path
from apikey import OPENAI_API_KEY
from recap_generator import *
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def generate_init_quiz(recap: str) -> str:
    # recap을 통해 객관식 퀴즈 생성
    prompt = '아래 [내용]으로 한글로 된 객관식 퀴즈를 [퀴즈 형식]에 맞게 만들어. \
        틀린 보기를 만들 때 너가 이미 알고 있는 지식을 이용할 수 있어.\n \
        {객관식 보기 내용}은 명사형 종결 어미로 만들어.\n \
        [퀴즈 형식]\n \
        {퀴즈 번호}.{퀴즈 내용}\n \
        a){객관식 보기 내용}\n \
        b){객관식 보기 내용}\n \
        c){객관식 보기 내용}\n \
        d){객관식 보기 내용}\n \
        답){해당 문제의 답}' + "\n [내용] \n"

    prompt += recap
    
    # openai API 키 인증
    openai.api_key = OPENAI_API_KEY

    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "너는 교육을 위한 문제 출제자야."},
            {"role": "user", "content": prompt}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    
    return answer

if __name__ == "__main__":
    base_file_path = os.path.join(os.getcwd(),"app", "data", "시니어_디지털_범죄", "메신저 피싱.txt") 
    init_recap = generate_init_recap(base_file_path=base_file_path)
    init_quiz = generate_init_quiz(init_recap)
    print(init_quiz)