from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def books():
    return {'message': 'books'}
