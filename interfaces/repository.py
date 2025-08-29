from typing import Protocol, TypeVar

Model = TypeVar('Model')

class SQLRepository(Protocol):
    
    async def get_one(self, id: int) -> Model:
        raise NotImplementedError
    
    async def get_all(self) -> list[Model]:
        raise NotImplementedError
    
    async def create(self, data: dict) -> int:
        raise NotImplementedError
    
    async def delete(self, id: int) -> None:
        raise NotImplementedError