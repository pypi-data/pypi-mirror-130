import sys
from setuptools import setup, find_packages

_requirements = [
    'sanic~=19.3.0',
    'sanic-envconfig',
    'sanic_brogz',
    'structlog',
    'sl_api_client',
    'marshmallow~=2.0',
    'sentry-sdk~=0.7.10'
]

if sys.version_info < (3, 7):
    _requirements.append('dataclasses')
    _requirements.append('aiocontextvars')

setup(
    name='microbase',
    version='0.5.5',
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
