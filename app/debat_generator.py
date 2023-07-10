import os
## for docker build
from app.models import TextResult
from app.recap_generator import *
from app.chatgpt import *
from app.utils import *

## for development environment
# from models import *
# from recap_generator import *
# from chatgpt import *
# from utils import *


def make_messages(role, content):
    return  [{
        'role': role,
        'content': content
    }]

def generate_debat_answer(state, text):
    messages = state + make_messages('user', text)

    ans = ChatGPT(messages)
 
    new_state = [{
        'role': 'user',
        'content': text
    }, {
        'role': 'assistant',
        'content': ans
    }]
 
    state = state + new_state
 
    return state, ans

def generate_debat(user_request: UserRequest) -> TextResult:
    answer_result = TextResult()
    base_file_path = create_base_path(user_request.edu_class_folder_name, user_request.edu_title_file_name)
    state = eval(user_request.state)
    try:
            # 1. 첫 문자열이 비었을 경우 토론 주제 생성
            if len(state) == 0:
                generated_recap = generate_init_recap(base_file_path)
                generated_recap = format_recap(generated_recap, base_file_path=base_file_path)
                print(generated_recap)

                init_prompt = "아래 [요약]을 통해 {토론 주제} 1개를 설정하고 [양식]에 따라 작성해. \
                              {토론 주제}는 제시하는 말투로 작성해. \n \
                              [요약]\n" + generated_recap + "\n" + \
                              "[양식] \n \
                              {토론 주제}"\
                
                topic = ChatGPT(make_messages('user', init_prompt))
                answer_result.topic = topic

                print("주제 : " + topic)

                init_prompt = "나는 너가 나와 토론자처럼 행동하길 원해. 우리는 <"+topic+">에 대해서 토론 할거야.\
                아래 조건에 따라 [토론 양식]을 작성할건데,\n \
                {너의 의견}을 작성 할 때는 반드시 존댓말을 사용하여 3줄 이내로 작성해.\n \
                [토론 양식]\n  \
                {너의 의견}"
                                    
                state, ans = generate_debat_answer(state, init_prompt)
            # 2. 내용이 있을 경우 이어지는 내용 생성
            else:
                state, ans = generate_debat_answer(state, user_request.request_contents)
    except Exception as err:
        print('[ERROR][GENERATE_DEBAT] : ', str(err))


    answer_result.txt_result = ans
    answer_result.state = str(state)

    return answer_result


if __name__ == '__main__' :
    user_request = UserRequest()
    answer_result = TextResult()
    base_file_path = create_base_path(user_request.edu_class_folder_name, user_request.edu_title_file_name)
    state = ''
    while True:
        user_request.state = answer_result.state
        user_input = input("답변(종료 > exit): ")
        if user_input == "exit":
            break
        try:
            user_request.request_contents = user_input
            # 1. 첫 문자열이 비었을 경우 토론 주제 생성
            if len(user_request.state) == 0:
                generated_recap = generate_init_recap(base_file_path)
                generated_recap = format_recap(generated_recap, base_file_path=base_file_path)
                print(generated_recap)

                init_prompt = "아래 [요약]을 통해 {토론 주제} 1개를 설정하고 [양식]에 따라 작성해. \
                              {토론 주제}는 제시하는 말투로 작성해. \n \
                              [요약]\n" + generated_recap + "\n" + \
                              "[양식] \n \
                              {토론 주제}"\
                
                topic = ChatGPT(make_messages('user', init_prompt))
                answer_result.topic = topic

                print("주제 : " + topic)

                init_prompt = "너는 토론의 상대편이 된 것처럼 행동해. 우리는 <"+topic+">에 대해서 토론 할거야.\
                아래 조건에 따라 [토론 양식]을 작성할건데,\n \
                {너의 의견}을 작성 할 때는 반드시 존댓말을 사용하여 3줄 이내로 작성해.\n \
                [토론 양식]\n  \
                {너의 의견}"
                                    
                state, ans = generate_debat_answer(user_request.state, init_prompt)
            # 2. 내용이 있을 경우 이어지는 내용 생성
            else:
                state, ans = generate_debat_answer(user_request.state, user_request.request_contents)
        except Exception as err:
            print('[ERROR][GENERATE_DEBAT] : ', str(err))


        answer_result.txt_result = ans
        answer_result.state = state
        print()
        print(user_request.state)
        print()
        print(answer_result.state)
        print()
        print(ans)
        

        
    