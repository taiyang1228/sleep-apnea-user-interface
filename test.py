import sys
import numpy as np
import tkinter as tk
from tkinter import filedialog  
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tensorflow.keras import models,utils

class check:
    def __init__(self,model=None,model_file_path=None,signal_file_path=None,
                signal=[],csv=0):
        np.random.seed()
        self.font = ('Arial', 12)
        self.model = model
        self.model_file_path = model_file_path
        self.signal_file_path = signal_file_path
        self.signal = signal
        self.csv = csv

    def set_button(self,text='',width=0,height=0,x=0,y=0,func=None):
        place_button = tk.Button(text=text, font=self.font, width=width, height=height,command=func)
        place_button.place(x=x,y=y)

    def set_label(self,text='',width=0,height=0,x=0,y=0):
        place_label = tk.Label(text=text, font=self.font, width=width, height=height)
        place_label.place(x=x,y=y)

    def set_message(self,title,message=''):
        messagebox.showinfo(title=title, message=message) 

    def close_window(self):
        sys.exit()

    def hit_choose_model(self):
        self.model_file_path = filedialog.askopenfilename()
        self.set_message(title='載入模型', message='載入模型中')    
        try:
            self.model = self.load_model(self.model_file_path)
            self.set_message(title='載入模型', message='載入模型成功') 
        except:
            self.set_message(title='載入模型', message='載入模型失敗，請重新選擇檔案') 
    
    def hit_choose_signal(self):
        self.signal_file_path = filedialog.askopenfilename()
        self.set_label(text='檔案路徑：'+self.signal_file_path,x=0,y=150)
        try:
            self.signal,self.csv = self.read_Des_npz_file(self.signal_file_path)
            self.set_label(text='訊號圖形顯示：'+self.signal_file_path,x=0,y=2000)
            plt.figure(figsize=(6,2))
            plt.plot(self.signal)
            fig = plt.gcf()
            canvas = FigureCanvasTkAgg(fig)
            canvas.draw()
            canvas.get_tk_widget().place(x=0,y=220)
        except:
            self.set_message(title='載入檔案', message='載入檔案失敗，該檔案非npz格式') 

    def load_model(self,file_path):
        model = models.load_model(file_path)
        return model

    def read_Des_npz_file(self,file):
        npz_data = np.load(file, allow_pickle=True)
        return npz_data['ECG_signal'], npz_data['csv_data'].item()

    def detect_OSA_severity(self):
        self.set_message(title='檢測訊號', message='檢測中...')
        signal_ = np.array(self.signal/100.0).reshape(-1,1)
        prediction = self.predict_model(signal_)
        self.set_label(text='睡眠呼吸中止症檢測結果為第 {} 類'.format(prediction[0]),x=10,y=500)
        self.set_message(title='檢測訊號', message='檢測完成')

    def generator(self,signal_,fake):
        while 1:
            signal_save=[]
            label_save=[]
            signal_save.append(np.array(signal_))
            label_save.append(np.array(utils.to_categorical(fake,4)))
                
            X_batch = np.array(signal_save)
            y_batch = np.array(label_save)
            yield X_batch, y_batch

    def predict_model(self,signal_):
        prediction = np.argmax(self.model.predict(self.generator(np.array(signal_),0)
                                            ,steps=1
                                            ,verbose=0),axis=1)
        return prediction
    
    