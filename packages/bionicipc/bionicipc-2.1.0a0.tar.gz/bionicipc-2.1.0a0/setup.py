import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="bionicipc",
    version="2.1.0a0",
    author="h3xcode",
    author_email="me@h3xco.de",
    description="Pretty simple RPC-like IPC proto",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/h3xcode/bionic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=["orjson"]
)
