from starlette.requests import Request
from starlette.responses import Response

from limsmock.filter import Filter
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_controltypes(request: Request):
    entity_type = {'sing': 'controltype', 'plur': 'controltypes'}

    params = request.query_params.multi_items()

    filter = Filter(params=params)
    xml = filter.make_entity_xml(db=request.app.db, entity_type=entity_type, base_uri=request.app.baseuri)

    return Response(content=xml)


@router.get("/{entity_id}")
def get_controltype(entity_id, request: Request):
    db = request.app.db

    return Response(content=db['controltypes'].get(entity_id))


@router.put("/{entity_id}")
async def put_controltype(entity_id, request: Request):
    body = await request.body()

    request.app.db['controltypes'][entity_id] = body
    return Response(content=body)
