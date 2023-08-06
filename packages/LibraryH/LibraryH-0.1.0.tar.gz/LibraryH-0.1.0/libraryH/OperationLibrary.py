##LIBRARY2

import importlib
import sys
import os

f = ''
wf = ''
lib = ''
def openLibrary(libPath):
   global f
   global lib
   try:
      f = open(libPath +'.py','r+')
      sys.path.append(os.path.realpath(__file__))
      PATH = libPath
      PATH = (PATH.split('\\'))[-1]
      lib = importlib.import_module(PATH)
   except:
      print("Can't open the library")

def getLibrary():
   try:
      functionList = []
      global f
      fl = f.readlines()
      for i in range(len(fl)):
         fl[i] = fl[i].strip()
      for i in fl:
         if 'def' in i:
            sl = i.split(' ')
            Name = sl[1]
            Name2 = Name.strip(':')
            functionList.append(Name2)
      return functionList
   except:
      print('Not found library')
         
def closeLibrary():
   global f
   try:
      f.close()
      f = ''
      wf = ''
      lib = ''
   except:
      print('Not open library')

def addToLibrary(text,lineBreak = True):
   global f
   f.seek(0,2)
   try:
      if lineBreak:
         f.write(text + '\n')
      elif lineBreak == False:
         f.write(text)
   except:
      print("Can't add to library")

def runFunction(functionName,*parameter):
   global lib
   try:
      function = 'lib.' + functionName + '('
      for i in parameter:
         function = function + pararmeter
      function = function + ')'
      eval(function)
   except:
      print("Can't run the function")














