'''
Created on Sep 7, 2013

@author: alice
'''
from setuptools import setup

""" setup SDK """
setup(name='aedsdk',
      version='0.1',
      description='Abstract Experiment Designer\'s SDK',
      url='http://github.com/codebunny/aed',
      author='Alice Q. Wong',
      author_email='alice@valour.me',
      license='MIT',
      packages=['aedsdk'],
      install_requires=['datetime'],
      zip_safe=False)
