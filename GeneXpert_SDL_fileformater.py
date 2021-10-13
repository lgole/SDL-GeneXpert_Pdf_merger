# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 15:26:06 2021

@author: lgole
"""

# from tkinter import *
from tkinter import (filedialog,Tk,Label,StringVar,IntVar,
                     ttk)
#from csv import writer
#import xlsxwriter
#import re
#import random
#import string
import datetime
# import shutil
# import subprocess
import os
import base64
import time
# pdfcat -o output.pdf head.pdf content.pdf :6 7: tail.pdf -1
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import pdfplumber
import glob
import subprocess

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

class Book:
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
            print(i)
            with pdfplumber.open(eachpdf) as pdf:
                  for j,each in enumerate(pdf.pages):
                      print(j)
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
                              print('Pattern not detected in {} file!'.format(self.name))
                              self.SampleID.append('null')
                              self.PageID.append(str(j))
                      else:
                            if len(self.PageID)>0:
                              print('This page doesnt have SampleID')
                              self.PageID.append(str(int(self.PageID[j-1])+1))
                              self.SampleID.append(self.SampleID[j-1])
        self.N = len(set(self.SampleID))      
        # this break s all 
        # self.SampleID.sort()
                              
             
    def display(self):
        print('input type: {}'.format(self.name))
        print('File ID: {}'.format(self.FileID))
        print('Page ID: {}'.format(self.PageID))
        print('Sample ID: {}'.format(self.SampleID))
        print('Number of Sample: {}'.format(self.N))
        
    def IDmatching(self,BOOK2):
        print('pattern matching')
        self.matchdest = BOOK2.Filename
        self.IDX = [ self.SampleID.index(i) for i in BOOK2.SampleID]
        
        
    # def RerunCheck(self):
    #     print('check for reruns')
    #     for i,elem in enumerate(self.Listpdf):
    #         if elem[:-16] + 'A' in self.Listpdf:
    #             print(i,elem)
    #             self.IDX.append(i)
    #         elif elem[:-16] + 'AA' in self.Listpdf:
    #             self.IDX.append(i)
    #         elif elem[:-16] + 'AAA' in self.Listpdf:
    #              self.IDX.append(i)
                 
        


def explore():
    path = OUTPath.get()
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', path])     

def askfile(): 
    Pbar.start()
    # Fpath = filedialog.askopenfilenames(filetypes = (("csv files","*.csv"),("excel files","*.xls*")))
    # Fpath = filedialog.askopenfilenames(filetypes = (("pdf files","*.pdf"),))
    Fpath = filedialog.askdirectory()
    fileSDL.set(Fpath)
    if len(Fpath)>0:
        Opath =  Fpath + "/GX_mergedPDF" + datetime.datetime.strftime(datetime.datetime.today(),'%y%m%d')
        # os.makedirs(Opath,exist_ok=True)
    else:
        Opath = ''  
     
    
    OUTPath.set(Opath)                        
    print(OUTPath.get())            
    Ndetail.set(len(glob.glob(Fpath + "\*details.pdf")))
    NCurve.set(len(glob.glob(Fpath + "\*Curve.pdf")))
    print(Ndetail.get())
    lblB.configure(text='Folder contains {} detail & {} Primary Curves pdfs.'.format(Ndetail.get(),NCurve.get()) )
    lblC.configure(text='' )
   
    D = [] 
    C = [] 
    D = Book(Fpath,'details')
    C = Book(Fpath,'Curve')
    
    for row in tree.get_children():
        tree.delete(row)
    for row in tree2.get_children():
        tree2.delete(row)
    for row in tree3.get_children():
        tree3.delete(row)
    
    index = iid = 0
    # not sorted yet here 
    for row in (C.SampleID):
        print(row)
        #tmp = row.replace(" ", "")
        tree.insert("", index,iid,values= (row,))
        index = iid = index + 1  
        
    index = iid = 0
    for row in (D.SampleID):
        print(row)
        #tmp = row.replace(" ", "")
        tree3.insert("", index,iid,values= (row,))
        index = iid = index + 1          
        

def MERGEPDF():
##################TO REPLACE MERGE FUNCTION#############

    Fpath = fileSDL.get()
    lblC.configure(text='')
    window.update_idletasks()
     # Fpath = 'C://Users//lgole//Desktop//GX_PDF'
    D = [] 
    C = [] 
    D = Book(Fpath,'details')
    C = Book(Fpath,'Curve')
    for row in tree.get_children():
        tree.delete(row)
    for row in tree2.get_children():
        tree2.delete(row)
    for row in tree3.get_children():
        tree3.delete(row)

    index = iid = 0
    # sorted here during merging
    for row in sorted(C.SampleID):
        print('row = {}'.format(row))
        tree.insert("", index,iid,values= (row,), tags = (row,))
        index = iid = index + 1  
        
    index = iid = 0
    for row in sorted(D.SampleID):
        print(row)
        tree3.insert("", index,iid,values= (row,), tags = (row,))
        index = iid = index + 1          


    if D.N != C.N:
        if D.N==0:
            print('D = 0')
            lblC.configure(text='MERGING FAIL. Err01 please add missing Detail pdf.')
            Pbar.stop()
            Pbar["value"]=0
            return
        elif C.N==0:
            print('C = 0')
            lblC.configure(text='MERGING FAIL. Err02 please add missing Curves pdf.')
            Pbar.stop()
            Pbar["value"]=0
            return
        else:
            print('D != C')
            C1 = len(tree.get_children())
            C2 = len(tree3.get_children())
            
            for j,CSID in enumerate(C.SampleID):
               # this is where the SampleID matching happens
               IDXtmp = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j]]
               # check for A or AA 
               IDXtmpopts1 = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j][:-1]]
               IDXtmpopts2 = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j][:-2]]
               IDXtmpopts3 = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j][:-3]]
               IDXtmp = IDXtmp + IDXtmpopts1 + IDXtmpopts2 + IDXtmpopts3
            
            if len(IDXtmp) >= max(C1,C2):
                lblC.configure(text='Warn01 retests without curves will be merged in same Pdf.')
                #os.makedirs(OUTPath.get(),exist_ok=True)
            else:
                lblC.configure(text='Warn02 MissMatch number of SampleIDs. only subset merged')
            
            os.makedirs(OUTPath.get(),exist_ok=True)
    else:
           os.makedirs(OUTPath.get(),exist_ok=True)

    for row in tree2.get_children():
        tree2.delete(row)   
        
        
       
    for j,CSID in enumerate(C.SampleID):
        print ('j = {}'.format(j),C.SampleID[j])
      
        Pbar.stop()
        Pbar["value"]= (j/C.N*10)
        window.update_idletasks()
        time.sleep(0.1)
        
        # Open the Curvepdf: 
        CurveFile = open(C.Filename[j],'rb')    
        Curvepdf = PdfFileReader(CurveFile)
        # destination pdf:
        pdfWriter = PdfFileWriter()
     
        # this is where the SampleID matching happens
        IDXtmp = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j]]
        
        # check for A or AA 
        IDXtmpopts1 = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j][:-1]]
        IDXtmpopts2 = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j][:-2]]
        IDXtmpopts3 = [i for i,x in enumerate(D.SampleID) if x==C.SampleID[j][:-3]]
     
        IDXtmp = IDXtmp + IDXtmpopts1 + IDXtmpopts2 + IDXtmpopts3
        
        for i in IDXtmp:
            print('i={}'.format(i))
            # Open the DetailPdf: 
            detailFile = open(D.Filename[i],'rb')   
            detailpdf =  PdfFileReader(detailFile)
            # ISSUE HERE WITH MULTIPLE DETAIL PDF 
            pageObjd = detailpdf.getPage(int(D.PageID[i]))
            pdfWriter.addPage(pageObjd)
        
        pageObjc = Curvepdf.getPage(0)
        pdfWriter.addPage(pageObjc)
    
        
        # Now that you have copied all the pages in both the documents, write them into the a new document
        pdfOutputFile = open(OUTPath.get() + '//' + C.SampleID[j] + '_MergedFiles.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
     
        # Close all the files - Created as well as opened
        pdfOutputFile.close()
        CurveFile.close()
        detailFile.close()
        
        tree2.insert("", j,j, values='Merged')
     
        
    IDXoff = set(D.SampleID) - set(C.SampleID)
    for k in IDXoff:
        print('k={}'.format(k))
        #tree2.insert("", index= 'end' , iid = k, values= (k + ' Curve missing', ))
        tree2.insert("", index= -1 , iid = k, values= (k + ' Curve missing', ))
        
    IDXoff = set(C.SampleID) - set(D.SampleID)
    for k in IDXoff:
        print('k={}'.format(k))
        # tree2.insert("", index= 'end' , iid = k, values= (k + ' detail missing', ))
        tree2.insert("", index= -1 , iid = k, values= (k + ' detail missing', ))
     
 
   
    Lf  = glob.glob(OUTPath.get()  + '/*{}.pdf'.format('MergedFiles'))
    ames = [os.path.basename(x) for x in Lf]
    amesR = [x[:-16] for x in ames]
    # remove all As recursively
    for rec in range(0,4):
        amesR =  [x[:-1] if x[-1]=='A' else x[:] for x in amesR]
        
    # use dict to find duplicates and it s index and then merge pdfs_______
    my_dict = {}
    for (ind,elem) in enumerate(amesR):
        if elem in my_dict:
            my_dict[elem].append(ind)
        else:
            my_dict.update({elem:[ind]})

    for key,value in my_dict.items():
        # print(value)
        if len(value) > 1:
            MERGIDX = value
           # print (key,value) 
            merger = PdfFileMerger()
            for j,i in enumerate(MERGIDX):
                # print(i)
                T = open(Lf[i],'rb')
                merger.append(PdfFileReader(T))
                T.close()
            merger.write(Lf[MERGIDX[-1]][:-4] + '_Retest.pdf')
            merger.close()  
            for j,i in enumerate(MERGIDX):
                   if os.path.exists(Lf[i]):
                       os.remove(Lf[i])
                       
   
    Lf  = glob.glob(OUTPath.get()  + '/*{}*.pdf'.format('MergedFiles'))
    if len(Lf)==0:
         lblC.configure(text='Merging Failed! No pdf were created.')
         
         try:
             os.rmdir(OUTPath.get())
         except:
             print("Error while deleting {} .".format(OUTPath.get()))
        
         Pbar.stop()
         Pbar["value"]= 0 
    else:    
        lblC.configure(text= f'Merging Success! {len(Lf)} pdf{ " was" if len(Lf) == 1 else "s were"} created.')
        Pbar.stop()
        Pbar["value"]= 10 
   
    
  




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
window.geometry('507x320')


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
tree2.column("one", width=150, minwidth=150)
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
lblB.grid(column=0,row=2,columnspan = 3, sticky="W",padx=0)

btn = ttk.Button(window,text = '    Run      ',command = MERGEPDF)
btn.grid(column =1,row =5,sticky="EW",padx=0)

btn = ttk.Button(window,text = 'Open Dir',command = explore)
btn.grid(column =2,row =2,sticky="E",padx=10)


lblC = ttk.Label(window,text = '')
lblC.grid(column=0,row=3,columnspan = 3 ,sticky="W",padx=10)

Pbar = ttk.Progressbar(window, orient='horizontal',style="cyan.Horizontal.TProgressbar", mode='indeterminate',maximum=10)
Pbar.grid(column = 0, row = 5 , sticky = "W" , padx = 10)

lbl10 =Label(window,text = 'version 1.1 Sept 2021 LG',fg = 'gray')
lbl10.grid(column=2,row=5,sticky="E", padx = 0)
    
## Delete the tempfile
os.remove(tempFile)
window.mainloop()

