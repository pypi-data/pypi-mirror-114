## Features  

* Run a matlab script file through a python script  

## Installation  
Requirements:  
	* Python 3.8  
	* MATLAB (any version)  
## IMPORTANT::INSTALL THE MATLAB ENGINE FOR PYTHON: 

![image](https://user-images.githubusercontent.com/55168674/127377377-e65c80d9-249c-4405-b11d-db5ec97b1ea1.png)  
* Picture from [Install MATLAB Engine Python](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html#responsive_offcanvas)  

You can then install by running the following pip command:  
> pip install mat_wrap  

## Usage  

### Initialization  
> from mat_wrap import mat_wrap  
> wrapper = mat_wrap.wrapper()

### Basic Functionality  
> wrapper.addToPath("directory of files being used") #Can include as many as you want  
> wrapper.wrap("matlab file name")  

## Acknowledgments

This project uses the [Python MATLAB Engine](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)  
MATLAB is developed and produced by [MathWorks](https://www.mathworks.com/)  

## Liscense  

Liscensed under GNU General Public License v3 or later  

## Contact  

If you have any questions or concerns, please feel free to email: sbeer3@uwyo.edu
