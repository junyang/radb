from setuptools import setup, find_packages
from codecs import open
import os
import configparser

def get_path(fname):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), fname)

def parse_setup_config(fname):
    configfile = get_path(fname)
    config = configparser.ConfigParser()
    config.read(configfile)
    return { key.replace('setup.', '', 1): val
             for key, val in config.items(configparser.DEFAULTSECT)
             if key.startswith('setup.') }
setup_config = parse_setup_config('radb/sys.ini')

def read(fname):
    return open(get_path(fname), encoding='utf-8').read()

setup(
    **setup_config,
    long_description=read('README.rst'),
    license='MIT',
    keywords='database relational algebra',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Interpreters',
        'Programming Language :: Python :: 3',
    ],

    packages=find_packages(),
    install_requires=['SQLAlchemy>=2.0', 'antlr4-python3-runtime>=4.12'],
    python_requires='>=3.5',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'radb=radb.ra:main',
        ],
    },

)
