"""Library Metadata Information."""

from setuptools import find_packages
from setuptools import setup

description = ('Any microservice will be able to use the “aio_requests” '
               'can make an async request(HTTP/SOAP/XML/FTP/redis) with the given payload to given address')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='fdk_client_python',
    version='v0.1rc1',
    author='Arjunsingh Yadav',
    author_email='arjunsinghyadav@fynd.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/fynd/ops-engg/libraries/aio-requests/-/tree/temp-package',
    packages=find_packages(
        exclude=('local_development', 'tests*', 'docs')),
    license='',
    install_requires=[
        "aiohttp==3.7.3",
        "async-timeout==3.0.1",
        "attrs==21.2.0",
        "backcall==0.2.0",
        "chardet==3.0.4",
        "decorator==5.1.0",
        "idna==3.2",
        "ipython==7.28.0",
        "jedi==0.18.0",
        "marshmallow==3.12.2",
        "matplotlib-inline==0.1.3",
        "multidict==5.2.0",
        "parso==0.8.2",
        "pexpect==4.8.0",
        "pickleshare==0.7.5",
        "prompt-toolkit==3.0.21",
        "ptyprocess==0.7.0",
        "Pygments==2.10.0",
        "pytz==2021.3",
        "traitlets==5.1.1",
        "typing-extensions==3.10.0.2",
        "ujson==4.0.1",
        "wcwidth==0.2.5",
        "yarl==1.6.3"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ],
)
