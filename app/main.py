from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import Session
from starlette import status

from app.database.models import Air
from app.database.session import get_session, create_db_and_tables
from app.schemas import AirRead, AirCreate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print('#' * 100)
    print("服务器已启动")
    print('#' * 100)
    create_db_and_tables()
    yield
    print('#' * 100)
    print("服务器已关闭")
    print('#' * 100)
app = FastAPI(lifespan=lifespan_handler)

@app.get("/air", response_model=AirRead)
def read_air(id: int, session: Session = Depends(get_session)):
    air = session.get(Air, id)
    if air is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="这个数据不存在哦"
        )

    return air

@app.post("/air", response_model=AirRead)
def create_air(data: AirCreate, session: Session = Depends(get_session)):
    data = {
        "datetime": datetime.now().isoformat(),
        **data.model_dump()
    }
    new_air = Air(**data)

    session.add(new_air)
    session.commit()
    session.refresh(new_air)

    return new_air


@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        # openapi_url=app.openapi_url,
        title="Scalar API",
    )

# taskkill /IM python.exe /F