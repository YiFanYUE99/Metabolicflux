# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:00:04 2021

@author: YiFan Yue
"""
import tkinter as tk
import numpy as np
import pandas as pd
import time
#建立窗口
window=tk.Tk()
window.title('mass spectrometry data processing')
window.geometry('900x900')
#标签
l1=tk.Label(window,text='a mass spectrometry data processing software made by Yifan Yue',font=("Times",8,"bold"))#font确定字体为Times，大小为8，字体加粗bold
l1.place(relx=0.5,rely=0.93,relheight=0.1,relwidth=0.5)
#定义输入框
e1=tk.Entry(window)
e1.place(relx=0.25,rely=0.05,relheight=0.04,relwidth=0.5)
e1.insert(0, "同位素取代的碳原子量ex:6")
e2=tk.Entry(window)
e2.place(relx=0.25,rely=0.1,relheight=0.04,relwidth=0.5)
e2.insert(0, "每个13C和普通C的质量差ex:1.0033")
e3=tk.Entry(window)
e3.place(relx=0.25,rely=0.15,relheight=0.04,relwidth=0.5)
e3.insert(0, "每个13C和普通C的质量差允许的误差ex:0.0002")
e4=tk.Entry(window)
e4.place(relx=0.25,rely=0.2,relheight=0.04,relwidth=0.5)
e4.insert(0, "保留时间允许的误差ex:0.05")
e5=tk.Entry(window)
e5.place(relx=0.25,rely=0.25,relheight=0.04,relwidth=0.5)
e5.insert(0, "CK组的样品个数ex:5")
e6=tk.Entry(window)
e6.place(relx=0.25,rely=0.3,relheight=0.04,relwidth=0.5)
e6.insert(0, "实验组的样品个数ex:3")
e7=tk.Entry(window)
e7.place(relx=0.25,rely=0.35,relheight=0.04,relwidth=0.5)
e7.insert(0, "输入文件的地址名称")
e8=tk.Entry(window)
e8.place(relx=0.25,rely=0.4,relheight=0.04,relwidth=0.5)
e8.insert(0, "输出文件的地址名称")
#加入文本框
t=tk.Text(window,height=2)
t.place(relx=0.25,rely=0.75,relheight=0.08,relwidth=0.5)

def liu():
    tic=time.time()
    Cnum=int(e1.get());
    deltaC=float(e2.get());
    ddC=float(e3.get());
    deltaRT=float(e4.get());
    CKnum=int(e5.get());
    EXPnum=int(e6.get());
    input=e7.get();
    output=e8.get();
    daixieliu=pd.read_csv(input,header=0);
    dai=np.array(daixieliu);
    select=[];
    inde=[];
    for i in range(dai.shape[0]):
        EXParea=np.mean(dai[i,2:(2+EXPnum)]);
        CKarea=np.mean(dai[i,(2+EXPnum):(2+EXPnum+CKnum)]);
        if (EXParea>5000) and (CKarea<5000) and (EXParea/CKarea>10):
            RTdown=dai[i,1]-deltaRT
            RTup=dai[i,1]+deltaRT
            Massup=dai[i,0]-Cnum*(deltaC-ddC)
            Massdown=dai[i,0]-Cnum*(deltaC+ddC)
            for j in range(dai.shape[0]):
                if (RTdown<dai[j,1]<RTup) and (Massdown<dai[j,0]<Massup):
                    EXParea1=np.mean(dai[j,2:(2+EXPnum)]);
                    CKarea1=np.mean(dai[j,(2+EXPnum):(2+EXPnum+CKnum)]);
                    if (EXParea1>5000) and (CKarea1>5000) and (0.5<(EXParea1/CKarea1)<2) :
                        select.append(dai[i,:])
                        inde.append(1);
                        select.append(dai[j,:])
                        inde.append(0);
    selected=pd.DataFrame(select);
    ind=np.array(inde).reshape(selected.shape[0],1);
    selected=pd.DataFrame(np.hstack([ind,selected]));
    colu=np.insert(daixieliu.columns,0, "leixing");
    selected.columns=colu
    selected.to_csv(output,header=True,index=False);
    toc=time.time()
    t.insert('insert',"DONE "+str(toc-tic)+"s\n")

#按钮
b1=tk.Button(window,text='search',command=liu)
b1.place(relx=0.25,rely=0.85,relheight=0.08,relwidth=0.5)

#建立框
window.mainloop()
    
    
    
    
    