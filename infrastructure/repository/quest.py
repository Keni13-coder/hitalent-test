from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from ..models import Question
from ..exceptions import RowsNotFoundError

class QuestRepository:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session    
    
    async def create(self, data: dict) -> int:
        stmt = insert(Question).values(**data).returning(Question.id)
        return (await self.session.execute(stmt)).scalar_one()
    
    async def get_one(self, id: int) -> Question:
        stmt = (
            select(Question)
            .options(selectinload(Question.answers))
            .where(Question.id == id)
        )
        try:
            return (await self.session.execute(stmt)).scalar_one()
        except MultipleResultsFound:
            raise
        except NoResultFound as e:
            raise RowsNotFoundError from e
        
    async def get_all(self, limit=1000, offset=0) -> list[Question]:
        stmt = (
            select(Question)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
    
        questions = result.scalars().all()
        return questions
    
    async def delete(self, id: int) -> None:
        stmt = delete(Question).where(Question.id == id)
        await self.session.execute(stmt)