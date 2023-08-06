import sys

def goto(string):
    file=sys.argv[0]
    f=open(file,"r")
    fileread=f.read()
    output=fileread.index(string)
    f.seek(output)
    fileread=f.read()
    x=exec(fileread)
    
        
