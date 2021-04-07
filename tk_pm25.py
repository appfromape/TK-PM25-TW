import tkinter as tk
import pandas as pd


def rbCity():
    global sitelist, listradio
    sitelist.clear()
    for r in listradio:
        r.destroy()
    n=0
    for c1 in data["County"]:
        if(c1 == city.get()):
            sitelist.append(data.iloc[n, 0])
        n += 1    
    sitemake()
    rbSite()

def rbSite():
    n = 0
    for s in data.iloc[:, 0]:
        if(s == site.get()):
            pm = data.iloc[n, 11]
            if(pm=='' or pm=='ND'):
                result1.set(s + "站的 PM2.5 值目前無資料！")
            else:
                if(int(pm) <= 35):
                    grade1 = "低"
                elif(int(pm) <= 53):
                    grade1 = "中"
                elif(int(pm) <= 70):
                    grade1 = "高"
                else:
                    grade1 = "非常高"
                result1.set(s + "站的 PM2.5 值為「" + str(pm) + "」：「" + grade1 + "」等級")
            break
        n += 1
    
def clickRefresh():
    global data
    data = pd.read_json("http://opendata2.epa.gov.tw/AQI.json")
    rbSite()

def sitemake():
    global sitelist, listradio
    for c1 in sitelist:
        rbtem = tk.Radiobutton(frame2,fg="black", text=c1, variable=site, value=c1, command=rbSite)
        listradio.append(rbtem)
        if(c1==sitelist[0]):      
            rbtem.select()
        rbtem.pack(side="left")


data = pd.read_json("http://opendata2.epa.gov.tw/AQI.json")

win=tk.Tk()
win.geometry("800x270")
win.title("PM2.5 實時監測")

city = tk.StringVar()
site = tk.StringVar()
result1 = tk.StringVar()
citylist = []
sitelist = []
listradio = []

for c1 in data["County"]:  
    if(c1 not in citylist):
        citylist.append(c1)

count = 0
for c1 in data["County"]:  
    if(c1 ==  citylist[0]):
        sitelist.append(data.iloc[count, 0])
    count += 1

label1 = tk.Label(win, text="縣市：", pady=6, fg="blue", font=("新細明體", 12))
label1.pack()
frame1 = tk.Frame(win)
frame1.pack()
for i in range(0,3):
    for j in range(0,8):
        n = i * 8 + j
        if(n < len(citylist)):
            city1 = citylist[n]
            rbtem = tk.Radiobutton(frame1, fg="black", text=city1, variable=city, value=city1, command=rbCity)
            rbtem.grid(row=i, column=j)
            if(n==0):
                rbtem.select()

label2 = tk.Label(win, text="測站：", pady=6, fg="blue", font=("新細明體", 12))
label2.pack()
frame2 = tk.Frame(win)
frame2.pack()
sitemake()

btnDown = tk.Button(win, text="更新資料", font=("新細明體", 12), fg="blue", command=clickRefresh)
btnDown.pack(pady=6)
lblResult1 = tk.Label(win, textvariable=result1, fg="red", font=("新細明體", 16))
lblResult1.pack(pady=6)
rbSite()

win.mainloop()