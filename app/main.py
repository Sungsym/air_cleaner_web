from contextlib import asynccontextmanager
from datetime import datetime

from sqlmodel import Session, select
from starlette import status
from scalar_fastapi import get_scalar_api_reference

from fastapi import FastAPI, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.models import Air
from app.database.session import get_session, create_db_and_tables
from app.schemas import AirRead, AirCreate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print('#' * 100)
    print("服务器已启动")
    print('#' * 100)
    await create_db_and_tables()
    yield
    print('#' * 100)
    print("服务器已关闭")
    print('#' * 100)
app = FastAPI(lifespan=lifespan_handler)

@app.get("/air", response_model=list[AirRead])
async def read_air(
    start: str,
    end: str | None = Query(description="截止日期", default=datetime.today().isoformat()),
    session: Session = Depends(get_session)
):
    statement = select(Air).where(
        Air.datetime >= start,
        Air.datetime <= end
    )

    result = await session.execute(statement)
    airs = result.scalars().all()

    if not airs:
        raise HTTPException(
            status_code=404,
            detail="查询的数据不存在哦"
        )

    return airs

@app.post("/air", response_model=AirRead)
async def create_air(data: AirCreate, session: Session = Depends(get_session)):
    data = {
        "datetime": datetime.now().isoformat(),
        **data.model_dump()
    }
    new_air = Air(**data)

    session.add(new_air)
    await session.commit()
    await session.refresh(new_air)

    return new_air


@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        # openapi_url=app.openapi_url,
        title="Scalar API",
    )







# taskkill /IM python.exe /F