from fastapi import FastAPI
from rag import ask
from schemas import MarkDownUpload
from ingest_runtime import insert_markdown_docs
from delete_collection import delete_all
from rag import search
from fastapi import UploadFile, File
from typing import List

app = FastAPI()


######################## Ask Queries to the Vector DB ########################
@app.get("/ask")
def query_docs(q: str):
    return {"answer": ask(q)}


######################### Search for Relevant Chunks ########################
@app.get("/relevent_chunks")
def get_relevent_chunks(q: str):
    return {"Most Relevent Chunks": search(q)}


######################## Ingest Markdown Documents ########################
@app.post("/upload_docs")
async def upload_docs(files: List[UploadFile] = File(...)):
    docs = []

    for file in files:
        content = (await file.read()).decode("utf-8")
        docs.append({
            "filename": file.filename,
            "content": content
        })

    count = insert_markdown_docs(docs)
    return {"status": "success", "chunks_added": count}


######################## Reset Collection ########################
@app.delete("/reset_collection")
def reset_collection():
    delete_all()
    return {"status": "Collection Reset"}
    