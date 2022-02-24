"""Library Metadata Information."""

from setuptools import find_packages
from setuptools import setup

description = ('Any microservice will be able to use the “aio_requests” '
               'can make an async request(HTTP/SOAP/XML/FTP/redis) '
               'with the given payload to given address')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='asyncio-requests',
    version='0.1rc1',
    author='Arjunsingh Yadav',
    author_email='arjunsinghyadav@fynd.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/fynd/ops-engg/libraries/aio-requests',
    download_url='https://github.com/gofynd/aio-requests/archive/refs/tags/v0.1rc1.tar.gz',
    packages=find_packages(
        exclude=('local_development', 'tests*', 'docs')),
    license='MIT',
    install_requires=[
        'aiohttp==3.8.1',
        'ujson==5.1.0',
        'requests==2.27.1',
        'zeep[async]==4.0.0',
        'aioboto3==9.3.1',
        'aiofiles==0.8.0',
        'pyfailsafe==0.6.0',
        'pytz==2021.3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
)
