#!/usr/bin/env python
# coding: utf-8

# In[1]:


import setuptools

with open('C:/Users/Hindy/Desktop/Container_MissForest/README.md', 'r') as fh:
    long_descripion = fh.read()
    
setuptools.setup(
    name='MissForest', 
    version='1.1.1',
    author='Hindy Yuen', 
    author_email='hindy888@hotmail.com',
    license='MIT',
    description='nonparametric imputation on missing values.', 
    long_description=long_descripion, 
    long_description_content_type='text/markdown', 
    url='https://github.com/HindyDS/MissForest', 
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
],
    keywords='MissForest aims to provide the most convenient way for the data science community to perform nonparametric imputation on missing values by using machine learning models',
    package_dir={"":"MissForest"},
    packages=['MissForest'],
    python_requires='>=3.6'
)

