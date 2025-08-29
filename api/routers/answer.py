from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from fastapi_cache.decorator import cache

from api.depends import UowDep
from api.mapper import ReadMapper
from api.serialize import ReadAnswer, ResponseAnswer
from infrastructure.exceptions import RowsNotFoundError

router = APIRouter(
    prefix='/answers',
    tags=['answers']
)


@router.get('/{id}')
@cache(expire=60)
async def get_answer(uow: UowDep, id: int) -> ReadAnswer:
    async with uow:
        try:
           read_model = await uow.answer_repository.get_one(id)
           return ReadMapper.map_answer(read_model)
        except RowsNotFoundError:
            logger.error(f'Answer not found {id}')
            raise HTTPException(status_code=404)

@router.delete('/{id}')
async def delete_answer(uow: UowDep, id: int) -> ResponseAnswer:
    async with uow:
        await uow.answer_repository.delete(id)
        await uow.commit()
        logger.info(f'Answer deleted {id}')
    return {'id': id}