# -*- coding: utf-8 -*-
import codecs

from setuptools import find_packages
from setuptools import setup

with codecs.open('README.rst', 'r', 'utf-8') as readme_f:
    README = readme_f.read()

with codecs.open('requirements.txt', 'r', 'utf-8') as requirements_f:
    REQUIREMENTS = [
        requirement.strip()
        for requirement
        in requirements_f.read().strip().split('\n')
    ]

with codecs.open('requirements-dev.txt', 'r', 'utf-8') as requirements_dev_f:
    REQUIREMENTS_DEV = [
        requirement.strip()
        for requirement
        in requirements_dev_f.read().strip().split('\n')[1:]
    ]

PACKAGES = find_packages(
    include=['django_changelist_inline'], exclude=['testing*', 'tests*'],
)

setup(
    name='django-changelist-inline',
    version='1.0.2',
    url='https://git.bthlabs.pl/tomekwojcik/django-changelist-inline',
    license='Other/Proprietary License',
    author='Tomek Wójcik',
    author_email='contact@bthlabs.pl',
    maintainer='BTHLabs',
    maintainer_email='contact@bthlabs.pl',
    description='Inline Changelists for Django',
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=PACKAGES,
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': REQUIREMENTS_DEV,
    },
    zip_safe=False,
    platforms='any',
)
