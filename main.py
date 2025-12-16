import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.api.items import router as item_router
from app.api.categories import router as category_router
from app.api.locations import router as location_router
from app.api.messages import router as message_router
from app.api.reviews import router as review_router
from app.api.roles import router as role_router
from app.api.web import router as web_router

app = FastAPI(title="ТовароОбмен", version="0.0.1")

app.mount("/static", StaticFiles(directory="app/static"), "static")
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутеры
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(item_router)
app.include_router(category_router)
app.include_router(location_router)
app.include_router(message_router)
app.include_router(review_router)
app.include_router(role_router)
app.include_router(web_router)


@app.get("/")
def home_page():
    return RedirectResponse(url="/web/index")

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)

# uvicorn main:app --reload