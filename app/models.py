from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    edu_class_folder_name: Optional[str] = '시니어_디지털_범죄'
    edu_title_file_name: Optional[str] = '메신저_피싱.txt' # edu 자료 파일 이름(대본 txt, 자료 pdf)
    request_type: Optional[str] # answer, quiz, recap, debat 
    request_contents: Optional[str] = '' # debat, answer 요청일 때만 활성화
    recap_option: Optional[int] = -1 # recap 요청일 때만 활성화, 몇 줄로 요약?
    quize_option: Optional[int] = -1 # quiz 요청일 때만 활성화, 몇 개의 퀴즈 생성?

class TextResult(BaseModel):
    emotion: Optional[str] = "" # happy, sad ...
    txt_result: Optional[str] = "" # when answer, dabat, recap

class QuizResult(BaseModel):
    quiz_dict: Optional[dict] = {} # quize
