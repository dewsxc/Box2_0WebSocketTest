from setuptools import setup, find_packages

setup(
    name='wbt',
    version='0.0.4',
    description='A websocket client maker, used to test capability of channel and server.',
    license='MIT',
    author='Chou, Yi-Tang',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['wbt = websocket_test.multi_client:main']
    },
    install_requires=['websocket-client']
)
