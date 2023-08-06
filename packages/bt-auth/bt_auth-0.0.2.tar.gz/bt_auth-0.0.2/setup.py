from setuptools import setup, find_packages


setup(
    name='bt_auth',
    version='0.0.2',
    description='Authentication library for Bayes Technology.',
    author='Roman Glotov',
    install_requires=[
        'fastapi>=0.62.0',
        'pydantic>=1.7.3',
        'pyjwt>=1.7.1',
        'starlette>=0.13.6',
        'requests>=2.25.0'
    ],
    include_package_data=True,
    packages=find_packages(),
)
