from api.serialize import ReadQuestion, ReadAnswer

class ReadMapper:
    
    @staticmethod
    def map_question(question):
        return ReadQuestion.model_validate(question, from_attributes=True)
        
    @staticmethod
    def map_answer(answer):
        return ReadAnswer.model_validate(answer, from_attributes=True)