import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.router import RegisterRouterList
app = FastAPI()
# 定义一个通用的异常处理器
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"An internal server error occurred: {str(exc)}"}
    )
# 加载路由
for item in RegisterRouterList:
    app.include_router(item.router,prefix='/api')

    # await run_schedule()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)