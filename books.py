from fastapi import FastAPI
from typing import Optional

app = FastAPI()

BOOKS = {
    "book_1": {"title": "title one", "author": "author one"},
    "book_2": {"title": "title two", "author": "author two"},
    "book_3": {"title": "title three", "author": "author three"},
    "book_4": {"title": "title four", "author": "author four"},
}


@app.get("/books")
async def books():
    return BOOKS


@app.get("/books/skip_book")
async def skip_book(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: str):
    return BOOKS.get(book_id)
