FROM tiangolo/uvicorn-gunicorn-starlette:python3.7


RUN pip install fastai==1.0.61 aiohttp

RUN pip install jinja2

RUN pip install starlette

COPY ./app ../app
COPY ./app ../model

WORKDIR /app

EXPOSE 80
