## Features  

* Run a matlab script file through a python script  

## Installation  
Prerequisits:  
	* Python 3.8 <=  
	* MATLAB (any version)  
You can then install by running the following pip command:  
> pip install mat_wrapper  

## Usage  

### Initialization  
> import matlab_wrapper_python  
> wrapper = mat_wrapper.wrapper()

### Basic Functionality  
> wrapper.addToPath("directory of files being used") #Can include as many as you want  
> wrapper.wrap("matlab file name")  

## Acknowledgments

This project uses the [Python MATLAB Engine](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)  
MATLAB is developed and produced by [MathWorks](https://www.mathworks.com/)  

## Liscense  

Liscensed under GNU General Public License v3 or later  