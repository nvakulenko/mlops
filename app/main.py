from fastai.vision import *
import fastai; 
from io import BytesIO
from starlette.middleware.cors import CORSMiddleware

import logging, sys

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.templating import Jinja2Templates

import uvicorn

import aiohttp
import asyncio

import os

app = Starlette()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
templates = Jinja2Templates(directory='templates')

@app.middleware("http")
async def add_custom_header(request, call_next):
    version = fastai.__version__
    logging.info("fastai version: " + version)
    logging.info("====infostart====")
    response = await call_next(request)
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Allow'] = 'GET, POST'
    response.headers['Access-Control-Allow-Origin'] = '*'
    logging.info("====debugend====")
    return response


async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

class OptionsResponse(Response):
    media_type = None
    headers = {
            'Allow': 'GET, POST',
    }


@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    img = open_image(BytesIO(bytes))
    learner = load_learner(Path("/app"))
    _,_,losses = learner.predict(img)
    return JSONResponse({
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )})

@app.route("/classify-url", methods=["POST"])
async def classify_url(request):
    bytes = await request.body()
    img = open_image(BytesIO(bytes))
    learner = load_learner(Path("/app"))
    _,_,losses = learner.predict(img)


    return JSONResponse({
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True

        )})

