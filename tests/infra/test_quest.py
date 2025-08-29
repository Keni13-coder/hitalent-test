import pytest

from infrastructure.exceptions import RowsNotFoundError


ids = {
    'quest_id': None,
    'answer_id': None
}

@pytest.mark.asyncio(loop_scope='module')
async def test_quest_create(quest_repository):
    data = {
        'text': 'test',
    }
    return_id = await quest_repository.create(data)
    await quest_repository.session.commit()
    assert return_id

    ids['quest_id'] = return_id
    
@pytest.mark.asyncio(loop_scope='module')
async def test_answer_create(answer_repository):
    data = {
        'question_id': ids['quest_id'],
        'text': 'test',
        'user_id': '123'
        
    }
    return_id = await answer_repository.create(data)
    await answer_repository.session.commit()
    
    assert return_id
    ids['answer_id'] = return_id
    
@pytest.mark.asyncio(loop_scope='module')
async def test_quest_get_one(quest_repository):
    return_data = await quest_repository.get_one(ids['quest_id'])
    
    assert return_data
    assert len(return_data.answers) > 0
    
@pytest.mark.asyncio(loop_scope='module')
async def test_quest_get_all(quest_repository_with_data):
    return_data = await quest_repository_with_data.get_all()
    
    assert return_data
    assert len(return_data) > 1

@pytest.mark.asyncio(loop_scope='module')
async def test_quest_delete(quest_repository):
    await quest_repository.delete(ids['quest_id'])
    await quest_repository.session.commit()
    
@pytest.mark.asyncio(loop_scope='module')
async def test_answer_get_one(answer_repository):
    
    with pytest.raises(RowsNotFoundError):
        return_data = await answer_repository.get_one(ids['answer_id'])
    