from tkinter import *
from tkinter import messagebox
import mysql.connector
from subprocess import call
from datetime import date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


#Connexion with DATABASE*******************************
def connection():
    conn=mysql.connector.connect(
        host='localhost',port='3307', user='root', password='', database='estellantis'
    )
    return conn
#******************************************************************************

#Functions**********************************************************************

#Show Plot
def showPlot():
    conn = connection()
    cursor = conn.cursor()
    # Fecthing Data From mysql to my python progame
    cursor.execute("select qteEnStock_prod,réf_prod from produit")
    result = cursor.fetchall

    Références = []
    Quantités = []

    for i in cursor:
        Références.append(i[0])
        Quantités.append(i[1])

    print("Reference of product = ", Quantités)
    print("Quantity in stock = ",Références)

    # Visulizing Data using Matplotlib
    # Define plot space
    figure=Figure(dpi=80)
    figure_canvas=FigureCanvasTkAgg(figure,home)
    axes=figure.add_subplot()
    axes.plot(Quantités, Références,marker='o',color='#7221FF')
    axes.set_title('Stock Evolution', fontsize = 12)
    axes.set_ylabel('Quantity in stock')
    axes.set_xlabel('Reference of product')
    axes.set_xticklabels(labels=Quantités,rotation=(90), fontsize=9, va='bottom', ha='left')
    figure_canvas.get_tk_widget().pack()
    figure_canvas.get_tk_widget().place(x=134,y=360,width=800,height=300)


#******************************************************

#Fonction pour avoir le nombre dotation effectuée au total
def NDotation():
    lbl2.delete(0, END)

    conn = connection()
    cursor = conn.cursor()

    sql=("SELECT count(*) FROM dotation")
    val = ()
    cursor.execute(sql, val)

    result = cursor.fetchone()
    found = result[0]

    lbl2.insert(0, found)
#**********************************************************************
#Fonction pour avoir le nombre dotation effectuée aujourd'hui
def NDotation1():
    lbl3.delete(0, END)
    now = date.today()
    dt_string = now.strftime("%Y-%m-%d")

    conn = connection()
    cursor = conn.cursor()

    sql=("SELECT count(*) FROM dotation WHERE date_dot LIKE '%"+dt_string+"%'")
    val = ()
    cursor.execute(sql, val)

    result = cursor.fetchone()
    found = result[0]
    lbl3.config(state="normal")
    lbl3.insert(0, found)
    lbl3.insert(END, " aujourd'hui")
    lbl3.config(state="disabled")


#**********************************************************************
#Fonction pour avoir la valeur du stock
def NStock():
    lbl1.delete(0, END)

    conn = connection()
    cursor = conn.cursor()

    sql=("SELECT SUM(prix) FROM commande")
    val = ()
    cursor.execute(sql, val)

    result = cursor.fetchone()
    found = result[0]

    lbl1.insert(0, found)
#**********************************************************************

#Fonction pour avoir le nombre de commande
def NCommande():
    lbl4.delete(0, END)

    conn = connection()
    cursor = conn.cursor()

    sql=("SELECT count(*) FROM contenir")
    val = ()
    cursor.execute(sql, val)

    result = cursor.fetchone()
    found = result[0]

    lbl4.insert(0, found)
#**********************************************************************
#Fonction pour accéder à la page Dotations****************************
def toDotations():
    home.destroy()
    call(["python", "Dotations.py"])
#*********************************************************************

#Fonction pour accéder à la page Profile****************************
def toProfile():
    home.destroy()
    call(["python", "Profile.py"])
#*********************************************************************



#Fonction pour accéder à la page Admins****************************
def toProducts():
    home.destroy()
    call(["python", "Products.py"])
#*********************************************************************

#Fonction pour accéder à la page Suppliers****************************
def toSuppliers():
    home.destroy()
    call(["python", "Suppliers.py"])
#*********************************************************************


#Fonction pour exiter****************************
def LogOut():
    if messagebox.askyesno("Confirm Please", "Are you sure you want to exit the application ?"):
        home.destroy()
    else :
        return True
#*********************************************************************
def btn_clicked():
    print("Button Clicked")


home = Tk()
home.geometry("1065x750")
home.configure(bg = "#e1f7fe")
home.title("G-Stock Stellantis PSA Group - Dashboard -")
home.iconbitmap(r'img/Logo.ico')

#Place the LoginPage in the center of the screen
x =home.winfo_screenwidth()//7
y = int(home.winfo_screenheight() * 0.030)
home.geometry("1065x750+"+str(x)+'+'+str(y))
#************************************************

canvas = Canvas(
    home,
    bg = "#e1f7fe",
    height = 750,
    width = 1065,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)


#Background Image Dotations Page
background_img = PhotoImage(file = f"img/HomeBG.png")
background = canvas.create_image(
    520, 370,
    image=background_img)
#***********************************************************


#Profile Image *******************************************
img0 = PhotoImage(file = f"img/profile.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = toProfile,
    relief = "flat")

b0.place(
    x = 875, y = 105,
    width = 34,
    height = 34)
#**********************************************************


canvas.create_text(
    800, 122,
    text = "Farhate Elatoui",
    fill = "#0500ff",
    font = ("None", int(11)))

#Dashboard Button Menu************************************
img3 = PhotoImage(file = f"img/Dashboard_Menu_On.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 84, y = 215,
    width = 35,
    height = 48)
#*********************************************************


#Dotations Button Menu************************************
img4 = PhotoImage(file = f"img/Dotations_Menu_Off.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = toDotations,
    relief = "flat")

b4.place(
    x = 87, y = 271,
    width = 25,
    height = 25)
#**********************************************************


#Products Button Menu**************************************
img5 = PhotoImage(file = f"img/Products_Menu.png")
b5 = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = toProducts,
    relief = "flat")

b5.place(
    x = 87, y = 320,
    width = 24,
    height = 24)
#**********************************************************


#Fournisseurs Button Menu**********************************
img6 = PhotoImage(file = f"img/Fournisseurs_Menu_Off.png")
b6 = Button(
    image = img6,
    borderwidth = 0,
    highlightthickness = 0,
    command = toSuppliers,
    relief = "flat")

b6.place(
    x = 89, y = 370,
    width = 24,
    height = 24)
#**********************************************************


#Admins Button Menu*****************************************
img7 = PhotoImage(file = f"img/Admins_Menu.png")
b7 = Button(
    image = img7,
    borderwidth = 0,
    highlightthickness = 0,
    command = toSuppliers,
    relief = "flat")

b7.place(
    x = 89, y = 415,
    width = 22,
    height = 28)
#***********************************************************

#LogOut Button**********************************************
img8 = PhotoImage(file = f"img/LogOut.png")
b8 = Button(
    image = img8,
    borderwidth = 0,
    highlightthickness = 0,
    command = LogOut,
    relief = "flat")

b8.place(
    x = 110, y = 635,
    width = 21,
    height = 22)
#***********************************************************

#Support Menu **********************************************
img9 = PhotoImage(file = f"img/Support.png")
b9 = Button(
    image = img9,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b9.place(
    x = 450, y = 115,
    width = 85,
    height = 25)
#***********************************************************

#My Account Menu********************************************
img10 = PhotoImage(file = f"img/MyAcc.png")
b10 = Button(
    image = img10,
    borderwidth = 0,
    highlightthickness = 0,
    command = toProfile,
    relief = "flat")

b10.place(
    x = 550, y = 112,
    width = 85,
    height = 25)
#************************************************************

#Home Menu**************************************************
img11 = PhotoImage(file = f"img/Home.png")
b11 = Button(
    image = img11,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b11.place(
    x = 380, y = 115,
    width = 56,
    height = 25)
#***********************************************************

#Total number dotation in day report
lbl1=Entry(home,bg='white',border=0,font=("Inter-Bold", int(17)),width=11)
lbl1.place(x=188,y=232)

lbl2=Entry(home,bg='white',border=0,font=("Inter-Bold", int(17)),width=11)
lbl2.place(x=440,y=232)

lbl3=Entry(home,bg='white',border=0,font=("Bold", int(10)),width=11)
lbl3.place(x=440,y=312)

lbl4=Entry(home,bg='white',border=0,font=("Bold", int(17)),width=11)
lbl4.place(x=696,y=232)
#***********************************************************************

NStock()
NDotation()
NDotation1()
NCommande()
showPlot()

home.resizable(False, False)
home.mainloop()
