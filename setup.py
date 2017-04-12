from setuptools import setup

setup(
    name='recipe-garden',
    packages=['recipe_garden'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_restful',
        'sqlalchemy',
        'pymysql'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ]
)
