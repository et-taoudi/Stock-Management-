from tkinter import *
from tkinter import messagebox
import tkinter as tk
import mysql.connector
from tkinter import filedialog
import os
from PIL import Image, ImageTk


#Connexion with DATABASE*******************************
def connection():
    conn=mysql.connector.connect(
        host='localhost',port='3307', user='root', password='', database='estock'
    )
    return conn
#******************************************************************************

#Fonction pour remplir le formulaire**********************************
def Remplir():
    conn=connection()
    cursor=conn.cursor()
   # try :
        #sql="SELECT * FROM admin id_admin=%s"
   # except Exception(e):
# Fonction pour afficher les données de produits la base de données dans un tableau
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM admin id_admin='SD29390'")
    records = cursor.fetchone()
    print(records)
    for record in records:
        p_records1=str(record)
        Identifier.insert(0,p_records1)

# ------------------------------------------------------------------------------



#Fonction update------------------------------------------------------------
def Update():
    Id=Identifier.get()
    FN = FName.get()
    LN= LName.get()
    Pass = Mdp.get()
    TL=Tél.get()
    Mail=Email.get()

    conn = connection()
    cursor = conn.cursor()

    try :
        sql="UPDATE admin SET nom_admin=%s, prénom_sal=%s, mdp_admin=%s, tél_admin=%s,email_admin=%s WHERE id_admin=%s"
        val=(LN,FN,Pass,TL,Mail,Id)
        cursor.execute(sql, val)

        conn.commit()
        lastid = cursor.lastrowid
        messagebox.showinfo("Information", "Profile updated successfully...!!")

        Id.delete(0, END)
        FN.delete(0, END)
        LN.delete(0, END)
        Pass.delete(0, END)
        TL.delete(0, END)
        Mail.delete(0, END)

        Id.focus_set()

    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
#*******************************************************************************

#Fonction pour accéder aux images dans notre pc
def showImage() :
    try :
        path=filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image File",filetypes=(("JPG File","*.jpg"),("PNG File",'+.png'),("All Files,*.*")))
        img = Image.open(path)
        print("\t\t\t\t",path)
        img.thumbnail((150,150))
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img)
        lbl.image=img
        lbl1.configure(text=path)
    except ValueError:
        tk.messagebox.showerror("Information","The file you have chosen is invalid")
    except FileNotFoundError:
        tk.messagebox.showerror("Information",f"No such file as {path}")
        return None
#*********************************************************************

#Function to save the image in Mysql database
ID="SD29390"
def InsertImage(path):
    with open(path,'rb') as File:
        BinaryData = File.read()

    conn = connection()
    cursor = conn.cursor()

    sql="UPDATE admin SET photo_admin=%s WHERE id_admin=%s"
    val = ( (BinaryData, ), ID)
    cursor.execute(sql, val)

    conn.commit()

def retrieveBlob(ID):
    conn = connection()
    cursor = conn.cursor()
    sql="SELECT * FROM admin WHERE id='{0}'"
    cursor.execute(sql.format(str(ID)))
    result=cursor.fetchone()[1]
    StoreFilePath ="ImageOutputs/img{0}.jpg".format(str(ID))
    print(result)
    with open(StoreFilePath,"wb") as File:
        File.write((result))
        File.close()

    conn.commit()

#*****************************************
def btn_clicked():
    print("Button Clicked")


profile = Tk()

profile.geometry("1065x750")
profile.configure(bg = "#e1f7fe")
profile.title("G-Stock Stellantis PSA Group")
profile.iconbitmap(r'img/Logo.ico')

#Place the LoginPage in the center of the screen
x = profile.winfo_screenwidth()//7
y = int(profile.winfo_screenheight() * 0.030)
profile.geometry("1065x750+"+str(x)+'+'+str(y))
#************************************************

canvas = Canvas(
    profile,
    bg = "#e1f7fe",
    height = 750,
    width = 1065,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"img/ProfileBG.png")
background = canvas.create_image(
     520, 400,
    image=background_img)


#Dashboard Button Menu************************************
img3 = PhotoImage(file = f"img/Dashboard_Menu.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 87, y = 220,
    width = 23,
    height = 23)
#*********************************************************


#Dotations Button Menu************************************
img4 = PhotoImage(file = f"img/Dotations_Menu_Off.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b4.place(
    x = 87, y = 269,
    width = 25,
    height = 25)
#**********************************************************


#Products Button Menu**************************************
img5 = PhotoImage(file = f"img/Products_Menu.png")
b5 = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b5.place(
    x = 87, y = 319,
    width = 24,
    height = 24)
#**********************************************************


#Fournisseurs Button Menu**********************************
img6 = PhotoImage(file = f"img/Fournisseurs_Menu.png")
b6 = Button(
    image = img6,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b6.place(
    x = 87, y = 370,
    width = 24,
    height = 24)
#**********************************************************


#Admins Button Menu*****************************************
img7 = PhotoImage(file = f"img/Admins_Menu.png")
b7 = Button(
    image = img7,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b7.place(
    x = 88, y = 415,
    width = 24,
    height = 24)
#***********************************************************

#LogOut Button**********************************************
img8 = PhotoImage(file = f"img/LogOut.png")
b8 = Button(
    image = img8,
    borderwidth = 0,
    highlightthickness = 0,
    command = profile.destroy,
    relief = "flat")

b8.place(
    x = 887, y = 600,
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
    x = 450, y = 121,
    width = 85,
    height = 25)
#***********************************************************

#My Account Menu********************************************
img10 = PhotoImage(file = f"img/MyAcc.png")
b10 = Button(
    image = img10,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b10.place(
    x = 550, y = 120,
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
    x = 380, y = 120,
    width = 56,
    height = 25)
#***********************************************************




#Profile Image *******************************************
img0 = PhotoImage(file = f"img/profile.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 870, y = 115,
    width = 34,
    height = 34)
#**********************************************************

canvas.create_text(
    800, 132,
    text = "Farhate Elatoui",
    fill = "#0500ff",
    font = ("None", int(11.0)))

#Edit Profile Button Image Browser ***************
lbl=Label(profile,bg='white')
lbl.pack
lbl.place(x=170,y=300)
lbl1=Label(profile,bg='white')
lbl1.pack
lbl1.place(x=250,y=520)
img13 = PhotoImage(file = f"img/EditProfile.png")
b13 = Button(
    image = img13,
    borderwidth = 0,
    highlightthickness = 0,
    command = showImage,
    relief = "flat")

b13.place(
    x = 275, y = 450,
    width = 22,
    height = 22)
#***************************************

#Save Changes Button****************
img14 = PhotoImage(file = f"img/Save.png")
b14 = Button(
    image = img14,
    borderwidth = 0,
    highlightthickness = 0,
    command = Update,
    relief = "flat")

b14.place(
    x = 798, y = 515,
    width = 96,
    height = 40)
#***************************************

#Edit Form***********************************************************************************
Identifier=Entry(profile,width=15,fg='#0500ff',bg='#F6FAFF',font=('Inter-Light',10),border=0)
Identifier.place(x=380,y=300,height=20)
Identifier.insert(0,'Yes')

FName=Entry(profile,width=15,fg='#0500ff',bg='#F6FAFF',font=('Inter-Light',16),border=0)
FName.place(x=380,y=370,height=20)

LName=Entry(profile,width=15,fg='#0500ff',bg='#F6FAFF',font=('Inter-Light',16),border=0)
LName.place(x=382,y=440,height=20)

Mdp=Entry(profile,width=15,fg='#0500ff',bg='#F6FAFF',font=('Inter-Light',16),border=0)
Mdp.place(x=650,y=300,height=20)

Tél=Entry(profile,width=15,fg='#0500ff',bg='#F6FAFF',font=('Inter-Light',16),border=0)
Tél.place(x=650,y=370,height=20)

Email=Entry(profile,width=15,fg='#0500ff',bg='#F6FAFF',font=('Inter-Light',16),border=0)
Email.place(x=650,y=440,height=20)
#*******************************************************************************************

profile.resizable(False, False)
profile.mainloop()
