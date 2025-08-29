from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RequestQuestion(BaseModel):
    text: str
    
class ResponseQuestion(BaseModel):
    id: int

class ReadQuestion(ResponseQuestion, RequestQuestion):
    created_at: datetime
    
    answers: Optional[list['ReadAnswer']] = []
    
    
class RequestAnswer(BaseModel):
    text: str
    user_id: str

class ResponseAnswer(BaseModel):
    id: int

class ReadAnswer(ResponseAnswer, RequestAnswer):
    created_at: datetime