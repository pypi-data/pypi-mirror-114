from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'helpful-django=helpful_django.manage:main'
        ],
    }
)
