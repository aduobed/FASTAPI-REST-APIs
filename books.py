from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

BOOKS = {
    "book_1": {"title": "title one", "author": "author one"},
    "book_2": {"title": "title two", "author": "author two"},
    "book_3": {"title": "title three", "author": "author three"},
    "book_4": {"title": "title four", "author": "author four"},
}

class Book(BaseModel):
    title: str
    author: str


@app.get("/books/")
async def books():
    return BOOKS


@app.get("/books/skip_book/")
async def skip_book(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: str):
    return BOOKS.get(book_id)


@app.post("/books/")
async def create_book(title, author):
    get_last_book_num = 0

    if len(BOOKS) > 0:
        get_last_book_num = int(list(
            BOOKS.keys())[-1].split("_")[-1])

    BOOKS[f"book_{get_last_book_num + 1}"] = {"title": title, "author": author}
    return BOOKS[f"book_{get_last_book_num + 1}"]


@app.put("/books/{book_id}")
async def update_book(book_id: str, title: str, author: str):
    if BOOKS[book_id]:
        BOOKS[book_id] = {"title": title, "author": author}

    return BOOKS[book_id]


@app.delete("/books/{book_id}")
async def update_book(book_id: str):
    if BOOKS[book_id]:
        del BOOKS[book_id]

    return f"{book_id} has been deleted successfully"
