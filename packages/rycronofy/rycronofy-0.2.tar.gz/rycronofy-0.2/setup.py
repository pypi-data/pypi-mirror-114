from setuptools import setup, find_packages

setup(
    name='rycronofy',
    version='0.2',
    author='Ryan Mohta',
    author_email='ryanmohta@gmail.com',
    description='A basic Python wrapper over the Cronofy calendar scheduling library',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'cronofy']
)
