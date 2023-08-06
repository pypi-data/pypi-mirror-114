from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='anarion',
    version='0.0.2',
    description='Stock Analysis',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='https://github.com/nabhat/anarion',
    author='nabhat',
    author_email='angman507@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='anarion',
    packages=find_packages(),
    install_requires=['numpy', 'pandas']
)
