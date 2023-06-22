import os
import openai
from utils import en_to_ko, save_txt_file
from os import path
from models import TextResult, QuizResult
from apikey import OPENAI_API_KEY
from recap_generator import *
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    
def generate_init_quiz(recap: str) -> str:
    # recap을 통해 객관식 퀴즈 생성
    prompt = "아래 [내용]으로 객관식 퀴즈를 [퀴즈 형식]에 맞게 한글로 만들어. \n \
            틀린 보기를 만들 때 너가 이미 알고 있는 지식을 이용할 수 있어. \n \
            {퀴즈 번호}와 {답}은 int 형이야. \n \
            {객관식 보기 내용}은 명사형 종결 어미로 만들어. \n \
            퀴즈가 많다면 '\n'로 구별해줘. \
            [퀴즈 형식]\n \
            {퀴즈 번호}\t '{퀴즈 문제}'\t '['{객관식 보기 내용}', '{객관식 보기 내용}','{객관식 보기 내용}', '{객관식 보기 내용}']' \t {해당 문제의 답}" \
            + "\n [내용] \n"

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


def generate_quiz(user_request: UserRequest) -> TextResult:
    answer_result = QuizResult()
    base_file_path = os.path.join(os.getcwd(), "data", user_request.edu_class_folder_name, user_request.edu_title_file_name) 
    quizzes = {}
    try:
        init_recap = generate_init_recap(base_file_path=base_file_path)
        ko_init_quiz = format_recap(init_recap)
        init_quiz = generate_init_quiz(ko_init_quiz)

        init_quiz_list = init_quiz.split('\n')
        print(init_quiz_list)
        for quiz in init_quiz_list:
           # parsing
           contents = quiz.split('\t')
           # string to other type
           quizzes[int(contents[0])] = {'question' : eval(contents[1]), 'options' : eval(contents[2]), 'answer' : int(contents[3])}

        answer_result.quiz_dict = quizzes

    except Exception as err:
         print('[ERROR][GENERATE_RECAP] : ', str(err))

    return answer_result

if __name__ == "__main__":
    base_file_path = os.path.join(os.getcwd(), "data", "시니어_디지털_범죄", "메신저 피싱.txt") 
    quizzes = {}
    init_recap = generate_init_recap(base_file_path=base_file_path)
    init_quiz = generate_init_quiz(init_recap)
    init_quiz_list = init_quiz.split('\n')
    for quiz in init_quiz_list:
        # parsing
        contents = quiz.split('\t')
        # string to other type
        quizzes[int(contents[0])] = {'question' : eval(contents[1]), 'options' : eval(contents[2]), 'answer' : int(contents[3])}
        # add_quiz(eval(quiz))
    print(quizzes)
    