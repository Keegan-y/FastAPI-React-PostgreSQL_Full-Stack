import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from db import dbconf, models
from routes import api_router
from conf import ProjectSettings

# REST API Settings
app = FastAPI(title=ProjectSettings.PROJECT_NAME,
              description=ProjectSettings.PROJECT_DESCRIPTION,
              version="2.5.0",
              docs_url=None,
              redoc_url=None,
              openapi_url=f"{ProjectSettings.API_VERSION_PATH}/openapi.json")
# Middleware Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=ProjectSettings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routes
# app.include_router(api_router, prefix=ProjectSettings.API_VERSION_PATH)
app.include_router(api_router)

# app.include_router(api_router)
# app.include_router(users.router, tags=["users"])
# app.include_router(posts.router, tags=["posts"])


# https://fastapi.tiangolo.com/tutorial/sql-databases/
# python 3.6 database session
# from app.db import SessionLocal
# from fastapi import Depends, FastAPI, HTTPException, Request, Response
# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response
#
#
# # Dependency
# def get_db(request: Request):
#     return request.state.db

# Server startup event
@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=dbconf.engine)


# Root API
@app.get("/")
def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={"message": "Welcome to Demo Server"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
