import uvicorn
from fastapi import FastAPI, status
from limsmock.store import build_db
from limsmock.routers import (artifactgroups,
                              artifacts,
                              automations,
                              protocols,
                              udfs,
                              udts,
                              workflows,
                              containers,
                              containertypes,
                              controltypes,
                              files,
                              instruments,
                              labs,
                              permissions,
                              processes,
                              processtemplates,
                              processtypes,
                              projects,
                              reagentkits,
                              reagentlots,
                              reagenttypes,
                              researchers,
                              roles,
                              samples)

app = FastAPI()


def run_server(file_path: str, host: str, port: str) -> None:
    """Starting up the server. This is the function that needs
    to be imported and used in the server fixure for your test
    
    Args:
        host: ..
        port: ..
        file_path: 
            Path to the xmls of the specific test. 
            Assumeds file structure:
                <file_path>
                    - <entity type>
                        - <entiry_id>.xml
                        
            eg: 
                <file_path>
                    - samples
                        - S1.xml
                        - S2.xml
                    - processes
                        - P1.xml
                        - P2.xml
     """

    app.db = build_db(file_path)
    app.baseuri = f'http://{host}:{port}'
    uvicorn.run(app, host=host, port=port)


app.include_router(
    samples.router,
    prefix="/api/v2/samples",
    tags=["samples"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Sample not found"}}
)

app.include_router(
    artifacts.router,
    prefix="/api/v2/artifacts",
    tags=["artifacts"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Artifact not found"}}
)

app.include_router(
    containertypes.router,
    prefix="/api/v2/containertypes",
    tags=["containertypes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "containertype not found"}}
)

app.include_router(
    containers.router,
    prefix="/api/v2/containers",
    tags=["containers"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "container not found"}}
)

app.include_router(
    automations.router,
    prefix="/api/v2/configuration/automations",
    tags=["automations"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "automation not found"}}
)

app.include_router(
    artifactgroups.router,
    prefix="/api/v2/artifactgroups",
    tags=["artifactgroups"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "artifactgroup not found"}}
)

app.include_router(
    workflows.router,
    prefix="/api/v2/configuration/workflows",
    tags=["workflows"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Workflow not found"}}
)

app.include_router(
    udts.router,
    prefix="/api/v2/configuration/udts",
    tags=["udts"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Udt not found"}}
)

app.include_router(
    udfs.router,
    prefix="/api/v2/configuration/udfs",
    tags=["udfs"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Udf not found"}}
)

app.include_router(
    roles.router,
    prefix="/api/v2/roles",
    tags=["roles"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Role not found"}}
)

app.include_router(
    researchers.router,
    prefix="/api/v2/researchers",
    tags=["researchers"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Researcher not found"}}
)

app.include_router(
    reagenttypes.router,
    prefix="/api/v2/reagenttypes",
    tags=["reagenttypes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Reagenttype not found"}}
)

app.include_router(
    reagentlots.router,
    prefix="/api/v2/reagentlots",
    tags=["reagentlots"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Reagentlot not found"}}
)

app.include_router(
    reagentkits.router,
    prefix="/api/v2/reagentkits",
    tags=["reagentkits"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Reagentkit not found"}}
)

app.include_router(
    protocols.router,
    prefix="/api/v2/configuration/protocols",
    tags=["protocols"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Protocol not found"}}
)
app.include_router(
    controltypes.router,
    prefix="/api/v2/controltypes",
    tags=["controltypes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "controltype not found"}}
)

app.include_router(
    files.router,
    prefix="/api/v2/files",
    tags=["files"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "file not found"}}
)

app.include_router(
    instruments.router,
    prefix="/api/v2/instruments",
    tags=["instruments"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "instrument not found"}}
)

app.include_router(
    labs.router,
    prefix="/api/v2/labs",
    tags=["labs"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "lab not found"}}
)

app.include_router(
    permissions.router,
    prefix="/api/v2/permissions",
    tags=["permissions"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "permission not found"}}
)

app.include_router(
    processes.router,
    prefix="/api/v2/processes",
    tags=["processes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "processe not found"}}
)

app.include_router(
    processtemplates.router,
    prefix="/api/v2/processtemplates",
    tags=["processtemplates"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "processtemplate not found"}}
)

app.include_router(
    processtypes.router,
    prefix="/api/v2/processtypes",
    tags=["processtypes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "processtype not found"}}
)

app.include_router(
    projects.router,
    prefix="/api/v2/projects",
    tags=["projects"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "project not found"}}
)
