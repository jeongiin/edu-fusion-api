import os

## for docker build
from app.models import TextResult, QuizResult
from app.apikey import OPENAI_API_KEY
from app.recap_generator import *
from app.chatgpt import *
from app.utils import *

## for development environment
# from models import TextResult, QuizResult
# from apikey import OPENAI_API_KEY
# from recap_generator import *
# from chatgpt import *
# from utils import *

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY # openai 에서 발급 받은 key 입력

    
def generate_init_quiz(recap: str) -> str:
    # recap을 통해 객관식 퀴즈 생성
    prompt = "아래 [내용]으로 객관식 퀴즈를 [퀴즈 형식]에 맞게 한글로 만들어. \n \
            틀린 보기를 만들 때 너가 이미 알고 있는 지식을 이용할 수 있어. \n \
            {퀴즈 번호}와 {답}은 int 형이야. \n \
            {객관식 보기 내용}은 명사형 종결 어미로 만들어. \n \
            퀴즈를 2개 이상 만들었다면 [퀴즈 형식] 사이를 '\n'로 구별해줘. \
            [퀴즈 형식]\n \
            {퀴즈 번호}\t '{퀴즈 문제}'\t ['{객관식 보기 내용}', '{객관식 보기 내용}','{객관식 보기 내용}', '{객관식 보기 내용}'] \t {해당 문제의 답}" \
            + "\n [내용] \n"
    
    prompt += recap
    

    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "너는 교육을 위한 문제 출제자야."},
            {"role": "user", "content": prompt}
    ]

    answer = ChatGPT(messages=messages)

    
    return answer


def generate_quiz(user_request: UserRequest) -> TextResult:
    answer_result = QuizResult()
    base_file_path = create_base_path(user_request.edu_class_folder_name, user_request.edu_title_file_name)
    quizzes = {}
    for make_quiz_try in range(5):
        try:
            init_recap = generate_init_recap(base_file_path=base_file_path)
            ko_init_quiz = format_recap(init_recap, base_file_path=base_file_path)
            init_quiz = generate_init_quiz(ko_init_quiz)

            init_quiz_list = init_quiz.split('\n')
            print(init_quiz_list)
            for quiz in init_quiz_list:
                # parsing
                contents = quiz.split('\t')
                # string to other type
                q_key = 'q'+str(int(contents[0]))
                quizzes[q_key] = {}
                quizzes[q_key]['q'] = eval(contents[1])
                quizzes[q_key]['o1'] = eval(contents[2])[0]
                quizzes[q_key]['o2'] = eval(contents[2])[1]
                quizzes[q_key]['o3'] = eval(contents[2])[2]
                quizzes[q_key]['o4'] = eval(contents[2])[3]
                quizzes[q_key]['a'] = 'a' + str(eval(contents[3]))

            answer_result.quiz_dict = quizzes
            break

        except Exception as err:
            print('[ERROR][GENERATE_RECAP] : ', str(err))

    return answer_result

if __name__ == "__main__":
    user_request = UserRequest()
    base_file_path = create_base_path(user_request.edu_class_folder_name, user_request.edu_title_file_name)
    answer_result = QuizResult()
    quizzes = {}

    for make_quiz_try in range(5):
        try:
            init_recap = generate_init_recap(base_file_path=base_file_path)
            ko_init_quiz = format_recap(init_recap, base_file_path=base_file_path)
            init_quiz = generate_init_quiz(ko_init_quiz)

            init_quiz_list = init_quiz.split('\n')
            print(init_quiz_list)
            for quiz in init_quiz_list:
                # parsing
                contents = quiz.split('\t')
                # string to other type
                q_key = 'q'+str(int(contents[0]))
                quizzes[q_key] = {}
                quizzes[q_key]['q'] = eval(contents[1])
                quizzes[q_key]['o1'] = eval(contents[2])[0]
                quizzes[q_key]['o2'] = eval(contents[2])[1]
                quizzes[q_key]['o3'] = eval(contents[2])[2]
                quizzes[q_key]['o4'] = eval(contents[2])[3]
                quizzes[q_key]['a'] = 'a' + str(eval(contents[3]))

            answer_result.quiz_dict = quizzes
            break

        except Exception as err:
            print('[ERROR][GENERATE_RECAP] : ', str(err))

    print(quizzes)
    