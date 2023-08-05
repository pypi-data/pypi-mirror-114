from fastapi.params import Depends
from starlette.requests import Request
from starlette.responses import Response

from limsmock.filter import Filter
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_workflows(request: Request):
    entity_type = {'sing': 'workflow', 'plur': 'workflows'}

    params = request.query_params.multi_items()

    filter = Filter(params=params)
    xml = filter.make_entity_xml(db=request.app.db, entity_type=entity_type, base_uri=request.app.baseuri)

    return Response(content=xml)


@router.get("/{entity_id}")
def get_workflow(entity_id, request: Request):
    db = request.app.db

    return Response(content=db['workflows'].get(entity_id))


@router.put("/{entity_id}")
async def put_workflow(entity_id, request: Request):
    body = await request.body()

    request.app.db['workflows'][entity_id] = body
    return Response(content=body)
