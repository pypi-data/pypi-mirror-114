
#Imports the matlab engine
import matlab.engine
import os, sys 

#creates an instance of the matlab engine
eng = matlab.engine.start_matlab()
#defines the wrapper class
class wrapper:
    #lets you add to the path of the matlab wrapper
    def addToPath(self, folder):
        eng.addpath(folder)
        os.chdir(folder)
        print("added " + folder + " to the path")

    #this wraps through python using the functions name
    def wrap(self, func):
        inputs = "nargout=0"
        try:
            evald = eval("eng" + "." + func + "(" + inputs + ")")
        except:
            evald ="The function or inputs were invalid, try again!"

