
from setuptools import find_namespace_packages, setup

VERSION = '0.0a1'

setup(
    name='fastapi-playground',
    version=VERSION,
    description='sticky-session-demo',
    author='XaiPient Inc',
    author_email='yang@xaipient.com',
    url='https://www.xaipient.com/',
    packages=find_namespace_packages(include=['./*']),
    install_requires=open('./requires.txt', 'r').read(),
    extras_require={
        'dev': [
            'pre-commit',
            'flake8',
            'jupyter',
            'PyYAML',
            'pytest',
            'autopep8'
        ]
    }
)
