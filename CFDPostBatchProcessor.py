'''
This code is an easy way to process results in CFD-Post.

Currently the only supported outputs are tables.
What are other functions you want supported? Let me know.
Author: Arsha Mamoozadeh
Let me know of any issues or features you want added at https://github.com/Arsha72128/CFDPostBatchProcessor
'''

'''
For any additional debugging information open the 'cfdpost_error.log'. This is either found in the directory where this python script exists or where the results files are.
'''
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys
import time
import subprocess
import re

#This function checks if the input is == null to check if the user canceled upon file selection
def existenceChecker(fileArray):

    if fileArray =='':
        print('User canceled file selection')
        sys.exit()

#This function write the session file for exporting a table as a .csv file.
def tableCSEWriter(version,stateFile,tableName,filePath):
    
    filePath=re.sub('\.res$','.csv',filePath)
    sessionName="CFDPostBatchProcessor.cse"
    session=open(sessionName,"w")
    session.write("COMMAND FILE:\n")
    session.write(("CFX Post Version = "+version+"\n"))
    session.write("END \n \n")
    session.write(">readstate filename="+stateFile+", mode=overwrite,load=false, keepexpressions=true\n\n")
    session.write("TABLE:"+tableName+"\n")    
    session.write("Export Table Only = True\n")
    session.write("Table Export HTML Title =\n")
    session.write("Table Export HTML Caption Position = Bottom\n")
    session.write("Table Export HTML Caption =\n")
    session.write("Table Export HTML Border Width = 1\n")
    session.write("Table Export HTML Cell Padding = 5\n")
    session.write("Table Export HTML Cell Spacing = 1\n")
    session.write("Table Export Lines = All\n")
    session.write("Table Export Trailing Separators = True\n")
    session.write("Table Export Separator = Tab\n")
    session.write("END\n")
    session.write(">table save="+filePath+",name="+tableName)
    session.close()
    return sessionName

def main():
    #Beginning of Main
    root = tk.Tk()
    root.withdraw()
    
    #I have no idea what this line does. There is zero documentation on it. It has something to do with converting Python to tcl/tlk or something
    #If you remove this line everything breaks.¯\_(ツ)_/¯
    root.call('wm', 'attributes', '.', '-topmost', True)
    
    #Prompts user to select all results files.
    messagebox.showinfo("Prompt", "Please select the files that you would like to process.") 
    files = filedialog.askopenfilename(filetypes=[("ANSYS Results", ".res")],multiple=True) 
    existenceChecker(files)
    
    #This var variable is a tuple and thus is immutable, and it is a list of the files
    var = root.tk.splitlist(files)
    
    #filePaths is the exact same as var except now it is mutable
    filePaths = []
    for f in var:
        filePaths.append(f)
    
    #Prompts user to select state file for processing.
    messagebox.showinfo("Prompt","Please select your CFD-Post State file")
    stateFile=filedialog.askopenfilename(filetypes=[("ANSYS State File", ".cst")],multiple=False)
    existenceChecker(stateFile)
    
    #These arent checked for correctness so please put a correct value in. Potentially the error fie will check for this.
    version=input("Please enter which version of ANSYS CFD-Post you want to use. Example-17.2:  ")
    
    #If you enter a table name that does not exist, your ouput .csv will be empty
    tableName=input("Please enter the name of the table that you would like to export as a csv. Example-Table 1:  ")
    
    print("\nCFD-Post is about to start. This may take seconds to hours to complete\n")
    
    for i in filePaths:
        t1=time.time()
        session=tableCSEWriter(version,stateFile,tableName,i)
        CFDPostEXE=r'C:\Program Files\Ansys Inc\version\CFX\bin\cfdpost.exe'
        CFDPostEXE=re.sub('version',('v'+re.sub('\.','',version)),CFDPostEXE)
        try:
            subprocess.run([CFDPostEXE,'-batch',session,i])
        except:
            print("You either specified an ANSYS version that isnt installed on this computer, the Ansys CFD-Post path is incorrect, or I was unable to think of all the possible ways to break this code. The program will hard kill now.")
            sys.exit()
        t2=time.time()
        delta=t2-t1;
        print('Just finished {} in {:.2f} seconds.'.format(i,delta))
        
main()