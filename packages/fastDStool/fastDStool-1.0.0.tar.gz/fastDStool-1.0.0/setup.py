from setuptools import setup, find_packages

setup(name='fastDStool',

version='1.0.0',

description='find best parameters for data science at once',

author='yerin Hong',

author_email='yerinoneul@gmail.com',

url='https://github.com/yerinOneul',

license='MIT',

py_modules=['fastDStool'],

python_requires='>=3',

classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
      ],

install_requires=["pandas", "sklearn"],

packages=find_packages()

)