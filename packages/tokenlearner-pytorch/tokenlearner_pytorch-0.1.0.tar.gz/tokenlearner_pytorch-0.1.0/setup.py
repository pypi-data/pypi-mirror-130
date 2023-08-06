from setuptools import setup

setup(
    name='tokenlearner_pytorch',
    version='0.1.0',    
    description='Unofficial PyTorch implementation of TokenLearner by Google AI',
    url='https://github.com/rish-16/tokenlearner-pytorch',
    author='Rishabh Anand',
    author_email='mail.rishabh.anand@gmail.com',
    license='MIT',
    packages=['tokenlearner_pytorch'],
    install_requires=['torch'],
    
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
    ],
)