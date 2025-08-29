from infrastructure.base import async_session_maker
from infrastructure.repository import AnswerRepository, QuestRepository

class UOWV1:
    def __init__(self):
        self.session_factory = async_session_maker
        
    
    async def __aenter__(self):
        self._session = self.session_factory()
        
        self.quest_repository = QuestRepository(self._session)
        self.answer_repository = AnswerRepository(self._session)
        
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self._session.rollback()
        await self._session.close()
        
    async def commit(self):
        await self._session.commit()