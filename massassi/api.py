import json

from django.http.response import Http404, HttpResponse
from ninja import NinjaAPI

from levels.api import router as levels_router
from saberworks.api import router as saberworks_router

api = NinjaAPI(csrf=True)

api.add_router("/levels/", levels_router)
api.add_router("/saberworks/", saberworks_router)

@api.exception_handler(Http404)
def not_found_error(request, exc):
    return api.create_response(
        request,
        { "error": "404", "message": "not found" },
        status=404,
    )
