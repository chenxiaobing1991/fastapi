from fastapi import APIRouter
router = APIRouter(tags=["默认路由"])


# 注册具体方法
@router.get("/")
async def index():
    return {
        "code": 200,
        "msg": "Hello World!",
    }
