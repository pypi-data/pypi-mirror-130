import setuptools
reqs = ['requests',
        'termcolor']
version = '2.7'

setuptools.setup(
    name='utils-s',
    version=version,
    author="Sal Faris",
    description="Utility functions",
    packages=setuptools.find_packages(),
    url='https://github.com/The-Sal/utils/',
    install_requires=reqs
)