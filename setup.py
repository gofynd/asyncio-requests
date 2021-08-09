"""Library Metadata Information."""

from setuptools import find_packages
from setuptools import setup

description = ('Any microservice will be able to use the “aio-requests” '
               'can make an async request(HTTP/SOAP/XML/FTP/redis) with the given payload to given address')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='aio-requests',
    version='0.1',
    author='Arjunsingh Yadav',
    author_email='arjunsinghyadav@fynd.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/fynd/ops-engg/libraries/aio-requests',
    packages=find_packages(
        exclude=('local_development', 'tests*', 'docs')),
    license='',
    install_requires=[
        'aiohttp==3.7.4.post0',
        'ujson==4.0.2',
        'requests==2.26.0',
        'zeep[async]==4.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
)
