from .auth import router as auth_router
from .ingredients import router as ingredient_router
from .tags import router as tag_router
from .users import router as user_router

__all__ = (
    'auth_router',
    'ingredient_router',
    'tag_router',
    'user_router',
)
