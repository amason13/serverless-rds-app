from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    description='Setting up our python package',
    author='Ash Mason',
    author_email='ashmason1389@gmail.com',
    packages=find_packages(include=['layers/helper_functions', 'layers.helper_functions.*']),
    install_requires=[
        'jupyter',
        'requests',
        'pandas',
        'numpy'
    ],
    extras_require={'plotting': ['matplotlib>=2.2.0', 'jupyter']}
)