from setuptools import setup

setup(
    name='mchatx_python',
    version='0.0.1',
    packages=['mchatx_python'],
    author='Michael Nolan',
    author_email='celegans25@gmail.com',
    install_requires = ['requests'],
    entry_points={
        'console_scripts': [
            'download_tl = mchatx_python.download_tl:main'
        ]
    },
)
