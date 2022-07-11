"""Library Metadata Information."""

from setuptools import find_packages
from setuptools import setup

description = ('Any microservice will be able to use the “asyncio_requests” '
               'can make an async request(HTTP/SOAP/XML/FTP/redis) '
               'with the given payload to given address')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='asyncio-requests',
    version='2.4',
    author='Arjunsingh Yadav, Manish Magnani, Devesh Ratthour',
    author_email='arjunsinghyadav@fynd.com, manishmagnani@gofynd.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gofynd/asyncio-requests',
    download_url='https://github.com/gofynd/aio-requests/archive/refs/tags/v2.4.tar.gz',  # noqa E251
    packages=find_packages(
        exclude=('local_development', 'tests*', 'docs')),
    license='MIT',
    install_requires=[
        'aiohttp==3.7.4',
        'ujson==5.4.0',
        'requests==2.25.0',
        'zeep[async]==4.0.0',
        'aioboto3==9.6.0',
        'aiofiles==0.8.0',
        'pyfailsafe==0.5.0',
        'pytz==2022.1',
        'aioftp==0.21.2'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
)
