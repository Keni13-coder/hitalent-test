from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from fastapi_cache.decorator import cache

from api.depends import UowDep
from api.mapper import ReadMapper
from api.serialize import (
    RequestQuestion,
    RequestAnswer,
    ReadQuestion,
    ResponseQuestion,
    ResponseAnswer
    )
from infrastructure.exceptions import RowsNotFoundError

router = APIRouter(
    prefix='/questions',
    tags=['questions']
)


@router.get('/{id}')
@cache(expire=60)
async def get_question(uow: UowDep, id: int) -> ReadQuestion:
    async with uow:
        try:
           read_model = await uow.quest_repository.get_one(id)
           return ReadMapper.map_question(read_model)
        except RowsNotFoundError:
            logger.error(f'Question not found {id}')
            return HTTPException(status_code=404)
        except:
            logger.error(f'Server error {id}')
            raise HTTPException(status_code=500)

@router.get('/')
@cache(expire=60)
async def get_questions(
    uow: UowDep,
    limit=Query(default=1000),
    offset=Query(default=0)
    ) -> list[ReadQuestion]:
    async with uow:
        read_models = await uow.quest_repository.get_all(limit, offset)
        return [ReadMapper.map_question(read_model) for read_model in read_models]

@router.post('/')
async def create_question(payload: RequestQuestion, uow: UowDep) -> ResponseQuestion:
    async with uow:
        return_id = await uow.quest_repository.create(payload.model_dump())
        await uow.commit()
    return {'id': return_id}

@router.post('/{id}/answers')
async def create_answer(payload: RequestAnswer, uow: UowDep, id: int) -> ResponseAnswer:
    async with uow:
        data = payload.model_dump()
        data['question_id'] = id
        try:
            return_id = await uow.answer_repository.create(data)
        except RowsNotFoundError:
            logger.error(f'Question not found {id}')
            raise HTTPException(status_code=404)
        await uow.commit()
    return {'id': return_id}

@router.delete('/{id}')
async def delete_question(uow: UowDep, id: int):
    async with uow:
        await uow.quest_repository.delete(id)
        await uow.commit()
        logger.info(f'Question deleted {id}')
    return {'id': id}