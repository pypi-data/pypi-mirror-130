# **Namespace Distribution**
The purpose of the distribution is to demonstrate how to install namespace packages. Namespace packages do not require \_\_init__.py files and allow modules to be stored in separate directories but logically appear to look as if they are installed in one directory.

To understand Git Mark down files [click here](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

## 1. What does it do?
This python distribution installs two namespace packages called SampleDistribution_1/pkg1 and SampleDistribution_2/pkg1. The two pkg1 directories logically look like one directory even though physically they are separate. Notice how the module SampleDistribution_2/pkg1/mod2 imports mod3 with the code "from . import mod3". 

## 2. How is this accomplished.
The python search path, sys.path, is modified to include the directories ...\PythonXX\site-packages\SampleDistribution_1 and ...\PythonXX\site-packages\SampleDistribution_2. The logic is coded in SampleDistribution_1/pkg2/main so that the environment varible PYTHONPATH does not have to be manually changed.

## 3. What versions of python support namespace packages
python 3.3 and later

## 4. How to install
pip install NamespaceDistribution

## 5. How do you run it?
SDRun <br>

## 6. What is the output?
in mod1.py <br>
...\PythonXX\site-packages\SampleDistribution_1\pkg1\mod3.py <br>
...\PythonXX\site-packages\SampleDistribution_2\pkg1\mod2.py

## 7. Why is the program named SDRun. 
SDRun is short for Sample Distribution Run. Instead of running python -m SampleDistribution_1/pkg2/main, the console script entry point SDRun has been created for ease of use.
