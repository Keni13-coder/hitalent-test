from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, ProgrammingError
from ..models import Answer
from ..exceptions import RowsNotFoundError


class AnswerRepository:
    def __init__(self, session):
        self.session = session   
        
    async def create(self, data: dict) -> int:
        stmt = insert(Answer).values(**data).returning(Answer.id)
        try:
            return (await self.session.execute(stmt)).scalar_one()
        except ProgrammingError as e:
            raise RowsNotFoundError from e
    
    async def get_one(self, id: int) -> Answer:
        stmt = (
            select(Answer)
            .where(Answer.id == id)
        )
        try:
            return (await self.session.execute(stmt)).scalar_one()
        except NoResultFound as e:
            raise RowsNotFoundError from e

    async def get_all(self, limit=1000, offset=0) -> list[Answer]:
        ...
        
    async def delete(self, id: int) -> None:
        stmt = delete(Answer).where(Answer.id == id)
        await self.session.execute(stmt)