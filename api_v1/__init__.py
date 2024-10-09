from fastapi import APIRouter

from .products.views import router as product_router
from .demo_auth.views import router as demo_auth_router
from .demo_auth.demo_jwt_auth import router as jwt_router

router = APIRouter()
router.include_router(router=jwt_router)
router.include_router(router=demo_auth_router)
router.include_router(router=product_router, prefix='/products')
