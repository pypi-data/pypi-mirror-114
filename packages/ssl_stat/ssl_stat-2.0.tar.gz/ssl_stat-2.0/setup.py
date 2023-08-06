#!/usr/bin/env python
 
from distutils.core import setup
from distutils.extension import Extension

setup(name="ssl_stat",
    version="2.0",
    python_requires='>=3',
    description="Python C Language Extension To Get SSL Certificate Information From URL",
    author="Ferdinand Silva",
    author_email="ferdinandsilva@ferdinandsilva.com",
    url="https://github.com/six519/ssl_stat",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
		'Programming Language :: C',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    download_url="https://github.com/six519/ssl_stat",
    ext_modules=[
        Extension("ssl_stat", 
            libraries = ['curl'], 
            sources = ["ssl_stat.c"]
        )
    ]
)