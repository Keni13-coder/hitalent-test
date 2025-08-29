import pytest
from infrastructure.repository import QuestRepository, AnswerRepository


@pytest.fixture(scope="module")
async def quest_repository(session):
    return QuestRepository(session)


@pytest.fixture(scope="module")
async def quest_repository_with_data(session):
    repository = QuestRepository(session)

    await repository.create(data={
        'text': 'test 2-3-4'
    })
    await repository.session.commit()
    return repository
    
@pytest.fixture(scope="module")
async def answer_repository(session):
    return AnswerRepository(session)