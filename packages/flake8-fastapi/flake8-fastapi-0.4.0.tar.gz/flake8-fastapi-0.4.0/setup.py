# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_fastapi', 'flake8_fastapi.visitors']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.65.1,<0.66.0', 'flake8-plugin-utils>=1.3.2,<2.0.0']

entry_points = \
{'flake8.extension': ['CF = flake8_fastapi.plugin:FastAPIPlugin']}

setup_kwargs = {
    'name': 'flake8-fastapi',
    'version': '0.4.0',
    'description': 'flake8 plugin that checks FastAPI code against opiniated style rules 🤓',
    'long_description': '<h1 align="center">\n    <strong>flake8-fastapi</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/flake8-fastapi" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/flake8-fastapi" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/flake8-fastapi/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/flake8-fastapi">\n    <br />\n    <a href="https://pypi.org/project/flake8-fastapi" target="_blank">\n        <img src="https://img.shields.io/pypi/v/flake8-fastapi" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/flake8-fastapi">\n    <img src="https://img.shields.io/github/license/Kludex/flake8-fastapi">\n</p>\n\nA [flake8](https://flake8.pycqa.org/en/latest/index.html) plugin that helps you avoid simple FastAPI mistakes.\n\n## Installation\n\nFirst, install the package:\n\n``` bash\npip install flake8-fastapi\n```\n\nThen, check if the plugin is installed using `flake8`:\n\n``` bash\n$ flake8 --version\n3.9.2 (flake8-fastapi: 0.2.0, mccabe: 0.6.1, pycodestyle: 2.7.0, pyflakes: 2.3.1) CPython 3.8.11 on Linux\n```\n\n## Rules\n\n### Route Decorator Error (CF001)\n\nDevelopers that were used to [flask](https://flask.palletsprojects.com/en/2.0.x/) can be persuaded or want to use the same pattern in FastAPI:\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n\n@app.route("/", methods=["GET"])\ndef home():\n    return "Hello world!"\n```\n\nBut on FastAPI, we have a simpler way to define this (and is the most known way to create endpoints):\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n\n@app.get("/")\ndef home():\n    return "Hello world!"\n```\n\n### Route Prefix Error (CF002)\n\nOn old FastAPI versions, we were able to add a prefix only on the `include_router` method:\n\n```python\nfrom fastapi import APIRouter, FastAPI\n\nrouter = APIRouter()\n\n\n@router.get("/")\ndef home():\n    ...\n\n\napp = FastAPI()\napp.include_router(router, prefix="/prefix")\n```\n\nNow, it\'s possible to add in the `Router` initialization:\n\n```python\nfrom fastapi import APIRouter, FastAPI\n\nrouter = APIRouter(prefix="/prefix")\n\n\n@router.get("/")\ndef home():\n    ...\n\n\napp = FastAPI()\napp.include_router(router)\n```\n\n### Generic Exception Handler\n\nFastAPI doesn\'t allow us to handle the base `Exception` with `exception_handler` decorator.\nIt\'s due to Starlette implementation, but well, FastAPI inherits the issue.\n\nTo be more precise, you\'ll be able to receive the response, but as soon as you check the server logs, you\'ll see an unexpected trace log.\n\nTo exemplify, you can\'t do:\n\n```python\nfrom fastapi import FastAPI, Request\nfrom starlette.responses import JSONResponse\n\napp = FastAPI()\n\n\n@app.exception_handler(Exception)\nasync def generic_exception_handler(request: Request, exc: Exception):\n    return JSONResponse(status_code=200, content="It doesn\'t work!")\n\n\n@app.get("/")\nasync def home():\n    raise Exception()\n```\n\nBut you can create a new exception, inheriting from `Exception`, or use [`HTTPException`](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception):\n\n```python\nfrom fastapi import FastAPI, Request\nfrom starlette.responses import JSONResponse\n\napp = FastAPI()\n\n\nclass NewException(Exception):\n    ...\n\n\n@app.exception_handler(NewException)\nasync def new_exception_handler(request: Request, exc: NewException):\n    return JSONResponse(status_code=200, content="It works!")\n\n\n@app.get("/")\nasync def home():\n    raise NewException()\n\n```\n\n\n### CORSMiddleware Order (CF008)\n\nThere\'s a [tricky issue](https://github.com/tiangolo/fastapi/issues/1663) about [CORSMiddleware](https://www.starlette.io/middleware/#corsmiddleware) that people are usually unaware. Which is that this middleware should be the last one on the middleware stack. You can read more about it [here](https://github.com/tiangolo/fastapi/issues/1663).\n\nLet\'s see an example of what doesn\'t work:\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=[\'*\'],\n    allow_credentials=True,\n    allow_methods=[\'*\'],\n    allow_headers=[\'*\']\n)\napp.add_middleware(GZipMiddleware)\n```\n\nAs you see, the last middleware added is not `CORSMiddleware`, so it will not work as expected. On the other hand, if you change the order, it will:\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\napp.add_middleware(GZipMiddleware)\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=[\'*\'],\n    allow_credentials=True,\n    allow_methods=[\'*\'],\n    allow_headers=[\'*\']\n)\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/flake8-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
