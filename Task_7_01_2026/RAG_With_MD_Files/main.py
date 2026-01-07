from fastapi import FastAPI
from rag import ask

app = FastAPI()

@app.get("/ask")
def query_docs(q: str):
    return {"answer": ask(q)}
