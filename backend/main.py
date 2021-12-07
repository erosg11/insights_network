from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dependencies import database
from entitys import Base
from routes import router_insight, router_tag

app = FastAPI(title='Insights', version='0.0.1', default_response_class=ORJSONResponse)


@app.on_event('startup')
async def startup():
    engine = create_engine(f'sqlite:///./app.db', connect_args={"check_same_thread": False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    database.Session = Session


@app.on_event('shutdown')
async def shutdown():
    database.Session.close_all()


app.include_router(
    router_insight,
    prefix='/insight',
    tags=['insights']
)

app.include_router(
    router_tag,
    prefix='/tag',
    tags=['tag']
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
