import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.load_env import envs
from src.routers import estimate_sleep, extract_steps, llm_feedback

app = FastAPI()

# デバッグ時は print を無効化しない
if not envs.IS_DEBUG:
    sys.stdout = open(os.devnull, "w")


# TODO: 環境変数に追加する
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(extract_steps.router, prefix=envs.API_V1_PREFIX)
app.include_router(estimate_sleep.router, prefix=envs.API_V1_PREFIX)
app.include_router(llm_feedback.router, prefix=envs.API_V1_PREFIX)
