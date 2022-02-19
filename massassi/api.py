from ninja import NinjaAPI

from levels.api import router as levels_router

api = NinjaAPI()

api.add_router("/levels/", levels_router)
