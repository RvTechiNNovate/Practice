from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

class RequestPayload(BaseModel):
    id:str
    name:str
    age:str

app=FastAPI()

@app.get("/item/{item_id}")
def read_api(item_id:str):
    return {"result": f"hi there this is my api response with item id: {item_id}"}

@app.post("/")
def post_api(data:RequestPayload):
    print(data.id)
    print(data.name)
    print(data.age)
    return {"result":"this post request is successful"}

@app.put("/")
def put_api(data:RequestPayload):
    print("checking if old is already exist if not can return to please add this id firs")
    print(data.id)
    print(data.name)
    print(data.age)
    return {"result":"this put request is successful"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)