from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    request_type: Optional[str] # answer, quiz, recap, debat 
    request_contents: Optional[str] = '' # debat, answer 요청일 때만 활성화
    recap_option: Optional[int] = -1 # recap 요청일 때만 활성화, 몇 줄로 요약?
    quize_option: Optional[int] = -1 # quiz 요청일 때만 활성화, 몇 개의 퀴즈 생성?


class TextResult(BaseModel):
    emotion: Optional[str] = "" # happy, sad ...
    txt_result: Optional[str] = "" # answer, dabat, recap

class QuizResult(BaseModel):
    quiz_list: Optional[list] = [] # quize
