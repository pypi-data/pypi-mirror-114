from setuptools import setup, find_packages, version
import setuptools

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Framework :: Django',
    'Framework :: Django :: 1.10',
    'Framework :: Django :: 1.9',
    'Framework :: Django :: 1.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Intended Audience :: Developers',
]

setup(
    name='gabibasiccalculator',
    version='0.0.1',
    description ='Very basic calculator',
    long_description='',
    url='',
    author='Gabriel Renom',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requieres=[''])