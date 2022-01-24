from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"data": {"blog list"}}

@app.get("/blog/unpublished")
def unpublished():
    # fetch unpublished blogs
    return {'data' : 'all unpublished blogs'}

@app.get("/blog/{id}")
def show(id: int):
    # fetch blog id
    return {'data' : id}

@app.get("/blog/{id}/comments")
def comments(id):
    # fetch comments of blog id
    return {'data' : {'1','2','3'}}