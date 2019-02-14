import os
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

here = os.path.abspath( os.path.dirname( __file__ ) )
README = open(os.path.join( here, 'README.rst' ) ).read()

setup(
    name='tetrapod',
    version='1.5',
    description='',
    long_description=README,
    license='',
    author='',
    author_email='',
    packages=find_packages(),
    install_requires=[ 'xmltodict>=0.11.0', 'pusher==2.1.2', ],
    dependency_links=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ] )
