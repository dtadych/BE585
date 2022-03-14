# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 2019
BE485 
@author: Armando Barreto
VIPLab Convolution
"""

import numpy as np

class SpecConvolution:

    def __init__(self):
        self.a=2019
        self.sensorname=''
        self.resmeter=1
        self.bands_reset()
        
        
    def bands_reset(self):
        self.bands=[]
        self.bRED=[]
        self.bGREEN=[]
        self.bBLUE=[]
        self.bNIR=[]
        self.hasdata=False
        self.RSRweight=[]         
        
    def bands_checkdata(self):
        nred=len(self.bRED)
        ngreen=len(self.bGREEN)
        nnir=len(self.bNIR)
        nblue=len(self.bBLUE)
        if(nred>2 and nnir>2):
           self.hasdata=True
        else:
           self.hasdata=False 
           
        self.bands=[]
        if(nblue>2):
            self.bands.append('BLUE')
        if(ngreen>2):
            self.bands.append('GREEN')
        if(nred>2):
            self.bands.append('RED')
        if(nnir>2):
            self.bands.append('NIR')    
            
    def getBandNames(self):
        xbands=self.bands
        return xbands        
        
    def displayRSR(self):
        print("Convolution:")
        if(self.hasdata==True):
            print("Sensor:",self.sensorname)
            print("Resolution:",self.resmeter,"meters")
            print("Bands:",self.getBandNames())
        else:
            print("Information is missing")
           
    def list2array(self,datalist):
        n=len(datalist)
        data=np.zeros((n,2))
        for r in range(n):
            data[r,0]=datalist[r][0]
            data[r,1]=datalist[r][1]
        return data    
        
    def getBand_RSR(self,bandname):
        data=[]
        bandname=bandname.upper()
        if(bandname=='RED'):
            data=self.list2array(self.bRED)
        if(bandname=='GREEN'):
            data=self.list2array(self.bGREEN)
        if(bandname=='BLUE'):
            data=self.list2array(self.bBLUE)
        if(bandname=='NIR'):
            data=self.list2array(self.bNIR)    
        return data     
    
    def spatial_resample(self,data,n):
        #get size of input band
        nrowsIN,ncolsIN=data.shape
        #calculate output band size
        nrows=int(round(nrowsIN // n))
        ncols=int(round(ncolsIN // n))
        n=int(round(n))
        
        #create empty band
        datares=np.zeros((nrows,ncols))
        for i in range(0,nrows):
            for j in range(0,ncols):
                
                #calculate row at input band
                rowIN=i*n
                #check for out of boundary row
                if(rowIN<0):
                    rowIN=0
                elif (rowIN>nrowsIN-1):
                    rowIN=nrowsIN-1
                    
                #calculate col at input band    
                colIN=j*n
                #check for out of boundary column
                if(colIN<0):
                    colIN=0
                elif (colIN>ncolsIN-1):
                    colIN=nrowsIN-1
                
                
                #subset and get average
                avgvalue=np.mean(data[rowIN:rowIN+n,colIN:colIN+n])
                
                #get the integer value of the average
                datares[i,j]= int(avgvalue)
        return datares
    
    def parseline(self,line): 
        line=line.strip('\n')
        n=len(line)
        if(n>2):
          line=line.split(",")          
        else:
          line=[0]          
        return line
               
    def add_WRtoBand(self,band,wave,refl):
        if(band=='RED'):
            self.bRED.append([wave,refl])
        elif(band=='NIR'):
            self.bNIR.append([wave,refl])
        elif(band=='GREEN'):
            self.bGREEN.append([wave,refl])
        elif(band=='BLUE'):
            self.bBLUE.append([wave,refl])    
    
    def Load_RSR(self,fname):
        band=''
        self.bands_reset()   
        print("Reading RSR:",fname)
        file=open(fname,"r")
        for line in file:
           data=self.parseline(line)
           if(data[0]=='SENSORNAME'):
               self.sensorname=data[1]
           elif (data[0]=='PIXELMETERS'):
               self.resmeter=float(data[1])
           elif (data[0]=='BAND'):
               band=data[1]
               band=band.upper()
           elif (data[0]=='WAVE'):
               data[0]=0
           else:
             data[0]=float(data[0])
             if(data[0]>100 and data[0]<3000):
                 self.add_WRtoBand(band,data[0],float(data[1]))
                    
        file.close()
        self.bands_checkdata()
        
         
    def Convo_Pixel(self, Wave, Refl):
        #len should match
        Data=[]
        if(len(Wave)==len(Refl)):
          # do something
          a=5    
        else :
          print("Arrays should be of the same size")
        
        return Data
          
    
    def getRSRweight(self,wave,bandWaves):
        weight=0
        n=len(bandWaves)
        found=False
        i=1
        item_prev=bandWaves[0]
        while (found==False and i<n):
            item=bandWaves[i]
            if(wave>item_prev[0] and wave<=item[0]):
                found=True
                dx=item[0]-item_prev[0]
                dy=item[1]-item_prev[1]
                d=wave-item_prev[0]
                x=d*dy/dx
                
                weight=x+item_prev[1]
            else:
              i=i+1
            item_prev=item
              
        return weight
            
    
    def prepare_convolution(self,NEONWaves,bandWaves):
        #get min and max
        n=len(bandWaves)
        wavemin=bandWaves[0][0]
        wavemax=bandWaves[n-1][0]
        
        #locate index values from neonWaves
        n=len(NEONWaves)
        index_min=0
        index_max=0
        valueprev=NEONWaves[0]
        for i in range(1,n):
            value=NEONWaves[i]
            if(wavemin>valueprev and wavemin<=value):
                index_min=i
            if(wavemax>valueprev and wavemax<=value):
                index_max=i
            valueprev=value    
                
        #print(" idxmin=",index_min," idxmax=",index_max)        
        print(" min=",wavemin,"max=",wavemax)
        
        #calculate coefficients
        self.RSRweight=[]
        SRFsum=0
        for i in range(index_min,index_max+1):
            wave=NEONWaves[i]
            weight=self.getRSRweight(wave,bandWaves)
            self.RSRweight.append([i,weight])
            SRFsum=SRFsum+weight
        
        #print("Interpolation:")
        #print(self.RSRweight)
        return index_min, index_max,SRFsum
        
    
    def convoband(self,NEONWaves,DataCube,bandRSR,nrows,ncols,label):
        print(" band:",label)
        dataBand=np.zeros((nrows,ncols),np.int16)
        idxmin,idxmax,SRFsum=self.prepare_convolution(NEONWaves,bandRSR)
        if(idxmin>0 and idxmax>0 and idxmax<426 and SRFsum>0):
           
           dataTMP=np.zeros((nrows,ncols),np.float64)
           nbands=len(self.RSRweight)
           for i in range(nbands):
               idx=idxmin+i
               print(" ",idx, end='')
               #data=DataCube[:,:,idx]
               w=self.RSRweight[i][1]
               dataTMP=dataTMP+(DataCube[:,:,idx]*w)
               
           dataTMP=dataTMP/SRFsum 
           #put back as integer
           for r in range(0,nrows):
               for c in range(0,ncols):
                   dataBand[r,c]= int(dataTMP[r,c])
              
           print(' .')      
        else:
            print("An error ocurred, not possible to locate band")
            
        return dataBand     
    
    def Spectral_Convolution(self,NEONWaves,DataCube):
        print("Processing convolution...")
        DataSim=[]
        if(self.hasdata==True):
           nrows,ncols,nbands=DataCube.shape
           #if(len(NEONWaves)==nbands):
           DataSim=np.zeros((nrows,ncols,4),np.int16)
           DataSim[:,:,0]=self.convoband(NEONWaves,DataCube,self.bBLUE,nrows,ncols,'BLUE')
           DataSim[:,:,1]=self.convoband(NEONWaves,DataCube,self.bGREEN,nrows,ncols,'GREEN')
           DataSim[:,:,2]=self.convoband(NEONWaves,DataCube,self.bRED,nrows,ncols,'RED')
           DataSim[:,:,3]=self.convoband(NEONWaves,DataCube,self.bNIR,nrows,ncols,'NIR') 
        else:
            print("Missing RSR information")
            
        return DataSim
        
    def Spectral_Spatial_Convolution(self,NEONWaves,DataCube,pixelsize=0):
        Data=[]
        if(self.hasdata==True):
            if(pixelsize==0):
                pixelsize=self.resmeter
            else :
                pixelsize= int(pixelsize)
            if(pixelsize>1 and pixelsize<500):
                Data=self.Spectral_Convolution(NEONWaves,DataCube)
                nrowsIN,ncolsIN,nbands=Data.shape
                nrows= int(round( nrowsIN / pixelsize))
                ncols= int(round( ncolsIN // pixelsize))
                
                if(nrows>1 and ncols>1):
                    #do something
                    print("Spatial Resampling at ",pixelsize," [",nrows,",",ncols,"]")
                    DataRes=np.zeros((nrows,ncols,nbands),np.int16)
                    for i in range(nbands):
                       DataRes[:,:,i]=self.spatial_resample(Data[:,:,i],pixelsize)
                    Data=DataRes
                else:
                    print("Spatial convolution can not be performed")
                
                
                #Data=self.spatial(pixelsize)
            else:
                print("Pixel size between 2 and 500 for now") 
        else:
            print("Missing RSR information")  
            
        return Data
       
    
    def Load_Wavesfile(self,fname):
         # Read the wavelength values from the textfile
        file = open(fname, 'r') 
        Xvalues= file.readlines() 
        nvalues=len(Xvalues)
        
        #convert text to number (float)
        for i in range(0,nvalues):
          Xvalues[i]=float(Xvalues[i]) 
        
        # close text file
        file.close
        
        return Xvalues



        
# end of class        


