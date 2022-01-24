from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/blog")
# only get 10oublished blogs
def index(limit = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f'{limit} published blogs from the db list'}
    else:
        return {"data": f'{limit} blogs from the db list'}

@app.get("/blog/unpublished")
def unpublished():
    # fetch unpublished blogs
    return {'data' : 'all unpublished blogs'}

@app.get("/blog/{id}")
def show(id: int):
    # fetch blog id
    return {'data' : id}

@app.get("/blog/{id}/comments")
def comments(id, limit = 10):
    # fetch comments of blog id
    return {'data' : {'1','2','3'}}