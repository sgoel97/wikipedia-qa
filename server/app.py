import os
from dotenv import load_dotenv
from llama_index import (
    download_loader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PERSIST_DIR = "./storage"


@app.on_event("startup")
def on_startup():
    load_dotenv()
    if not os.path.exists(PERSIST_DIR):
        WikipediaReader = download_loader("WikipediaReader")
        loader = WikipediaReader()
        documents = loader.load_data(
            pages=["Berlin", "Rome", "Tokyo", "Canberra", "Santiago"]
        )
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context=storage_context)


@app.get("/api/v1/question")
def get_answer(q: str):
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context=storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(q)
    return response.response
