import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gs_sdk",
    version="2.0.0",
    author="duqiang",
    author_email="1427327705@qq.com",
    description="sdk调用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://forthink.xin:8889/dq/sdk.git",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires=">=3.9",
    install_requires=[
        'python-consul == 1.1.0',
        'paho-mqtt == 1.6.1',
        'pydantic == 1.8.2'
    ],
)