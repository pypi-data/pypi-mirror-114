"""
Flask-Logging
-------------
 
Log every request to specific view
"""
from setuptools import setup
 
setup(
    name='Flask-Auth-User',
    version='1.0.2',
    url='http://iotwonderful.com',
    license='BSD',
    author='zhangchi, lisichen',

    description='auth user',
    long_description=__doc__,
    packages=['flask_auth_user'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask','PyJWT','aliyun_python_sdk_core', 'Cython'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)