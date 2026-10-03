from time import sleep

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.main import run

from agent import ask_llm

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat")
async def chat(question) -> StreamingResponse:
    return StreamingResponse(
        ask_llm(question)
    )

if __name__ == "__main__":
    run(app)
