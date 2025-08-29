from typing import Protocol, TypeVar, Any

Model = TypeVar('Model')

class SQLRepository(Protocol):
    
    async def get_one(self, id: Any) -> Model:
        raise NotImplementedError
    
    async def get_all(self, limit=1000, offset=0) -> list[Model]:
        raise NotImplementedError
    
    async def create(self, data: dict) -> int:
        raise NotImplementedError
    
    async def delete(self, id: Any) -> None:
        raise NotImplementedError