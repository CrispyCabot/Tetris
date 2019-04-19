# defaults: width - 420 height - 600 size - 30
# small: 
import os
width = 420 #multiple of size
height = 600 #multiple of size

size = 30

columns = width/size

PATH = os.path.abspath(__file__)
PATH = PATH[0:-9] #-10 to chop off config.py