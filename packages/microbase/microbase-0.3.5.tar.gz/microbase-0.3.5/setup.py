import sys
from setuptools import setup, find_packages

_requirements = [
    'sanic-envconfig',
    'python-rapidjson',
    'structlog',
    'sl_api_client',
    'marshmallow'
]

if sys.version_info < (3, 7):
    _requirements.append('dataclasses')

setup(
    name='microbase',
    version='0.3.5',
    packages=find_packages(exclude=['tests', 'examples']),
    url='https://gitlab.itnap.ru/libs/python/microbase',
    license='',
    author='Dmitry Sobolev',
    author_email='ds@napoleonit.ru',
    description='',
    install_requires=_requirements,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio'
    ],
    test_suite='tests',
)
