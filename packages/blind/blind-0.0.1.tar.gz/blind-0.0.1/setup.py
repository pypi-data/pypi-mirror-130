import logging
from setuptools import setup, find_packages

alembic_files = [
    "../mlflow/store/db_migrations/alembic.ini",
    "../mlflow/temporary_db_migrations_for_pre_1_users/alembic.ini",
]

# See requirements.txt for additional color on requirements.
required_packages = [
    'click',
    'cloudpickle',
    'entrypoints',
    'gitpython',
    'pyyaml',
    'protobuf',
    'pytz',
    'requests',
    'Flask',
    'gunicorn',
    'cython',  # needed for numpy on m1?
    'numpy',
    'pandas',
    'querystring_parser',
    'sqlparse',
    'sqlalchemy'
]

setup(
    name="blind",
    version="0.0.1",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"blind": alembic_files},
    install_requires=required_packages,
    zip_safe=False,
    author="Jake",
    description="Blind Client: The easiest ML tracking library",
    long_description=open("README.rst").read(),  # TODO update this to README.md
    long_description_content_type="text/x-rst",
    license="Apache License 2.0",
    classifiers=["Intended Audience :: Developers", "Programming Language :: Python :: 3.8"],
    keywords="ml ai tracking mlops",
    url="http://google.com",
    python_requires=">=3.6",
)
