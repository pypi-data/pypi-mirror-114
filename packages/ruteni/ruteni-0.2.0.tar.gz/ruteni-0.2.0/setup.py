import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruteni",
    version="0.2.0",
    author="Johnny Accot",
    description="Thin layer over Starlette",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["ruteni"],
    install_requires=[
        "sqlalchemy>=1.3.22,<1.4.0",
        "itsdangerous>=1.1.0,<2.0.0",
        "aiofiles>=0.6.0,<0.7.0",
        "python-socketio>=5.0.3,<6.0.0",
        "httpx>=0.16.1,<0.17.0",
        "starlette>=0.14.1,<0.15.0",
        "databases>=0.4.1,<0.5.0",
        "authlib>=0.15.4,<0.16.0",
        "sqlalchemy-utils>=0.36.8,<0.37.0",
    ],
)
