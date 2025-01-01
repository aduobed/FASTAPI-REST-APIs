from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

app = FastAPI()

books = []


class Book(BaseModel):
    id: UUID = None
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        title="Description of the book", max_length=100, min_length=1, default=None)
    rating: int = Field(gt=-1, lt=11)

    # Add a custom example to the json schema
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "2a1de2ce-7899-44c4-9947-da248418a967",
                    "title": "monkey king",
                    "author": "james david",
                    "description": "example of a description",
                    "rating": 3}
            ]
        }
    }


@app.get("/books/")
async def get_all_books(number_of_books: Optional[int] = None):
    if len(books) < 1:
        generate_book_data()

    if number_of_books and len(books) >= number_of_books > 0:
        return books[:number_of_books:]
    return books


@app.get("/books/skip_book/")
async def skip_book(skip_book: Optional[str] = None):
    if skip_book:
        new_books = books.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: UUID):
    return [book for book in books if book.id == book_id]


@app.post("/books/")
async def create_book(book: Book):
    if book.id is None:
        book.id = uuid4
    books.append(book)
    return books


@app.put("/books/{book_id}")
async def update_book(book_id: UUID, book: Book):
    get_book_index = [idx for idx, val in enumerate(
        books) if book_id == val.id]

    if get_book_index:
        books[get_book_index[0]] = book
        return books[get_book_index[0]]

    raise HTTPException(status_code=404, detail="Book not found", headers={
                        "X-Header-Error": "No UUID Header found"})


@app.delete("/books/{book_id}")
async def update_book(book_id: UUID):
    get_book_index = [idx for idx, val in enumerate(
        books) if book_id == val.id]

    if get_book_index:
        del books[get_book_index[0]]
        return f"{book_id} has been deleted successfully"

    raise HTTPException(status_code=404, detail="Book not found", headers={
                        "X-Header-Error": "No UUID Header found"})


def generate_book_data():
    book_1 = Book(id='3a1de2ce-7899-44c4-9947-da248418a967',
                  title='title 1',
                  author='author 1',
                  description='description 1',
                  rating='1')
    book_2 = Book(id='88168e82-251c-4b22-9138-f73d94f54ea7',
                  title='title 2',
                  author='author 2',
                  description='description 2',
                  rating='2')
    book_3 = Book(id='87aeeb07-5d9f-4158-933b-94009978b2a9',
                  title='title 3',
                  author='author 3',
                  description='description 3',
                  rating='3')
    book_4 = Book(id='b86fcb31-c5b8-4ad1-8771-bc99aa7b6e11',
                  title='title 4',
                  author='author 4',
                  description='description 4',
                  rating='4')

    books.append(book_1)
    books.append(book_2)
    books.append(book_3)
    books.append(book_4)
