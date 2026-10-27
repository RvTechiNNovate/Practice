from fastapi import FastAPI, Request
import time

app=FastAPI()

import logging 
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger("api_logger")


#-------------------- processing time  handling middleware---------------

@app.middleware("http")
async def add_process_time_header(req: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(req)
    process_time = time.perf_counter() - start_time
    logger.info("time taken to process the request: "+str(process_time))
    response.headers["X-Process-Time"] = str(process_time)
    return response


#-------------------- Loggger handling middleware---------------

@app.middleware("http")
async def request_logging(req:Request,my_func):
    logger.info("Api call started: "+req.method+"")
    response = await my_func(req)
    logger.info("API call completed")
    return response


#-------------------- random request id uuid handling middleware---------------


import uuid
@app.middleware("http")
async def request_id_gen(req:Request,func):
    request_id=str(uuid.uuid4())
    req.state.request_id=request_id
    response=await func(req)
    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/item")
def get_item(request:Request):
    return {"request_id": request.state.request_id}


#-------------------- exception handling middleware---------------

from fastapi.responses import JSONResponse

class UserNotFoundError(Exception):
    pass


@app.exception_handler(UserNotFoundError)
async def exception_hanlingUsernotfound(req:Request,exc:UserNotFoundError):
    return JSONResponse(
        status_code=403,
        content={"detail": "User account is inactive"}
    )

@app.get("/dashboard")
async def dashboard():
    raise UserNotFoundError()


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8001)