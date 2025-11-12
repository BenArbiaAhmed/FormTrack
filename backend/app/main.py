from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.v1 import router
from .middleware.cors import add_cors_middleware



app = FastAPI()

add_cors_middleware(app)

app.include_router(router=router.api_router, prefix="/api/v1")




