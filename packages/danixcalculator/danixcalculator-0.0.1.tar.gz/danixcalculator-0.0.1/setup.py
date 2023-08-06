from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='danixcalculator',
    version='0.0.1',
    description='Basic Calculator 2 numbers',
    author='Danix25',
    license='MIT',
    packages=find_packages(),
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    classifiers=classifiers,
    _install_requires=['']
)