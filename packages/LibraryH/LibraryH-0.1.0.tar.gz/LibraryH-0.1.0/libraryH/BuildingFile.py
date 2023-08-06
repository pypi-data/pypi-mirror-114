#LIBRARY1

def NewLibrary(libPath,encoding = 'UTF-8'):
   try:
      f = open(libPath + '.py','w',encoding = encoding)
      f.close()
   except:
      print("Can't building library")

def NewCSV(csvPath,encoding = 'UTF-8'):
   try:
      f = open(csvPath + '.csv','w',encoding = encoding)
      f.close()
   except:
      print("Can't building CSV file")

def NewFile(filePath,nameSuffix = '.txt',encoding = 'UTF-8'):
   try:
      f = open(filePath + nameSuffix,encoding = encoding)
      f.close()
   except:
      print("Can't building file")
