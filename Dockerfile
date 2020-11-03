FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

# pre-install api dependencies to cache them
COPY ./requires.txt ./
RUN pip install -q -r requires.txt

COPY . .
RUN pip install .

EXPOSE 80

# https://github.com/tiangolo/meinheld-gunicorn-docker
ENV APP_MODULE fastapi_playground.main:app
ENV LOG_LEVEL warning
