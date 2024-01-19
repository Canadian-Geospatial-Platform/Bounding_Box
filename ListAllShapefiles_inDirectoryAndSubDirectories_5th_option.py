#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      seagles
#
# Created:     11-01-2024
# Copyright:   (c) seagles 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os

path = os.getcwd()

print path + " = PATH"

if __name__ == "__main__":
    List_Files = []
    for (root,dirs,files) in os.walk(path, topdown=True):
        print (root)
        #print (dirs)
        #print (files)
        files = os.listdir(root)
        files = [f for f in files if f.lower().endswith('.shp')]
        if len(files)==0:
            print("there are no files ending with .shp in your folder")
        else:
            print('There are {} shapefiles in your folder'.format(len(files)))
        for f in files:
            print root + "\\" + f
            List_Files.append(root + "\\" + f)
        print ('--------------------------------')
print List_Files
print ('There are {} shapefiles in your list'.format(len(List_Files)))
