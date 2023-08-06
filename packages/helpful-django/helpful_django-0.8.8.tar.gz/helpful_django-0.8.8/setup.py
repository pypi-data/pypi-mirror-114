from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'helpful-django=manage:main'
        ],
    }
)
