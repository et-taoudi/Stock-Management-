from tkinter import *
import mysql.connector
from tkinter import messagebox
from subprocess import call

login = Tk()

#Function GetStarted with calling Mysql Database
def GetStarted():
    mysqldb=mysql.connector.connect(host='localhost',port='3307', user='root', password='', database='estellantis')
    mycursor = mysqldb.cursor()
    identifier=id.get()
    password=pw.get()

    sql='select * from admin where id_admin = %s and mdp_admin = %s'
    mycursor.execute(sql, [(identifier),(password)])
    results = mycursor.fetchall()
    if results:
        login.destroy()
        call(["python","Home.py"])
        return True
    else:
        messagebox.showinfo("Error","Incorrect Username and Password")
        return False
#*********************************************************************************

#Function Show and Hide Password
def Show_Hide_Pw () :
    if pw['show'] == '*':
        pw.configure(show='')

    else :
        pw.configure(show='*')
#***********************************************


#Caractéristiques de la fenêtre LoginPage
def win2():
   login.configure(bg = "#83a6fa")
   login.title("G-Stock Stellantis PSA Group")
   login.iconbitmap(r'img/Logo.ico')
   # Place the LoginPage in the center of the screen
   x = login.winfo_screenwidth() // 6
   y = int(login.winfo_screenheight() * 0.05)
   login.geometry("1001x726+" + str(x) + '+' + str(y))
   # ************************************************
#******************
canvas = Canvas(
    login,
    bg = "#83a6fa",
    height = 726,
    width = 1001,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)


#Background Image
background_img = PhotoImage(file = f"img/LoginPageBG.png")
background = canvas.create_image(
    500, 362,
    image=background_img)
#*******************************************************

#Hidden Password Image
hidden_img = PhotoImage(file = f"img/hidden_img.png")
hidden = Button(
    image = hidden_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = Show_Hide_Pw,
    relief = "flat")

hidden.place(
    x = 870, y = 390,
    width = 28,
    height = 23)
#*************************************************

#Identifier TextBox
def on_enter(e):
    id.delete(0,'end')

def on_leave(e):
    identifier=id.get()
    if identifier == '' :
        id.insert(0,'Identifier')

id = Entry(border=0,width=20,fg='#0500ff',bg='white',font=('Inter-Light',16))
id.place(x=520,y=310)
id.insert(0,'Identifier')

id.bind('<FocusIn>', on_enter)
id.bind('<FocusOut>', on_leave)
#*************************************************************

#Password TextBox
def on_enter(e):
    pw.delete(0,'end')

def on_leave(e):
    password=pw.get()
    if password == '' :
        pw.insert(0,'Password')

pw = Entry(border=0,width=20,fg='#0500ff',bg='white',font=('Inter-Light',16), show='*')
pw.place(x=520,y=390)
pw.insert(0,'Password')

pw.bind('<FocusIn>', on_enter)
pw.bind('<FocusOut>', on_leave)
#*************************************************************

#Get Started Button
GetStarted_img = PhotoImage(file = f"img/GetStarted_img.png")
signin = Button(
    image = GetStarted_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = GetStarted,
    relief = "flat")

signin.place(
    x = 620, y = 490,
    width = 181,
    height = 58)
#**********************************************

#Run Application
win2()
login.resizable(False, False)
login.mainloop()
#*************************************************
