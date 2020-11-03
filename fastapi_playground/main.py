from fastapi_playground.logger import NoHealth, get_basic_logger
from os import environ
import random
from time import perf_counter

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config
from expiring_dict import ExpiringDict

known_cookies = ExpiringDict(600)

logger = get_basic_logger(__name__, 'DEBUG')
logger.addFilter(NoHealth())

"""
one of our dependencies probably locked the seed somewhere.
However, I actually need the global random.
If unlocking the random seed breaks your code,
you should create a new random instance and lock only the one you created
"""
random.seed()

# For deployment. SCRIPT_NAME is the root path of uvicorn.
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/
SCRIPT_NAME = Config()('SCRIPT_NAME', default='')

TITLE = 'Sticky Session Demo'

app = FastAPI(
    title=TITLE,
    openapi_prefix=SCRIPT_NAME,
)


origins = [
    'http://localhost:3000',
    'https://dev.dev.xaipient.com',
    'https://demo.dev.xaipient.com',
    'https://demo.test.xaipient.com',
    'https://demo.xaipient.com',
    'https://dev.xaipient.com',
]


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = perf_counter()

    response = await call_next(request)

    process_time = round(perf_counter() - start_time, 3)
    if process_time > 1:
        logger.warning(
            f'`{request.method} {request.url}` took {process_time} seconds')
    response.headers['X-Process-Time'] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

POD_ID = environ.get('POD_ID', 'unknown')


@app.get('/', tags=['other'])
async def hello(req: Request):
    user_ingress_cookie = req.cookies.get('INGRESSCOOKIE')
    is_known_user = user_ingress_cookie in known_cookies
    if user_ingress_cookie:
        known_cookies[user_ingress_cookie] = True
    return {'message': 'Hello from Sticky Session Demo',
            'pod_id': POD_ID,
            'root_path': req.scope.get('root_path'),
            'user_ingress_cookie': user_ingress_cookie,
            'is_known_user': is_known_user,
            }


@app.get('/healthcheck', tags=['other'])
async def healthcheck():
    return {'message': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=4000)
