
# -*- coding: utf-8 -*-
"""
GeneXpert PDF MERGER SOURCE CODE 
PDFS MUST be named *details.pdf and *curve.pdf
Created on Sat Jun 19 15:26:06 2021

@author: lgole
"""

from tkinter import (filedialog,Tk,Label,StringVar,IntVar,
                     ttk)
import datetime
import os
import base64
import time
from PyPDF2 import PdfFileReader, PdfFileWriter
import pdfplumber
import glob
import subprocess

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')



class Book:
    """
    this class gather information about a list of pdf that ends with name.pdf keyword. 
    it also extract all Sample ID(*): information and corresponding page
    """
    def __init__(self,Fpath,name):
        self.name =  name 
        self.Listpdf  = glob.glob(Fpath + '/*{}.pdf'.format(name))

        self.SampleID = []    # creates a new empty list for each SID
        self.FileID = []    # creates a new empty list for each SID
        self.PageID = []    # creates a new empty list for each SID
        self.Filename = []
        self.IDX = []
        self.N = [] 
        pattern = 'Sample ID'
        self.N = len(set(self.SampleID))
        for i,eachpdf in enumerate(self.Listpdf):
            # print(i)
            with pdfplumber.open(eachpdf) as pdf:
                  for j,each in enumerate(pdf.pages):
                      # print(j)
                      self.FileID.append(str(i))
                      self.Filename.append(eachpdf)
                      tmp = each.extract_text()
                      if tmp.find(pattern)!=-1:
                            if tmp.split(pattern)[1][0] == '*':
                              self.SampleID.append((tmp.split('Sample ID*: '))[1].split('\n')[0])
                              self.PageID.append(str(j))
                            elif tmp.split(pattern)[1][0] == ':':
                              self.SampleID.append((tmp.split('Sample ID: '))[1].split('\n')[0])
                              self.PageID.append(str(j))
                            else:
                              # print('Pattern not detected in {} file!'.format(self.name))
                              self.SampleID.append('null')
                              self.PageID.append(str(j))
                      else:
                            if len(self.PageID)>0:
                              # print('This page doesnt have SampleID')
                              self.PageID.append(str(int(self.PageID[j-1])+1))
                              self.SampleID.append(self.SampleID[j-1])
        self.N = len(set(self.SampleID))      
                              
             
    def display(self):
        print('input type: {}'.format(self.name))
        print('File ID: {}'.format(self.FileID))
        print('Page ID: {}'.format(self.PageID))
        print('Sample ID: {}'.format(self.SampleID))
        print('Number of Sample: {}'.format(self.N))
#*****************************************************************************        


# to open file explorer
def explore():
    path = OUTPath.get()
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', path])    
        
# to open folder browser and select path and read all pdf inside + extra display things
def askfile(): 
    Pbar.start()
    Fpath = filedialog.askdirectory()
    fileSDL.set(Fpath)
    if len(Fpath)>0:
        Opath =  Fpath + "/GX_mergedPDF" + datetime.datetime.strftime(datetime.datetime.today(),'%y%m%d')
    else:
        Opath = ''  
     
    
    OUTPath.set(Opath)                        
    #print(OUTPath.get())            
    Ndetail.set(len(glob.glob(Fpath + "\*details.pdf")))
    NCurve.set(len(glob.glob(Fpath + "\*Curve.pdf")))
    #print(Ndetail.get())
  
    lblC.configure(text= '                                                                                                  ')
    lblB.configure(text= f'Reading {Ndetail.get()+NCurve.get()} pdfs... please wait...                                      ')
    window.update_idletasks()
    
      # Books class reads and extract all sample IDs from pdf and respetive pages  
    D = [] 
    C = [] 
    D = Book(Fpath,'details')
    C = Book(Fpath,'Curve')
    
    
    
    # UI Display things 
    lblB.configure(text=f'Folder contains {Ndetail.get()} detail & {NCurve.get()} curve pdf{" " if (NCurve.get()+Ndetail.get()) <= 1 else "s"}.' )
    for row in tree.get_children():
        tree.delete(row)
    for row in tree2.get_children():
        tree2.delete(row)
    for row in tree3.get_children():
        tree3.delete(row)
    index = iid = 0
    # not sorted yet here 
    for row in sorted(C.SampleID):
        print(row)
        tree.insert("", -1,iid,values= (row,))
        index = iid = index + 1  
    index = iid = 0
    for row in sorted(D.SampleID):
        print(row)
        tree3.insert("", -1,iid,values= (row,))
        index = iid = index + 1          

        

def MERGEPDF():
##################TO REPLACE MERGE FUNCTION#############

    Fpath = fileSDL.get()
    lblB.configure(text='')
    lblC.configure(text= 'Merging pdfs... please wait...                                                                              ')
    window.update_idletasks()
    
    # for testing/debugging
    #Fpath = 'C://Users//lgole//Desktop//2021 09 09_GX pdf//2021 09 09_GX pdf'
    D = [] 
    C = [] 
    D = Book(Fpath,'details')
    C = Book(Fpath,'Curve')
    for row in tree2.get_children():
        tree2.delete(row)
    
# recursively remove all "A"s at the end of sample IDs. for SID pattern matching
    list_curves_SampleID = C.SampleID
    list_details_SampleID = D.SampleID
    for rec in range(0,4):
        list_curves_SampleID =  [x[:-1] if x[-1]=='A' else x[:] for x in list_curves_SampleID]
        list_details_SampleID =  [x[:-1] if x[-1]=='A' else x[:] for x in list_details_SampleID]



# creating a list of unique ids on  which to match both books
    UniqueSet  = sorted(set(list_curves_SampleID).union(list_details_SampleID))
    # finding indexes that matches 
    INDEX_Cur = []
    INDEX_Det = []
    for j,SID in enumerate(UniqueSet):
       indices = [i for i, x in enumerate(list_curves_SampleID) if x == SID]
       indides = [i for i, x in enumerate(list_details_SampleID) if x == SID]
       INDEX_Cur.append(indices[:])
       INDEX_Det.append(indides[:])
 
   # MERGING ALL PDFS TOGETHER  in 1 go     
    if len(UniqueSet)>0:       
        os.makedirs(OUTPath.get(),exist_ok=True)
        Lf  = glob.glob(OUTPath.get()  + '/*{}*.pdf'.format(''))  
        if len(Lf)>0:
            lblB.configure(text= '')
            lblB.configure(text= f'Warning! output folder already contains {len(Lf)}  pdf{" " if len(Lf) == 1 else "s"}                             ')
            #  uncomment this part to make it delete output folder content each time.
            # for _,mfile in enumerate(Lf):
            #     if os.path.exists(mfile):
            #         try:
            #             os.remove(mfile)
            #         except:
            #               print("Error while deleting file ", mfile)
    else:
        lblC.configure(text= '')
        lblC.configure(text= 'List is empty! No pdf are created.                                       ')
        Pbar.stop()
        Pbar["value"]= 0
        return
    
    
    MissingPagesCounter = 0
    # opening matching detail and curve and erging into 1 pdf
    for each, SID in enumerate(UniqueSet):
         print (f'i={each} ID = {SID}')
         pdfWriter = PdfFileWriter()
         Pbar.stop()
         Pbar["value"]= (each/len(UniqueSet)*10)
         window.update_idletasks()
         time.sleep(0.1)
         if INDEX_Det[each] != []: 
             for d,elemd in enumerate(INDEX_Det[each]): 
                 # print(f'detail at {elemd}')
                 DetailFile = open(D.Filename[elemd],'rb')  
                 Detailpdf =  PdfFileReader(DetailFile)
                 pageObjd = Detailpdf.getPage(int(D.PageID[elemd]))
                 pdfWriter.addPage(pageObjd)
         if INDEX_Cur[each] != []:  
             for c,elemc in enumerate(INDEX_Cur[each]): 
                 # print(f'curve at {elemc} i = {c}')
                 CurveFile = open(C.Filename[elemc],'rb')  
                 Curvepdf =  PdfFileReader(CurveFile)
                 pageObjc = Curvepdf.getPage(int(C.PageID[elemc]))
                 pdfWriter.addPage(pageObjc)
                 
         # Now that we have copied all the pages in both the documents, write them into the a new document
         if INDEX_Cur[each] == []: 
             tree2.insert("", -1,each, values= f'{SID}_No_curves')
             MissingPagesCounter += 1
             L = [D.SampleID[i] for i in INDEX_Det[each]]
             pdfOutputFile = open(OUTPath.get() + '//' + max(L,key=len) + '_No_Curves.pdf', 'wb')
         elif INDEX_Det[each] == []: 
             tree2.insert("", -1,each, values= f'{SID}_No_details')
             L = [C.SampleID[i] for i in INDEX_Cur[each]]
             MissingPagesCounter +=  1
             pdfOutputFile = open(OUTPath.get() + '//' + max(L,key=len) + '_No_Details.pdf', 'wb')
         else: 
             tree2.insert("", -1,each, values= SID + '_Merged')
             L = [C.SampleID[i] for i in INDEX_Cur[each]]
             pdfOutputFile = open(OUTPath.get() + '//' + max(L,key=len) + '_MergedFiles.pdf', 'wb')
       
         pdfWriter.write(pdfOutputFile)
         # Close all the files - Created as well as opened
         pdfOutputFile.close()
         try: 
             DetailFile.close()
         except:
            print('No detail')
        
         try: 
             CurveFile.close()
         except:
            print('No curve')
    
    
    Lf  = glob.glob(OUTPath.get()  + '/*{}*.pdf'.format(''))   
    if   MissingPagesCounter == 0:
        lblC.configure(text= '')
        lblC.configure(text= f'Merging Success! {len(Lf)} pdf{ " was" if len(Lf) == 1 else "s were"} created.                                         ')
    else: 
        lblC.configure(text= '')
        lblC.configure(text= f'Missing {MissingPagesCounter} page{"s!"  if (len(Lf)) > 1 else "!"}  {len(Lf)} pdf{ " was" if (len(Lf)) == 1 else "s were"} created.        ')
    Pbar.stop()
    Pbar["value"]= 10 
    tmp = "GX_mergedPDF" + datetime.datetime.strftime(datetime.datetime.today(),'%y%m%d')
    lblB.configure(text= '')
    lblB.configure(text= f'Click here to access merged pdf{" " if len(Lf) == 1 else "s"} in {tmp}           -->       ')

# ****************************************************************************





# *APPLICATION UI**************************************************************
icon = b'AAABAAEAMDAAAAEAGACoHAAAFgAAACgAAAAwAAAAYAAAAAEAGAAAAAAAgBwAAAAAAAAAAAAAAAAAAAAAAAD///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+LRDr///////+LRDr///////////////////////+LRDqLRDqLRDr////////t4uCLRDr///////+LRDr///////+WVkz///////+LRDr///+LRDr///////////////////////////////////////////////////////////////////////////////////+LRDqLRDqyg3z////////u4+Ly6+n////////////59vWLRDr////////r396LRDr////////49POPS0GVVUvIpqH///////+LRDqLRDr///////////////////////////////////////////////////////////////////////////////////////+LRDq5j4n///////////+fZVyQTEL////////Zwr6LRDr////////////r396LRDr///////////+LRDqjbGT///////////+bXVWLRDr8+vr////////////////////////////////////////////////////////////////////////////////////w5+WLRDr////////9+/vs4N/i0M369/f///+LRDqLRDqLRDr////Lq6eLRDqLRDqLRDr////////fzMmLRDr///////////+QTEKNRz3+/f3////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+/f3//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7//v7+/f3///////////////////////////////////////////////////////////////////////////////+HQDaCNiuCNiuCNyuCNiuCNyuBNiuBNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNyuCNiuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuja2P///////////////////////////////////////////////////////////////////////////////+NRz2BNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuBNiuCNiuBNiuCNiuCNyuCNiuCNiuCNiuCNiuBNiuCNiuCNiuBNiuCNyqncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuCNiuCNyuCNiuCNiuBNiuCNiuCNiuBNiuCNiuBNiuCNiuCNiuBNiuCNiuBNiuCNiuCNiuCNyuBNiuCNiuBNiuCNiuCNiuCNyuncWn///////////////////////////////////////////////////////////////////////////////+IQDaNR0SLRUF6KiGCNiqCNiuCNiuBNiuCNiuCNiuCNiuCNiuBNSp6KiF8KyZ6KiJ+MCSCNiuCNiuCNiuCNiuDNyuCNiuCNiuCNiuCNiuCNiuncWn////////////////////////////////////////////////////////////////////////////////58vL////////////Mqqp5KSCCNiuCNiuBNiuCNiuCNit9LyTRsbL////////////69fazgYJ6KiCCNyuCNiuCNyuCNiuCNiuCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////////////////////////////+LQj+CNyuCNiuCNiuCNirHoaL////////////////////9+/v///+cXVyBNSmBNiuCNiuCNiuCNyuCNiuCNiuncWn////////////////////////////////////////////////////////////////////////////////////07Ox3JhyCNTDhzM3///////+nb26BNSmCNit8LCL///////////99LSiBNSmBNSl9LyOBMy7bwsLIpKWANCeCNiuCNiuCNiuCNiuCNyuncWn////////////////////////////////////////////////////////////////////////////////l0dH///98LCWCNiuANCiMREH///////+9kZGAMyh6KiH///////////+BNSmCNiuBNiuCNiuCNiuBNSmRTUuiaGeCNiuCNiuCNiuCNiuBNiuncWn///////////////////////////////////////////////////////////////////////////////+QTUn////38fF6KiCBNiuCNyt6KR/k0NH////IpKR4Jhz///////////+CNiqCNiuCNyqCNiuCNiuBNiuCNiuBNSqCNiuCNiuCNiuCNyuCNiuncWn///////////////////////////////////////////////////////////////////////////////+LRjrm09P////t4OF7LCGBNiuCNit/MiW9kJH////Kqqrs397///////+BNiqBNiuCNiuCNiuCNiuCNyuCNyqCNiuCNiuBNiuCNiuCNiuCNiuncmn///////////////////////////////////////////////////////////////////////////////+NRz16KSH////////u4uJ6KiCCNiuCNiuBNimlbGv///////////////9+MCWCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuCNyuCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNyuRS0j////////59PR6KSKCNyuCNiuCNiqdYF////////////96KiOCNiuCNiuBNiuCNiuCNiuCNyuBNiuBNyqCNiuCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNyqvfHz///////////+LQ0CCNyuCNiuCNiuiZ2X///////+kamiBNyuCNiuCNiuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNyuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuBNiuBNSm9kJH///////////+kaml+MSaCNiuCNyqmb2/////9+/t8LCGCNiuCNiuCNiuCNiuCNiuCNyqCNiuCNyuCNiuCNiqCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuCNiuBNiivfn3////////////q29x4Jx+CNyuBNirFn57///+sd3eCNyqCNiuBNiuCNiuCNiuCNiuCNyuCNiuCNiuCNiuCNiumcWn///////////////////////////////////////////////////////////////////////////////+NRz2CNyuCNiuCNiuCNiuCNyqVUU////////////////+VU1GCNip/MiXm1NX///+aWliDNyuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+MRz2CNiuCNiuCNiuBNiuCNiuCNyt6KiTo2dn////////////Io6SBNS98LCj///////9/MiyCNyuBNiuCNiuCNiuCNiuCNiuCNiuCNyuBNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuCNiuCNiuCNiuCNiuCNiuAMyd+LymvfHz////////IpKSLQz7FnZ3///////+OR0WCNyuCNiuCNiuCNiuCNiuCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNyuCNyuBNSmBNimCNiuCNit/MSXTtLX////27+9/MiaCNiuCNiuCNiuCNyuCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNyuCNiuCNyuCNiuCNiuCNiuCNiuBNSiBNC99LiWCNiuCNiuCNiuCNiuCNiuBNiuCNiuCNiuncmn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuBNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuBNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuCNiuCNiuCNyuCNiuCNiuCNiuCNiuCNiuCNyuCNiuBNiuCNiuCNiuCNiuDNimCNyqCNiuBNiuFNyeENyeCNiuCNiuCNiuBNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuCNiuCNiuCNiuCNyuCNiuBNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNylHJ6lYK4mGNyOCNitOKZ1QK5uBNiuCNiuBNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNyuCNiuCNyuCNiuCNiuBNiuCNyuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNytrL2MuJNkoIeaMOB0qIuJEJ62CNiqCNiqCNyuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuBNiuCNiuCNyuCNiuBNiuBNiuCNiuCNiuCNyuCNiuCNiuCNiuCNiuCNiuFNyQmIuqDNDYgIPYmI+09Jb2CNymCNiuBNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuBNTMsIt9tMWBGJ6soI+mGNimCNyuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+MRz2CNiuCNiuCNiuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuBNiuBNiuCNit8MzxuL100JM89Jb6KOB0lIeweIfphLHiGOCSCNiuncmn///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNyuCNiuCNiuCNiuCNiuCNyuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNyuFNyQnIekhIvgiIvQsI+BnLm4iIfOUOg06JcMsI+CHNyimcWn///////////////////////////////////////////////////////////////////////////////+NRz2BNiuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuFNyWIOCGFNitVK49gLHsnIukjIfAsIt01JMkhIvaSa5v///////////////////////////////////////////////////////////////////////////////+NRz2CNiuCNiuBNiuCNiuCNiuCNyuCNiuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuJOCAkIew5JcWKNyKINyVyMVRLKaJ7Z8X///////////////////////////////////////////////////////////////////////////////+NRz2BNiuCNiuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuBNiuCNiuBNitUKpJCJrB6NEKCNiuCNyuCNiqncmj///////////////////////////////////////////////////////////////////////////////+NRz2CNiv+/f3//////v6CNiuCNiveysf////////+/f3s4d+CNiuCNiv59fT////////////OsayBNyuCNiuINyEgIfpnL2qBNiuCNiuCNyuncmn///////////////////////////////////////////////////////////////////////////////+NRzzOsKyCNiuIQDbHpaD8+vqCNiveysf8+vrFoZzDnpn48/Ps4N+CNiv59fTt4uCwf3iwf3icYFeCNiuCNiuBNipaK4JlL22CNyuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNivUurb07ez9/Pz+/f2CNiveysf8+vrCnJeCNivfzMn59fSCNiv59fTq3tyCNiuCNiuCNiuCNiuCNiuCNiuCNiqBNiqCNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz3Xv7z+/f338vHl1dOCNiuIQDbeysf8+vrCnJeCNyvj0c/59fSCNiv59fTq3tyCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuBNiuCNiuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz3Zwr77+fiCNiuCNivcx8SCNiveysf8+vrNr6vYwLz8+vro2tiCNiv59fTq3tyCNiuCNiuCNiuCNiuCNiuCNyuCNiuCNiuBNiuCNyuCNiuncWn///////////////////////////////////////////////////////////////////////////////+NRz2CNivl1tT7+Pj8+fmCNiuCNivZwr/59fT59fT17+7aw8CCNiuCNivz6+rl1dOCNiuCNiuCNiuCNiuCNiuCNiuCNyqCNiuCNiuCNyuBNiumcWn///////////////////////////////////////////////////////////////////////////////+KRDqCNiuCNiuBNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNiuCNyuCNiuCNiuBNiuCNyuCNyuCNiuCNiuCNiuCNiuCNiuCNiuCNiulb2f///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='

icondata= base64.b64decode(icon)
## The temp file is icon.ico
tempFile= "icon.ico"
iconfile= open(tempFile,"wb")
## Extract the icon
iconfile.write(icondata)
iconfile.close()

window = Tk()
s = ttk.Style()
s.theme_use('winnative')
s.configure("red.Horizontal.TProgressbar", foreground='blue', background='black')
# window.wm_iconbitmap(r'astar_logo.ico')
window.wm_iconbitmap(tempFile)
window.title("GeneXpert Report Automerge")
window.geometry('557x320')


fileSDL = StringVar()
fileSDL.set("")

OUTPath = StringVar()
Ndetail = IntVar()
NCurve = IntVar()
NCurve.set(0)
Ndetail.set(0)
Npages = IntVar()


tree = ttk.Treeview(window)
tree.grid(column = 0, row = 4 , sticky = "W" , padx = 10)
tree["columns"] = ["one"]
tree.column("#0", width=0, minwidth=0)
tree.column("one", width=150, minwidth=150)
tree.heading("one", text = 'Sample IDs Curve PDF')

tree2 = ttk.Treeview(window)
tree2.grid(column = 1, row = 4 , sticky = "W" , padx = 0)
tree2["columns"] = ["one"]
tree2.column("#0", width=0, minwidth=0)
tree2.column("one", width=200, minwidth=150)
tree2.heading("one", text = 'Status')

tree3 = ttk.Treeview(window)
tree3.grid(column = 2, row = 4 , sticky = "W" , padx = 0)
tree3["columns"] = ["one"]
tree3.column("#0", width=0, minwidth=0)
tree3.column("one", width=150, minwidth=150)
tree3.heading("one", text = 'Sample IDs Details PDF')


def Myview(*args):
    """ scroll both listboxes together """
    tree.yview(*args)
    tree2.yview(*args)
    tree3.yview(*args)
    
sb = ttk.Scrollbar(window, orient='vertical', command=Myview)
tree.config(yscrollcommand=sb.set)
tree2.config(yscrollcommand=sb.set)
tree3.config(yscrollcommand=sb.set)


sb.grid(row=4, column=3, sticky='ns')

btn1 = ttk.Button(window,text = 'Select input directory',command = askfile)
btn1.grid(column =0,row =1,sticky="W",padx=10)

INPUT_PATH = ttk.Entry(window,textvariable= fileSDL,width=50 )
INPUT_PATH.grid(column =1,row =1,columnspan=2,sticky="W")

lblB = ttk.Label(window,text = '',wraplength=500)
lblB.grid(column=0,row=2,columnspan = 3, sticky="W",padx=10)

btn = ttk.Button(window,text = '    Run      ',command = MERGEPDF)
btn.grid(column =1,row =5,sticky="EW",padx=0)

btn = ttk.Button(window,text = 'Open Dir',command = explore)
btn.grid(column =2,row =2,sticky="E",padx=10)


lblC = ttk.Label(window,text = '')
lblC.grid(column=0,row=3,columnspan = 3 ,sticky="W",padx=10)

Pbar = ttk.Progressbar(window, orient='horizontal',style="cyan.Horizontal.TProgressbar", mode='indeterminate',maximum=10)
Pbar.grid(column = 0, row = 5 , sticky = "W" , padx = 10)

lbl10 =Label(window,text = 'version 1.2 Oct 2021 LG',fg = 'gray')
lbl10.grid(column=2,row=5,sticky="E", padx = 0)
    
## Delete the tempfile
os.remove(tempFile)
window.mainloop()


