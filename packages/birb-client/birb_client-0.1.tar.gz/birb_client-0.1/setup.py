from setuptools import setup, find_packages

setup(
    name='birb_client',
    version='0.1',
    # py_modules=['birb_flask_auth0'],
    package_dir={'birb_client': 'birb_client'},
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
)