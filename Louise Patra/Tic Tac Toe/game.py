import tkinter as tk
from tkinter import *
import socket
import requests
import pickle
import os
import base64
from pyngrok import ngrok
from threading import Thread
from tkinter import messagebox
import cv2
import mediapipe as mp
from random import randint

# url="http://127.0.0.1:5002/"
url="http://louise055.pythonanywhere.com/"
w=800
h=460
flag=0
key=None
oid=None
camwidth=640
camheight=480
fe=0

def back(x,y,c=1,d=0,cap=None,con=None):
    x.deiconify()
    y.withdraw()
    if c:
        closeroom()
    if d:
        cap.release()
        cv2.destroyAllWindows()
        con.send("quit".encode())
        con.close()
    
def closecon(x,c=1):
    x.destroy()
    global window
    window.destroy()
    if c:
        closeroom()
def temp():pass    

def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def getdata():
    global key,oid,fe
    if os.path.exists("./data"):
        fe=1
        data=pickle.load(open("data","rb"))
        key=data["key"]
        print(key)
        # oid=data["onlineid"]

def init():
    global window,flag
    flag=is_connected()
    getdata()
    window=tk.Tk()
    window.geometry(str(w)+"x"+str(h))
    window.title("WELCOME")
    tk.Label(window, text="Hello User :D",font=('Helvetica bold', 24)).place(relx=0.5, rely=0.2, anchor="center")
    tk.Button(window, text="Create a room",command=lambda :croom(window),width=25, bd=5,padx=5, pady=5).place(relx=.5,rely=.3,anchor='center')
    tk.Button(window,text="Join a room",command=lambda :jroom(window),width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.4,anchor='center')
    tk.Button(window, text="How to play?",command=temp,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.5,anchor='center')
    tk.Button(window, text="About",command=temp,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')
    tk.Button(window,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Exit",command=lambda :window.destroy(),width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.7,anchor='center')
    # imgl.place(x=0, y=0, relwidth=1, relheight=1)
    window.bind_all('<Escape>', lambda x:window.destroy())
    window.protocol("WM_DELETE_WINDOW",lambda :window.destroy())
    # window.resizable(False,False)
    window.mainloop()
    
def croom(prev):
    current=tk.Toplevel()
    
    prev.withdraw()
    current.geometry(str(w)+"x"+str(h))
    current.title("New ROOM")
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(prev,current),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')

    tk.Label(current, text="Create a new room",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(current, text="User ID : ",font=('Helvetica bold', 12)).place(relx=.40,rely=.2,anchor='center')
    if oid is None:
        res=requests.get(url+"generateint")
        uid=0
        if res.ok:
            uid=res.json()['id']
        else:
            print("not ok")
    else:
        uid=oid
    mystr = StringVar()
    mystr.set(uid)
    mystr2 = StringVar()
    mystr2.set("Your name here")
    Entry(current,textvariable=mystr,state=DISABLED).place(relx=.55, rely=.2, anchor="center")
    tk.Label(current, text="Player Name : ",font=('Helvetica bold', 12)).place(relx=.37,rely=.3,anchor='center')
    name=Entry(current,textvariable=mystr2)
    name.place(relx=.55, rely=.3, anchor="center")
    mystr3 = StringVar()
    mystr3.set("Password")

    passw=Entry(current,textvariable=mystr3,show="*")
    passw.place(relx=.55, rely=.5, anchor="center")
    val=IntVar(value=0)
    typval=IntVar(value=0)
    
    def show():
        if(val.get()==1):passw.config(show='')
        else:passw.config(show='*')
    cbx=tk.Checkbutton(current,text='Show Password',variable=val,onvalue=1,offvalue=0,command=show)
    cbx.place(relx=.70, rely=.5, anchor="center")
    def chngval():
        passw.config(state=cval.get())
        cbx.config(state=cval.get())
        mystr3.set(-1)
    tk.Label(current, text="Password  :",font=('Helvetica bold', 12)).place(relx=.40,rely=.4,anchor='center')
    cval=StringVar(value=NORMAL)
    tk.Checkbutton(current,variable=cval,onvalue=NORMAL,offvalue=DISABLED,command=chngval).place(relx=.47, rely=.4, anchor="center")
    tk.Label(current, text="On/Offline  :",font=('Helvetica bold', 12)).place(relx=.56,rely=.4,anchor='center')
    tk.Checkbutton(current,variable=typval,onvalue=1,offvalue=0,state=DISABLED if flag==0 else NORMAL).place(relx=.64, rely=.4, anchor="center")
    tk.Label(current, text="Password : ",font=('Helvetica bold', 12)).place(relx=.37,rely=.5,anchor='center')
    tk.Label(current, text="Ngrok Authtoken : ",font=('Helvetica bold', 12)).place(relx=.35,rely=.6,anchor='center')
    mystr4 = StringVar()
    mystr4.set("Your Authtoken here" if key is None else key)
    print(DISABLED if key!=None else NORMAL,key)
    auth=Entry(current,textvariable=mystr4,state=DISABLED if key!=None else NORMAL)
    auth.place(relx=.55, rely=.6, anchor="center")
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Submit",command=lambda :connection(uid,mystr2.get(),mystr3.get(),typval.get(),mystr4.get(),current),width=8, bd=5, padx=5, pady=5).place(relx=.5,rely=.7,anchor='center')
    
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(window,current),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    current.protocol("WM_DELETE_WINDOW",lambda :closecon(current))
    # current.resizable(False,False)
    current.mainloop()
    
def connection(a,b,c,d,e,prev):
    print(d)
    global fe,key
    if fe==0:
        data={}
        key=e
        ngrok.set_auth_token(e)
        data['key']=e
        pickle.dump(data,open('data','wb'))
        fe=1
        
    def fn1():
        global host,port,server_socket,sc,nt
        sc=tk.Label(current, text="Creating Socket...",font=('Helvetica bold', 15))
        sc.place(relx=.5,rely=.3,anchor='center')
        host = socket.gethostname()
        host="127.0.0.1"
        port = 5000
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
        while 1:
            try:
                server_socket.bind((host, port)) 
                break
            except OSError:
                port+=1
                print(port)
        server_socket.listen(2)
        sc.destroy()
        sc=tk.Label(current, text="Socket Created.",font=('Helvetica bold', 15))
        sc.place(relx=.5,rely=.3,anchor='center')
        nt=tk.Label(current, text="Starting Ngrok Tunnel...",font=('Helvetica bold', 15))
        nt.place(relx=.5,rely=.4,anchor='center')
    def fn2():
        global socketurl,nt
        socketurl = ngrok.connect(host+":"+str(port), "tcp").public_url
        # ngrok_process = ngrok.get_ngrok_process()
        print(socketurl)
        nt.destroy()
        nt=tk.Label(current, text="Ngrok Tunnel Started.",font=('Helvetica bold', 15))
        nt.place(relx=.5,rely=.4,anchor='center')

    def fn3():
        epass=encrypt(encrypt(c,c),c)
        code=encrypt(socketurl,c)
        global ply
        res=requests.get(url+"/addserver?uid={}&usr={}&pass={}&code={}&type={}".format(a,b,epass,code,d))
        if res.ok:
            print(res.json())
            ply=tk.Label(current, text="Waiting for players to join the room...",font=('Helvetica bold', 15))
            ply.place(relx=.5,rely=.5,anchor='center')
        else:
            print("Not okay")
            tk.Label(current, text="Server creation error! Please try again.",font=('Helvetica bold', 15)).place(relx=.5,rely=.5,anchor='center')
    current=tk.Toplevel()
    prev.withdraw()
    current.geometry(str(w)+"x"+str(h))
    current.title("Waiting")
    global con,plys,plyc
    con=IntVar(value=0)
    plys=IntVar(value=0)
    plyc=IntVar(value=0)
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(window,current,1),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    tk.Label(current, text="Creating server..",font=('Helvetica bold', 15)).place(relx=.5,rely=.2,anchor='center')
    current.update_idletasks()
    current.update()
    fn1()
    current.update_idletasks()
    current.update()
    fn2()
    current.update_idletasks()
    current.update()
    fn3()
    current.update_idletasks()
    current.update()
    def playcall():
        global data
        if plys.get()+plyc.get()==2:
            current.update()
            a=randint(0,1)
            t="turn:"+str(a)
            conn.send(t.encode())
            play(conn,current,data,1-a)
    plys.trace('w',lambda x,y,z: playcall())
    plyc.trace('w',lambda x,y,z: playcall())

    Thread(target=getcon,args=(server_socket,current,prev)).start()
    
    current.mainloop()
    current.protocol("WM_DELETE_WINDOW",lambda :closecon(current,1))
    # current.resizable(False,False)
    
def getcon(server_socket,current,prev):
    global plys,con,plyc,conn,data
    conn, address = server_socket.accept()
    print("connected")
    con.set(1)
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="START",command=lambda :start(conn,prev,current),width=5, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')
    while 1:
        data = conn.recv(1024).decode()
        if data:
            ply.destroy()
            tk.Label(current, text="Player {} connected".format(data),font=('Helvetica bold', 15)).place(relx=.5,rely=.5,anchor='center')
            break
    while 1:
        data1 = conn.recv(1024).decode()
        if data1=="ready":
            ply.destroy()
            plyc.set(1)
            if plys.get()!=1:
                tk.Label(current, text="Player ready,click to start the game",font=('Helvetica bold', 7)).place(relx=.5,rely=.7,anchor='center')
            break

def start(conn,prev,current):
    if plyc.get()!=1:
        tk.Label(current, text="Waiting for player to start",font=('Helvetica bold', 7)).place(relx=.5,rely=.7,anchor='center')
        conn.send("ready".encode())
    plys.set(1)

def closeroom():
    print(" Shutting down server.")
    ngrok.kill()
    
def encrypt(message, keypass):
    message = message.encode('utf-8')
    keypass = str(keypass).encode('utf-8')
    encoded = base64.b64encode(message + keypass)
    return encoded.decode('utf-8')

def decrypt(encoded, keypass):
    encoded = encoded.encode('utf-8')
    keypass = str(keypass).encode('utf-8')
    decoded = base64.b64decode(encoded)
    message = decoded[:-len(keypass)].decode('utf-8')
    return message

def jroom(prev):
    current=tk.Toplevel()
    prev.withdraw()
    current.geometry(str(w)+"x"+str(h))
    current.title("New ROOM")
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(prev,current),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')

    tk.Label(current, text="Join room",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(current, text="User ID : ",font=('Helvetica bold', 12)).place(relx=.40,rely=.2,anchor='center')
    mystr = StringVar()
    mystr.set("Enter UID")
    mystr2 = StringVar()
    mystr2.set("Your name here")
    val=IntVar(value=0)
    Entry(current,textvariable=mystr).place(relx=.55, rely=.2, anchor="center")
    tk.Label(current, text="Player Name : ",font=('Helvetica bold', 12)).place(relx=.37,rely=.3,anchor='center')
    name=Entry(current,textvariable=mystr2)
    name.place(relx=.55, rely=.3, anchor="center")
    mystr3 = StringVar()
    mystr3.set("Password")
    passw=Entry(current,textvariable=mystr3,show="*")
    passw.place(relx=.55, rely=.4, anchor="center")
    typval=IntVar(value=0)
    def show():
        if(val.get()==1):passw.config(show='')
        else:passw.config(show='*')
    cbx=tk.Checkbutton(current,text='Show Password',variable=val,onvalue=1,offvalue=0,command=show)
    cbx.place(relx=.70, rely=.4, anchor="center")
    def chngval():
        passw.config(state=cval.get())
        cbx.config(state=cval.get())
        mystr3.set(-1)
    tk.Label(current, text="Password : ",font=('Helvetica bold', 12)).place(relx=.37,rely=.4,anchor='center')
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Join",command=lambda :joinserv(mystr.get(),mystr2.get(),mystr3.get(),typval.get(),current),width=8, bd=5, padx=5, pady=5).place(relx=.5,rely=.7,anchor='center')
    tk.Label(current, text="On/Offline  :",font=('Helvetica bold', 12)).place(relx=.45,rely=.5,anchor='center')
    tk.Checkbutton(current,variable=typval,onvalue=1,offvalue=0,state=DISABLED if flag==0 else NORMAL).place(relx=.55, rely=.5, anchor="center")
    
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(prev,current),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    current.protocol("WM_DELETE_WINDOW",lambda :closecon(current))
    # current.resizable(False,False)
    current.mainloop()
def joinserv(uid,name,passw,typ,prev):
    
    res=requests.get(url+"/joinserver?uid={}&player={}&pass={}&type={}".format(uid,name,encrypt(encrypt(passw,passw),passw),typ))
    if res.ok:
        a=res.json()
        print(a)
        if a["eno"]:
            messagebox.showerror("Error",a['msg'])
            return
        else:
            ip=decrypt(a["code"],passw)
    else:
        messagebox.showerror("Error","API Connection error!")
        return
    current=tk.Toplevel()
    prev.withdraw()
    current.geometry(str(w)+"x"+str(h))
    current.title("Joining.")
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(window,current),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    global con,plys,plyc
    con=IntVar(value=0)
    plys=IntVar(value=0)
    plyc=IntVar(value=0)
    
    def fn1():
        global host,port,server_socket,sc,nt
        sc=tk.Label(current, text="Connecting...",font=('Helvetica bold', 15))
        sc.place(relx=.5,rely=.3,anchor='center')
        host = socket.gethostname()
        l=ip.split(":")
        host = l[1][2:]  # The server's hostname or IP address
        port = int(l[2])
        global csoc
            
        csoc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        csoc.connect((host,port))
        csoc.send(name.encode())
        tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="START",command=lambda :plyc.set(1),width=5, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')

        Thread(target=recvprc,args=(csoc,current)).start()
        Thread(target=sendinc,args=(csoc,current)).start()
        
        sc.destroy()
        sc=tk.Label(current, text="Connection Succesful.",font=('Helvetica bold', 15))
        sc.place(relx=.5,rely=.3,anchor='center')
    # tk.Label(current, text="Creating server..",font=('Helvetica bold', 15)).place(relx=.5,rely=.2,anchor='center')
    print("val",plyc.get())
    print("val",plyc.get())
    current.update_idletasks()
    current.update()
    Thread(target=fn1()).start()
    current.update_idletasks()
    current.update()
    
    def playcall():
        if plys.get()+plyc.get()==2:
            # current.update()
            play(csoc,current,name)
    plys.trace('w',lambda x,y,z: playcall())
    plyc.trace('w',lambda x,y,z: playcall())
    current.mainloop()
    current.protocol("WM_DELETE_WINDOW",lambda :closecon(current,1))
    # current.resizable(False,False)

def recvprc(co,current):
    global plyc,plys,con
    while(1):
        data = co.recv(1024).decode()
        if data=="ready":
            plys.set(1)
            tk.Label(current, text="Player ready,click to start the game",font=('Helvetica bold', 7)).place(relx=.5,rely=.7,anchor='center')
            break
            

def sendinc(co,current):
    global plyc,plys,con
    while 1:
        if plyc.get()==1:
            co.send("ready".encode()) 
            tk.Label(current, text="Waiting for player to start",font=('Helvetica bold', 7)).place(relx=.5,rely=.7,anchor='center')
            break

def play(conn,prev,name,v=0):
    current=tk.Toplevel()
    global can,wall,won,cap
    can=[None,None,None,None,None,None,None,None,None]
    prev.withdraw()
    current.geometry(str(w)+"x"+str(h))
    current.title("LETS PLAY!!!!.")
    global turn,loc,l,b,sr,proc,cor,wallen,tot,wtot,ltot,dtot,chan,rem
    tot=IntVar(value=0)
    wtot=IntVar(value=0)
    ltot=IntVar(value=0)
    dtot=IntVar(value=0)
    chan=IntVar(value=0)
    
    wall=[[255,255,0],[0,255,255],[0,255,0],[0,0,255],[255,0,0]]
    text =[name+"'s Turn","Your Turn","You Won Congratulations!","You Lost LOL!","Draw Match"]
    
    l,b=-1,-1
    turn=IntVar(value=v)
    sr=IntVar(value=-1)
    loc=IntVar(value=-1)
    proc=IntVar(value=0)
    won=IntVar(value=-1)
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(window,current),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    Thread(target=recvturn,args=(conn,)).start()
    Thread(target=sendturn,args=(conn,)).start()
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    midw=camwidth//2
    midh=camheight//2
    wallen=int(min(midw,midh)*3/2)
    ws=midw-wallen//2
    hs=midh-wallen//2
    dis=wallen//3
    tsize=max(len(text[0]),len(text[1]),len(text[2]),len(text[3]),len(text[4]))
    
    tk.Label(current, text="Stats",font=('Helvetica bold', 20)).place(relx=.5,rely=.2,anchor='center')
    # tk.Label(current, text="Total           Won           Lost            Draw",font=('Helvetica bold', 10)).place(relx=.5,rely=.3,anchor='center')
    tk.Label(current, text="Total",font=('Helvetica bold', 10)).place(relx=.37,rely=.27,anchor='center')
    tk.Label(current, text="Won",font=('Helvetica bold', 10)).place(relx=.46,rely=.27,anchor='center')
    tk.Label(current, text="Lost",font=('Helvetica bold', 10)).place(relx=.55,rely=.27,anchor='center')
    tk.Label(current, text="Draw",font=('Helvetica bold', 10)).place(relx=.64,rely=.27,anchor='center')
    tk.Label(current, text="You : ",font=('Helvetica bold', 16)).place(relx=.25,rely=.32,anchor='center')
    tk.Label(current, text=name+" : ",font=('Helvetica bold', 16)).place(relx=.25,rely=.42,anchor='center')
    tk.Label(current, textvariable=tot,font=('Helvetica bold', 16)).place(relx=.37,rely=.32,anchor='center')
    tk.Label(current, textvariable=wtot,font=('Helvetica bold', 16)).place(relx=.46,rely=.32,anchor='center')
    tk.Label(current, textvariable=ltot,font=('Helvetica bold', 16)).place(relx=.55,rely=.32,anchor='center')
    tk.Label(current, textvariable=dtot,font=('Helvetica bold', 16)).place(relx=.64,rely=.32,anchor='center')
    
    tk.Label(current, textvariable=tot,font=('Helvetica bold', 16)).place(relx=.37,rely=.42,anchor='center')
    tk.Label(current, textvariable=ltot,font=('Helvetica bold', 16)).place(relx=.46,rely=.42,anchor='center')
    tk.Label(current, textvariable=wtot,font=('Helvetica bold', 16)).place(relx=.55,rely=.42,anchor='center')
    tk.Label(current, textvariable=dtot,font=('Helvetica bold', 16)).place(relx=.64,rely=.42,anchor='center')
    def chngcam(key,s):
        cv2.waitKey(-1)
        key=s
    
    rem=tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Rematch",command=lambda :rematch(conn),width=5, bd=5, padx=15, pady=5,state="disabled")
    rem.place(relx=.60,rely=.6,anchor='center')
    def remconf(*args):
        if proc.get() == 1:
            rem.config(state="normal")
        else:
            rem.config(state="disabled")
    proc.trace("w",remconf)
    tk.Button(current,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Play/Pause",command=lambda :Thread(target=chngcam,args=(key,ord('p'))).start(),width=5, bd=5, padx=15, pady=5).place(relx=.40,rely=.6,anchor='center')

    for i in range(5):text[i]=text[i].center(tsize)
    # image = cv2.putText(cv2.flip(image, 1),text[turn.get()],(int(midw*19/24),int(midh*1/5)), cv2.FONT_HERSHEY_SIMPLEX, (wallen/300), wall[turn.get()],int(wallen/120), cv2.LINE_AA)
    tsize=cv2.getTextSize(text[0],cv2.FONT_HERSHEY_SIMPLEX, (wallen/300), int(wallen/120))
    cor=[]
    def chanfn(a,b,c):
        print("chan",chan.get())
        if chan.get()==9:
            turn.set(4)
            tot.set(tot.get()+1)
            proc.set(1)
            dtot.set(dtot.get()+1)
    chan.trace("w",chanfn)
    global ax,by
    x=[(ws)/camwidth,(ws+wallen*1/3)/camwidth,(ws+wallen*2/3)/camwidth,(ws+wallen)/camwidth]
    y=[hs/camheight,(hs+wallen*1/3)/camheight,(hs+wallen*2/3)/camheight,(hs+wallen)/camheight]
    ax,by=(wallen/100), int(wallen/120)
    siz= cv2.getTextSize("X",cv2.FONT_HERSHEY_SIMPLEX, ax, by)
    for i in range(len(x)-1):
        for j in range(len(y)-1):
            cor.append((int((x[i+1]+x[i])*camwidth/2)-int(siz[0][0]/2),int((y[j+1]+y[j])*camheight/2)+int(siz[0][1]/2)))
    print(cor)
    # print(siz)
    print(x)
    print(y)
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, camwidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camheight)
    s,u=int(wallen/3),int(wallen/1.5)
    print(s,u)
    # print(siz)
    wonline=[]
    wonline.append(((int(cor[8][0]+siz[0][0]/2),int(y[3]*camheight)),(int(cor[8][0]+siz[0][0]/2),int(y[0]*camheight))))
    wonline.append(((int(cor[5][0]+siz[0][0]/2),int(y[3]*camheight)),(int(cor[5][0]+siz[0][0]/2),int(y[0]*camheight))))
    wonline.append(((int(cor[2][0]+siz[0][0]/2),int(y[3]*camheight)),(int(cor[2][0]+siz[0][0]/2),int(y[0]*camheight))))
    wonline.append(((int(x[3]*camwidth),int(cor[6][1]-siz[0][1]/2)),(int(x[0]*camwidth),int(cor[6][1]-siz[0][1]/2))))
    wonline.append(((int(x[3]*camwidth),int(cor[7][1]-siz[0][1]/2)),(int(x[0]*camwidth),int(cor[7][1]-siz[0][1]/2))))
    wonline.append(((int(x[3]*camwidth),int(cor[8][1]-siz[0][1]/2)),(int(x[0]*camwidth),int(cor[8][1]-siz[0][1]/2))))
    wonline.append(((int(x[3]*camwidth),int(y[0]*camheight)),(int(x[0]*camwidth),int(y[3]*camheight))))
    wonline.append(((int(x[3]*camwidth),int(y[3]*camheight)),(int(x[0]*camwidth),int(y[0]*camheight))))
    
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=2,
        static_image_mode=False,
    ) as hands:
        while cap.isOpened():
            current.update()
            success, image = cap.read()
            key = cv2.waitKey(1)

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            for i in range(wallen):
                t=wall[turn.get()]
                image[hs+s-2][i+ws]=t
                image[hs+s-1][i+ws]=t
                image[hs+s][i+ws]=t
                image[hs+s+1][i+ws]=t
                image[hs+s+2][i+ws]=t
                
                image[hs+u-2][i+ws]=t
                image[hs+u-1][i+ws]=t
                image[hs+u][i+ws]=t
                image[hs+u+1][i+ws]=t
                image[hs+u+2][i+ws]=t
                
                image[i+hs][ws+s-2]=t
                image[i+hs][ws+s-1]=t
                image[i+hs][ws+s]=t
                image[i+hs][ws+s+1]=t
                image[i+hs][ws+s+2]=t
                
                image[i+hs][ws+u-2]=t
                image[i+hs][ws+u-1]=t
                image[i+hs][ws+u]=t
                image[i+hs][ws+u+1]=t
                image[i+hs][ws+u+2]=t
            if won.get()==-1 and chan.get()<9:
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        if turn.get()==1 and won.get()==-1:
                            mx,my=check(hand_landmarks.landmark,x,y)
                            # print("mx my :",mx,my)
                            image = cv2.circle(image, (mx,my), radius=2, color=(0, 0, 255), thickness=-1)
                        # mp_drawing.draw_landmarks(
                        #     image,
                        #     hand_landmarks,
                        #     mp_hands.HAND_CONNECTIONS,
                        #     mp_drawing_styles.get_default_hand_landmarks_style(),
                        #     mp_drawing_styles.get_default_hand_connections_style(),
                        # )
            # if won.get()==0:
            elif chan.get()<9:
                image = cv2.line(image, wonline[won.get()][0], wonline[won.get()][1], [0,0,255], int(wallen/90))

            image = cv2.putText(cv2.flip(image, 1),text[turn.get()],(int(midw-tsize[0][0]/2),int(midh*5/20-tsize[0][1]/2)), cv2.FONT_HERSHEY_SIMPLEX, (wallen/300), wall[turn.get()],int(wallen/120), cv2.LINE_AA)
            for i in range(9):
                if can[i]:draw(image,i,can[i])
            cv2.imshow("Tic Tack Toe", image)
            if key == ord('q'):
                back(window,current,1,1,cap,conn)
                break
            if key == ord('p'):
                print("p")
                cv2.waitKey(-1) #wait until any key is pressed
                print("p dome")
            if cv2.waitKey(5) & 0xFF == 27:
                back(window,current,1,1,cap,conn)
                break
    cap.release()
    cv2.destroyAllWindows()
    
    current.mainloop()
    current.protocol("WM_DELETE_WINDOW",lambda :closecon(current,1))

def rematch(conn):
    global can,chan,turn,won
    can=[None,None,None,None,None,None,None,None,None]
    chan.set(0)
    a=randint(0,1)
    t="rematch:"+str(a)
    conn.send(t.encode())
    # play(conn,current,data,1-a)
    conn.send(t.encode())
    turn.set(1-a)
    sr.set(-1)
    won.set(-1)
    loc.set(-1)
    
def draw(img,n,s):img = cv2.putText(img,s,cor[n], cv2.FONT_HERSHEY_SIMPLEX, ax,wall[turn.get()],by, cv2.LINE_AA)
    
def check(a,x,y):
    global wall
    cx,cy=(a[5].x+a[17].x+a[0].x+a[1].x)/4,(a[5].y+a[17].y+a[0].y+a[1].y)/4
    f=(a[8].y+a[12].y+a[16].y+a[20].y)-(a[5].y+a[17].y+a[13].y+a[1].y)
    if(f>0):
        global l,b
        if cx>=x[0] and cx<=x[1] and l!=1 and cy<=y[3] and cy>=y[0]:l=1
        elif cx>=x[1] and cx<=x[2] and l!=2 and cy<=y[3] and cy>=y[0]:l=2
        elif cx>=x[2] and cx<=x[3] and l!=3 and cy<=y[3] and cy>=y[0]:l=3
        if cy>=y[0] and cy<=y[1] and b!=1 and cx<=x[3] and cx>=x[0]:b=1
        elif cy>=y[1] and cy<=y[2] and b!=2 and cx<=x[3] and cx>=x[0]:b=2
        elif cy>=y[2] and cy<=y[3] and b!=3 and cx<=x[3] and cx>=x[0]:b=3
        k=loc.get()
        if l==1 and b==1:loc.set(6)
        elif l==1 and b==2:loc.set(7)
        elif l==1 and b==3:loc.set(8)
        elif l==2 and b==1:loc.set(3)
        elif l==2 and b==2:loc.set(4)
        elif l==2 and b==3:loc.set(5)
        elif l==3 and b==1:loc.set(0)
        elif l==3 and b==2:loc.set(1)
        elif l==3 and b==3:loc.set(2)
        t=loc.get()
        if t!=k:
            if can[t] is None:
                can[t]="X"
                sr.set(t)
                if chkwin(t):
                    turn.set(2)
                    print("winnner")
            print(t)
    return(int(cx*camwidth),int(cy*camheight))

def chkwin(n):
    global can,won
    if n==0:
        if can[0]==can[1] and can[1]==can[2]:
            print("won 0")
            won.set(0)
            return(1)
        elif can[0]==can[3] and can[3]==can[6]:
            print("won 3")
            won.set(3)
            return(1)
        elif can[0]==can[4] and can[4]==can[8]:
            print("won 6")
            won.set(6)
            return(1)
    elif n==1:
        if can[1]==can[0] and can[0]==can[2]:
            print("won 0")
            won.set(0)
            return(1)
        elif can[1]==can[4] and can[4]==can[7]:
            print("won 4")
            won.set(4)
            return(1)
    elif n==2:
        if can[2]==can[1] and can[1]==can[0]:
            print("won 0")
            won.set(0)
            return(1)
        elif can[2]==can[5] and can[5]==can[8]:
            print("won 5")
            won.set(5)
            return(1)
        elif can[2]==can[4] and can[4]==can[6]:
            print("won 7")
            won.set(7)
            return(1)
    elif n==3:
        if can[3]==can[0] and can[0]==can[6]:
            print("won 3")
            won.set(3)
            return(1)
        elif can[3]==can[4] and can[4]==can[5]:
            print("won 1")
            won.set(1)
            return(1)
    elif n==4:
        if can[3]==can[4] and can[4]==can[5]:
            print("won 1")
            won.set(1)
            return(1)
        elif can[1]==can[4] and can[4]==can[7]:
            print("won 4")
            won.set(4)
            return(1)
        elif can[0]==can[4] and can[4]==can[8]:
            print("won 6")
            won.set(6)
            return(1)
        elif can[6]==can[4] and can[4]==can[2]:
            print("won 7")
            won.set(7)
            return(1)
    elif n==5:
        if can[5]==can[3] and can[4]==can[5]:
            print("won 1")
            won.set(1)
            return(1)
        elif can[5]==can[2] and can[2]==can[8]:
            print("won 5")
            won.set(5)
            return(1)
    elif n==6:
        if can[6]==can[4] and can[4]==can[2]:
            print("won 7")
            won.set(7)
            return(1)
        elif can[6]==can[3] and can[3]==can[0]:
            print("won 3")
            won.set(3)
            return(1)
        elif can[6]==can[7] and can[7]==can[8]:
            print("won 2")
            won.set(2)
            return(1)
    elif n==7:
        if can[7]==can[1] and can[1]==can[4]:
            print("won 4")
            won.set(4)
            return(1)
        elif can[7]==can[8] and can[8]==can[6]:
            print("won 2")
            won.set(2)
            return(1)
    elif n==8:
        if can[8]==can[5] and can[5]==can[2]:
            print("won 5")
            won.set(5)
            return(1)
        elif can[8]==can[7] and can[7]==can[6]:
            print("won 2")
            won.set(2)
            return(1)
        elif can[8]==can[4] and can[4]==can[0]:
            print("won 6")
            won.set(6)
            return(1)

def recvturn(co):
    global can
    while 1:
        d=co.recv(1024).decode()
        if d:
                # print(d)
            if d[:4]=="turn":
                turn.set(int(d[5]))
            elif d[:2]=="pl":
                turn.set(1)
                can[int(d[3])]="O"
                chan.set(chan.get()+1)
                # print(can)
            elif d[:3]=="won":
                turn.set(3)
                can[int(d[4])]="O"
                won.set(int(d[6]))
                print("Winner lol",d)
                proc.set(1)
                tot.set(tot.get()+1)
                ltot.set(ltot.get()+1)
                chan.set(chan.get()+1)
            elif d[:7]=="rematch":
                turn.set(int(d[8]))
                can=[None,None,None,None,None,None,None,None,None]
                chan.set(0)
                sr.set(-1)
                won.set(-1)
                loc.set(-1)
            elif d[:4]=="quit":
                global cap
                cap.release()
                cv2.destroyAllWindows()
                break
def sendturn(co):
    while(1):
        if sr.get()>-1 and won.get()==-1 and chan.get()<9:
            # print("world")
            # print("pl:{}".format(sr.get()))
            co.send(("pl:{}".format(sr.get())).encode())
            sr.set(-1)
            turn.set(0)
            
            chan.set(chan.get()+1)
        elif sr.get()>-1 and won.get()!=-1 and chan.get()<9:
            co.send(("won:{}:{}".format(sr.get(),won.get())).encode())
            wtot.set(wtot.get()+1)
            proc.set(1)
            tot.set(tot.get()+1)
            chan.set(chan.get()+1)
            sr.set(-1)
            # turn.set(0)
        
init()
# play(0,0,"jkihj",1)