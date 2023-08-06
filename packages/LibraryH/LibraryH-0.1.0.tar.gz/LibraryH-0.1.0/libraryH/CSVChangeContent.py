##LIBRARY 5

csvF = ''
def PATH(Path):
   global csvF
   try:
      csvF = open(Path + '.csv','r+')
   except:
      print("Can't open CSV file")

def READ():
   global csvF
   try:
      return [csvF.read(),csvF.readlines()]
   except:
      print("Can't read CSV file")

def CLOSECSV():
   global csvF
   try:
      csvF.close()
   except:
      print('Not any CSV file open')

def ADDTOCSV(text,lineBreak = True):
   global csvF
   try:
      if lineBreak:
         csvF.write(text + '\n')
      if lineBreak == False:
         csvF.write(text)
   except:
      print("Can't add to CSV file")








      
