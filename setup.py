import os
import re
from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)

setup(
    name="django-tables2-extras",
    version=get_version('tables2_extras'),
    description="Additional views and mixins for using django-tables2 and django-tables2-reports.",
    long_description="Additional views and mixins for using django-tables2 and django-tables2-reports.",
    keywords="django, views, mixins, tables",
    author="Jerick Don San Juan <jerick@icannhas.com>",
    author_email="jerick@icannhas.com",
    url="https://github.com/jericksanjuan/django-tables2-extras",
    license="",
    packages=["tables2_extras"],
    zip_safe=False,
    install_requires=[
        "Django >= 1.4.1",
        "django-extra-views >= 0.6.4",
        "django-vanilla-views >= 1.0.2",
        "django-tables2 >= 0.15.0",
        "django_tables2_reports"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
