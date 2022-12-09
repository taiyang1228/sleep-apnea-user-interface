import tkinter as tk
from test import check

window = tk.Tk()
window.title('Sleep Apnea Detector')
window.geometry('600x600')
position = check()
position.set_button('載入模型',width=10,height=1,x=250,y=50,func=position.hit_choose_model)
position.set_label('請選擇檔案：',width=20,height=1,x=0,y=100)
position.set_button('選擇檔案',width=10,height=1,x=200,y=100,func=position.hit_choose_signal)
position.set_button('開始檢測',width=10,height=1,x=250,y=420,func=position.detect_OSA_severity)
position.set_button('結束程式',width=10, height=1,x=250,y=550,func=position.close_window)

position.set_message(title='初始化',message='初始化完成')
window.mainloop()
