# -*- coding: utf-8 -*-
"""
Date: 2017/11/07
Author: Robi

Target:
    獲得圖片檔EXIF(Exchangeable image file format)資訊進行自動化檔名修改
    for JPEG、TIFF、RIFF
info:
    exifread:
        https://pypi.python.org/pypi/ExifRead
        http://www.exiv2.org/tags.html
reference: 
    https://docs.python.org/3/library/os.html?highlight=os#module-os
    https://www.ricequant.com/community/topic/2027/
"""
import os, glob, time
import exifread
import pandas as pd
#import numpy as np


def GuiGet():
    #開啟視窗選單選取畫面
    #import tkinter as tk
    #from tkinter import filedialog
    
    #root = tk.Tk()
    #root.withdraw()
    
    file_path = filedialog.askopenfilename()
    
    '''
    #也可以使用以下的讀檔方式：
    import easygui
    path = easygui.fileopenbox()
    '''
    return file_path


def FilePath():
    #讀取路徑以及檔案列表
    #temp=input('請輸入支援EXIF資訊的照片格式:JPG/JPEG/TIFF/RIFF\n')
    temp='JPG'
    files=glob.glob('./*.'+temp)    #.JPG, .TIF, .WAV    #若是沒有找到對應的資料則回傳空集合
    return(files)
    
def PhotoTime(file):
    #讀取作業系統提供的"建立日期"、"編輯日期"
    info= os.stat(file)    #取得時間戳資料
    date_c= time.strftime('%Y%m%d-%H%M',time.localtime(info.st_ctime))    # creation of time
    date_m= time.strftime('%Y%m%d-%H%M',time.localtime(info.st_mtime))    # modification of time
    
    #讀取EXIF資訊
    fid_rb1 = open(file, 'rb')    #'rb'==reading (binary mode)
    tags = exifread.process_file(fid_rb1)    #.process_file(f, stop_tag='UNDEF', details=True, strict=False, debug=False)
    '''
    #print(tags)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print ("Key: %s, value %s" % (tag, tags[tag]))
    '''
    #提取"拍攝日期"
    temp=str(tags['EXIF DateTimeOriginal'])    #
    temp= temp.split(' ')
    date_o=temp[0].split(':')+temp[1].split(':')[0:2]
    date_o.insert(3,'-')
    date_o=''.join(date_o)
    '''
    Exif.Image.DateTime
        The date and time of image creation. In Exif standard, it is the date and time the file was changed.
    Exif.Image.DateTimeOriginal	
        The date and time when the original image data was generated.
    '''
    return date_o,date_m,date_c

def NakeLog(files,dates,sel=0):
    #資料合併
    
    filename= [os.path.basename(x) for x in files]    #從完整路徑中取得filename
    name_new=[]
    for n in range(0,len(filename)):
        name_new.append(dates[n][sel]+'_'+filename[n])
    
    #建立.csv，紀錄"檔案名稱"、"原始名稱"、"拍攝日期"、"建立日期"、"編輯日期"
    title=['檔案名稱','原始名稱','拍攝日期','建立日期','編輯日期']
     
    df1= pd.DataFrame(name_new,index=range(0,len(filename)),columns=[title[0]])    #注意單一字串直接轉換list會被拆解成字元
    df2= pd.DataFrame(filename,index=range(0,len(filename)),columns=[title[1]])
    df3= pd.DataFrame(dates,index=range(0,len(filename)),columns=title[2:5])
    res_df= pd.concat([df1,df2,df3],axis=1, ignore_index=False, join='outer')
    #df.columns.values    #顯示columns
    #df.rename(columns={ df.columns[2]: "new name" }, inplace=True)    #columns修改其中之一
    #df.columns = ['col_1', 'col_2', 'col_3']    #columns全數修改
        
    file_name='./Info.csv'
    #df.to_csv(file_name, sep=',', encoding='utf-8')
    res_df.to_csv(file_name, sep=',', encoding='ansi')    #for Excel
    return 0

def ReFile(file_path, duplication=1):
    
    data_df= pd.read_csv(file_path,encoding='ansi')
    name_new=list(data_df[data_df.columns[1]])
    filename=list(data_df[data_df.columns[2]])
    #指定依據時間修改檔名，是否指定新資料夾另存(保留原始修改日期)
    if duplication==1:    #1==Yes; 0==No
        folder='result'
        os.system('md "./'+folder+'"')
        for n in range(0,len(filename)):
            os.system('copy "./'+filename[n]+'" "./'+folder+'/'+name_new[n]+'" /Y/V')
            print('copy "./'+filename[n]+'" "./'+folder+'/'+name_new[n]+'" /Y/V')
    else:
        folder=os.getcwd()
        for n in range(0,len(filename)):
            os.system('move /-Y "./'+filename[n]+'" "./'+name_new[n]+'"')
            print('move /-Y "./'+filename[n]+'" "./'+name_new[n]+'"')
    return 0

def toFolder(file_path, duplication=2):
    data_df= pd.read_csv(file_path,encoding='ansi')
    #讀取同一天日期，自動分類至該日期資料夾
    date_idx=list(data_df[data_df.columns[3]])
    date_idx=[ x[:x.find('-')] for x in date_idx]    #切割出'年月日'    #注意這裡因為是只有一個'-'...
    date_set=set(date_idx)
    
    for fmd in date_set:
        os.system('md "./'+fmd+'"')
        for n, idx in enumerate(date_idx,0):
            if fmd==idx:
                file=data_df.loc[n][data_df.columns[2]]    #df.DataFrame要用超過一維的index提取特定資料時需要加上.loc
                
                if duplication==1:
                    os.system('copy "./'+file+'" "./'+fmd+'/'+'" /Y/V')
                    print('copy "./'+file+'" "./'+fmd+'/'+'" /Y/V')
                else:
                    os.system('move /-Y "./'+file+'" "./'+fmd+'/"')
                    print('move /-Y "./'+file+'" "./'+fmd+'/"')
    return 0
    
def main():
    files=FilePath()
    #files=GuiGet()
    if len(files)==0:
        print('No File')
        return 1
        
    for n in range(0,len(files)):
        print('%s' %files[n], sep='\n')
    
    dates=[]
    for file in files:
        date=PhotoTime(file)
        dates.append(date)
    
    NakeLog(files,dates,sel=0)
    
    Info_path='./Info.csv'
    #ReFile(Info_path, duplication=1)
    toFolder(Info_path, duplication=2)
    return 0
    
if __name__ == '__main__':
    #__name__是當前此程式的名稱
    #'_main_'是正在被直行的程式名稱。(不包括"被引入")
    main()