import os
import numpy as np
import re 
from os import listdir
from os.path import isfile,join
import time
from datetime import datetime
class read():
    def __init__(self,lapalma_path,sordar_path,ali_path,massdata_path):       
        self.datacube_lapa=dict()
        self.protimelabel=[]        #All the profile data                   
        self.prodata=[] 
        self.proname=[]            #Iteration to get the profile data        

        self.datacube_sordar=dict()
        self.datacube_ali=dict()
        self.datacube_mass=dict()
        self.timedata=[]                 #All the profile data                   
        self.prodata_mass=[]             #Iteration to get the profile data 

        self.folder_lapa=lapalma_path
        self.sordar_path= sordar_path
        self.ali_path = ali_path
        self.massdata_path = massdata_path
    
    def readlapalmadata(self):
        # self.folder=folder
        folder = self.folder_lapa
        #Read all the profile.txt file from the folder '*profile.txt' will be assumed to be profile
        onlyfiles = [ f for f in listdir(folder) if isfile(join(folder,f)) ]
        for temfile in onlyfiles:
            self.proname.append(temfile)
            if 'profile.txt' in temfile:
                self.protimelabel.append(time.mktime(datetime.strptime("".join(list(filter(str.isdigit,temfile))), '%Y%m%d%H%M%S').timetuple()))
                temfile=open(folder+temfile)
                line=temfile.readline()
                #temdata is used to store each profile
                temdata=None
                errormark=0
                #Read the profile
                while line:
                    linetemdata=line.split()
                    if linetemdata[0] != '###':
                        linetemdata=list(map(float,linetemdata))
                        # linetemdata=np.array([[linetemdata[0],linetemdata[1],linetemdata[2],linetemdata[3]]])
                        linetemdata=np.array([[linetemdata[0],linetemdata[1],linetemdata[2],linetemdata[3]]])  #  h and cn2 and v and deg
                        if temdata is None:
                            temdata=linetemdata
                        else:
                            temdata=np.concatenate((temdata,linetemdata))
                    line=temfile.readline()
                #Check the data status
                if temdata is not None and errormark is not 1:
                    hightsize = temdata.shape
                    for i in range(hightsize[0], -1, -1):  # delete  negative rows of high
                        if  temdata[i-1][0] <= 0.0:
                            temdata=np.delete(temdata,[i-1],axis=0)

                    cnsize=temdata.shape                    #delete  0 rows of cn
                    for j in range(cnsize[0],-1,-1):
                        if temdata[j-1][1]==0:
                            temdata=np.delete(temdata,[j-1],axis=0)
                    #Add or comment the relative weight will not change the results much
                    # temdata[:,1]=np.abs(temdata[:,1])/sum(temdata[:,1])#*1000
                    #We need to set all the values to 100*4 dimensions
                    newdata=np.zeros([100,4])
                    orgsize=np.shape(temdata)[0]
                    newdata[0:orgsize,:]=temdata
                    self.prodata.append(newdata)
                else:
                    self.protimelabel.pop()
        #to genrate the datacube with time as key and profile as data
        # ind=0
        # for sec in self.protimelabel:
        #     self.protimelabel[ind]=time.ctime(int(sec))
        #     ind=ind+1
        # self.datacube_lapa=dict(zip(self.protimelabel,self.prodata))
        self.datacube_lapa=dict(zip(self.proname,self.prodata))
        
    def readsordardata(self):
        path = self.sordar_path
        onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
        for temfile in onlyfiles:
            if 'sfas_data14.txt' in temfile:
                path = path+temfile
                print(path)
                height = np.arange(10,205,5).reshape(-1,1)    #sfas_data14.txt
                # height = np.arange(40,820,20).reshape(-1,1)   #xfas_data14.txt
                self.readsordardata_one(path,height)
            else:
                pass

    def readsordardata_one(self,path,height):
        f = open(path,"r")  
        line = f.readline()  
        from datetime import datetime, timedelta
        data =[ ]
        cn2 = []
        time = []
        speed = []
        Dir = []
        while line:  
            data.append(line.split(" "))          
            i=len(data)-1
            if data[i][5] == '0.000000e+000'or data[i][5] == 'NaN':                    
                data.remove(data[i])
            else:
                cn2.append(data[i][5:44])
                # speed.append(data[i][44:83]) 
                # Dir.append(data[i][200:239])
                p = re.compile(r'\d\d\d\d\d\d.\d\d\d\d\d\d')
                x=p.findall(line)                
                x=''.join(x)
                date = datetime.fromordinal(int(float(x)))+ timedelta(days=float(x)%1) - timedelta(days = 366)
                time.append(date)
            line = f.readline()
        f.close() 
        data1=height
        data2= np.asfarray(cn2).reshape(-1,1)
        # data3= np.asfarray(speed).reshape(-1,1)
        # data4= np.asfarray(Dir).reshape(-1,1)  
        print(len(data1),len(data2))
        out_list=[]
        for i in range(len(data2) ):            
            out_list_z=[]
            out_list_z.append( float(data1[i-int(i/39)*39]) )
            out_list_z.append( float(data2[i]) )
            # out_list_z.append( float(data3[i]) )
            # out_list_z.append( float(data4[i]) )
            out_list.append(out_list_z)
        out_list = np.array(out_list)
        for i in range( int(len(out_list)/39)):
            self.datacube_sordar[time[i]]=out_list[i*39:39*(i+1)]

    def readmassdata(self):
        path =self.massdata_path
        onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
        # datacube2=dict()
        X=[] 
        for temfile in onlyfiles:
            if 'results.TMTMASS' in temfile:
                f=open(path+temfile,'r') 
                for line in f.readlines():
                    line=line.strip('\n')
                    line =line.split(" ")
                    if "9999.00" in line:
                        continue
                    else:
                        while ('') in line:                
                            line.remove('')                           
                        if line[6]=='X':
                            str2=line
                            X.append(str2)                                                      
                f.close()                                     
            else:
                pass
        name2 = []
        data2 = []
        data2_2 = []                       
        for i in range(len(X)):            
            name2.append(X[i][0]+"."+X[i][1]+"."+X[i][2]+"."+X[i][3]+":"+X[i][4]+":"+X[i][5])
            data2.append(X[i][10:])     
        for i in data2:
            data2 = np.asfarray(i).reshape((-1,2))
            data2_2.append(data2)                    
        self.datacube_mass=dict(zip(name2,data2_2))
        self.timedata=name2                 #All the profile data                   
        self.prodata_mass=data2_2 
        # for key,value in datacube2.items():
        #     listz0 = []
        #     for i in range(len(datacube2[key])):
        #         listz0.append( datacube2[key][i])                
        #     listz = np.array(listz0)
        #     self.timedata=datacube2[key]
        #     self.prodata_mass = listz
        #     self.datacube_mass[key] = listz

 
    # def readmassdata_one(self,path):
    #     datacube1=dict()   
    #     datacube2=dict()
    #     L=[]
    #     X=[]  
    #     f=open(path,'r') 
    #     for line in f.readlines():
    #         line=line.strip('\n')
    #         line =line.split(" ")
    #         if "9999.00" in line:
    #             continue
    #         else:
    #             while ('') in line:                
    #                 line.remove('')              
    #             if line[6]=='L':
    #                 str1=line
    #                 L.append(str1)                
    #             if line[6]=='X':
    #                 str2=line
    #                 X.append(str2)  
    #     f.close()                
    #     # name1 = []
    #     # data1 = []
    #     # data1_1 = []
    #     name2 = []
    #     data2 = []
    #     data2_2 = []         
    #     # for i in range(len(L)):            
    #     #     name1.append(L[i][0]+":"+L[i][1]+":"+L[i][2]+":"+L[i][3]+":"+L[i][4]+":"+L[i][5])             
    #     #     data1.append(L[i][10:16])       
    #     # for i in data1:
    #     #     s = len(i)
    #     #     data1 = np.asfarray(i).reshape((-1,2))
    #     #     data1_1.append(data1)            
    #     # datacube1=dict(zip(name1,data1_1))                
    #     for i in range(len(X)):            
    #         name2.append(X[i][0]+":"+X[i][1]+":"+X[i][2]+":"+X[i][3]+":"+X[i][4]+":"+X[i][5])
    #         data2.append(X[i][10:])
    #     #    print(data2)       
    #     for i in data2:
    #         s = len(i)
    #         data2 = np.asfarray(i).reshape((-1,2))
    #         data2_2.append(data2)                    
    #     datacube2=dict(zip(name2,data2_2))        
    #     # L在前x在后
    #     for key,value in datacube2.items():
    #         listz = []
    #         # print(len(datacube2[key]))
    #         # for i in range(len(datacube1[key])):
    #         #     listz.append( datacube1[key][i])
    #         # print(len(listz))
    #         for i in range(len(datacube2[key])):
    #             listz.append( datacube2[key][i])
    #         listz = np.array(listz)
    #         self.datacube_mass[key] = listz
    
    def readalidata(self):            
        path = self.ali_path
        onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
        for temfile in onlyfiles:
            if '.rn00' in temfile:
                self.readalidata_one(path,temfile)        
            else:
                pass 
    def readalidata_one(self,path,nfilename):  
        filename=nfilename
        f=open(path+filename)
        line=f.readline()
        Heure=[]
        Minute=[]
        Seconde=[]
        data=[]
        cut = [0]*3000
        cut_num2 = -1        
        sitenum1 = 1
        sitenum2 = 1        
        line_num = -1
        delete_num = 0
        sub_num = 0
        while line:   
            x=line
            x1=''.join(x)
            site=x1.rfind('Heure')            
            #shu chu shijian
            if(site==1):               
                sitel=x1.rfind('=')                                    
                last_site=len(x1)
                str1 = x1[sitel+1:last_site+1]
                Heure.append(str1)
            site=x1.rfind('Minute')
            if(site==1):
                sitel=x1.rfind('=')
                last_site=len(x1)
                str2 = x1[sitel+1:last_site+1]
                Minute.append(str2)
            site=x1.rfind('Seconde')
            if(site==1):
                sitel=x1.rfind('=')
                last_site=len(x1)
                str3 = x1[sitel+1:last_site+1]
                Seconde.append(str3)            
            site = x1.rfind('=')# shu chu shu ju             
            line_num = line_num+1
            if  line_num%2== 0 :
                sitenum1 = site
            else:
                sitenum2 = site                
            if(site==-1):
                if sitenum1==sitenum2:  
                     pass
                else:
                    cut_num2 = cut_num2+1
                    delete_num = 0
                    sub_num = 0                    
                xx = x1.split()       
                for i in range(len(xx)):
                    if float( xx[0] )<0 or float( xx[3] )==0:               
                        pass           
                    else:
                        if float( xx[0] )  == 0:
                            if sub_num !=0:
                                xx[0] =  sub_num *120
                                sub_num = sub_num+1  
                            else:
                                sub_num = sub_num+1                                     
                        if i==1:
                            pass
                        else:
                            delete_num = delete_num+1
                            data.append(float(xx[i]))                             
                if  cut_num2<3000:
                    cut[cut_num2] = delete_num/5
            line = f.readline()            
        lenth =  len(data)
        xxx= np.full((lenth,),0)
        for i in range(lenth):
            xxx[i] = data[i]
        x1=xxx  
        DICT={}
        l = 0
        r = 0
        for i in range(len(cut)):
            if cut[i]>0:    
                num = 5*int(cut[i])   
                if i==0:
                    l = 0
                else:
                    l = r
                r = r+num
                NAME1=Heure[i].strip("\n").strip()+":"+Minute[i].strip("\n").strip()+":"+Seconde[i].strip("\n").strip()
                DATA=x1[l:r].reshape(int(cut[i]),5 )
                DICT[NAME1]=DATA        
        x=filename
        x=''.join(x)
        site=x.rfind('.')        
        if(site>1):
            site=x.rfind('.')
            last_site=len(x)
            str2 = x[:site]
        self.datacube_ali[str2]=DICT 

