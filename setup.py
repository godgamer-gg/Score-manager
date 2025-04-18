from setuptools import setup, find_packages

setup(
    name="score-manager",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.21.0",
        "passlib>=1.7.4",
        "bcrypt>=4.0.1",
        "python-jose>=3.3.0",
        "python-dotenv>=1.0.0",
        "jsonpickle>=3.0.1",
        "sortedcontainers>=2.4.0",
        "requests>=2.28.0",
    ],
)
