from setuptools import setup

setup(
    name='parqser',
    version='1.0.12',
    description='Finally, a good parser',
    url='https://github.com/ARQtty/parqser',
    author='Ilya Shamov',
    author_email='ShamovIA@yandex.ru',
    license='MIT',
    packages=['parqser'],
    install_requires=['requests',
                      'lxml',
                      'loguru'],

    classifiers=[],
)
