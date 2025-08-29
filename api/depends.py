from typing import Annotated

from fastapi import Depends
from application.uow import UOWV1


UowDep = Annotated[UOWV1, Depends()]