from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from subprocess import call
import pandas as pd



#Connexion with DATABASE*******************************
def connection():
    conn=mysql.connector.connect(
        host='localhost',port='3307', user='root', password='', database='estellantis'
    )
    return conn
#******************************************************************************

#Functions**********************************************************************


#Export data to Excel File**************************************************
def ExportExcel():

    conn = connection()
    cursor = conn.cursor()

    sql="SELECT * FROM fournisseur "
    df = pd.read_sql(sql,conn )

    df.to_excel('C:\ExportExcel.xlsx',index=False,header=['ID', 'Nom','Tél','Email','Adresse'])
    messagebox.showinfo("Information", "An Excel File was genrated successfully in C:\ExportExcel.xlsx")
    df = pd.read_excel('C:\ExportExcel.xlsx')

#*****************************************************************************

#Fonction pour cleaner les textbox************************************
def Clean():
    id.delete(0, END)
    nom.delete(0, END)
    tél.delete(0, END)
    mail.delete(0, END)
    add.delete(0, END)
#********************************************************************


#Fonction pour rechercher un produit selon les données dans la barre de recherche************************************
def Research():
    rechercher = str(rech.get())

    conn = connection()
    cursor = conn.cursor()

    if rechercher=="":
        messagebox.showinfo("Information", "Please fill in the search field to find a supplier!!")
        showTable()
    else :

        try:

            sql = "SELECT id_fourn AS 'Identifier',nomcomplet_fourn AS 'Name',tél_fourn AS 'Phone_number',email_fourn AS 'Email',adresse_fourn AS 'Address' FROM fournisseur WHERE id_fourn LIKE '%"+rechercher+"%' OR nomcomplet_fourn LIKE '%"+rechercher+"%' OR tél_fourn LIKE '%"+rechercher+"%' OR email_fourn LIKE '%"+rechercher+"%' OR adresse_fourn LIKE '%"+rechercher+"%'"
            val = ()
            cursor.execute(sql, val)

            for records in listBox.get_children():
                listBox.delete(records)

            records = cursor.fetchall()
            print(records)

            for i, (Identifier,Name,Phone_Number,Email,Address) in enumerate(records,start=1):
                listBox.insert("", "end", values=(Identifier,Name,Phone_Number,Email,Address))
                conn.close()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
#********************************************************************

#Fonction pour afficher les données de la base de données dans un tableau
def showTable() :
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_fourn AS 'Identifier',nomcomplet_fourn AS 'Name',tél_fourn AS 'Phone_number',email_fourn AS 'Email',adresse_fourn AS 'Address' FROM fournisseur")
    records = cursor.fetchall()
    print(records)

    for i,(Identifier,Name,Phone_Number,Email,Address) in enumerate(records,start=1) :
        listBox.insert("","end",values=(Identifier,Name,Phone_Number,Email,Address))
        conn.close()
#------------------------------------------------------------------------------

#Fonction pour rafraichir les données du tableau************************************
def Refresh():
    for records in listBox.get_children():
        listBox.delete(records)
    showTable()
#********************************************************************

#Fonction pour ajouter un nouveau admin-------------------------------
def Add():
    numéro=id.get()
    name=nom.get()
    télé=tél.get()
    email=mail.get()
    address= add.get()

    if numéro=="":
        messagebox.showinfo("Information", "Please insert a Supplier ID to add a new supplier !!")
    if ((name == "") or (télé == "")):
        messagebox.showinfo("Information", "Please fill all the textbox !!!")
    else :
        conn = connection()
        cursor = conn.cursor()


        sql1="SELECT count(*) FROM fournisseur WHERE id_fourn=%s"
        val1=(numéro,)
        cursor.execute(sql1, val1)
        result = cursor.fetchone()
        found=result[0]

        try :

            if found == 0:

                sql="INSERT INTO fournisseur VALUES (%s,%s,%s,%s,%s)"
                val=(numéro,name,télé,email,address)
                cursor.execute(sql,val)

                conn.commit()
                lastid=cursor.lastrowid
                messagebox.showinfo("Information","Supplier inserted successfully...!!")
                Refresh()

                numéro.delete(0,END)
                name.delete(0, END)
                télé.delete(0,END)
                email.delete(0,END)
                address.delete(0, END)

                id.focus_set()
            else :
                messagebox.showinfo("Information","Supplier ID already exist. Try with another!!")

        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()

#----------------------------------------------------------------------------


#Fonction Delete***********************************************
def delete():
    numéro=id.get()

    conn = connection()
    cursor = conn.cursor()

    if messagebox.askyesno("Confirm Please","Are you sure you want to delete this supplier ?"):
        try:
            sql1 = "DELETE FROM fournisseur WHERE id_fourn=%s"
            val1 = (numéro,)
            cursor.execute(sql1, val1)

            conn.commit()
            lastid = cursor.lastrowid
            messagebox.showinfo("Information", "Supplier deleted successfully...!!")
            Refresh()

            id.delete(0, END)
            id.focus_set()

        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
    else :
        return True
#*********************************************************************************************

#Fonction pour remplir les champs avec les données de la ligne séléctionnée depuis le tableau
def Remplir(event):
    id.delete(0,END)
    nom.delete(0, END)
    tél.delete(0,END)
    mail.delete(0,END)
    add.delete(0, END)

    row_id=listBox.selection()[0]
    select=listBox.set(row_id)

    id.insert(0,select['Identifier'])
    nom.insert(0, select['Name'])
    tél.insert(0,select['Phone_Number'])
    mail.insert(0,select['Email'])
    add.insert(0, select['Address'])
#***********************************************************************************************

#Fonction pour accéder à la page Dotations****************************
def toDotations():
    supplier.destroy()
    call(["python", "Dotations.py"])
#*********************************************************************

#Fonction pour accéder à la page Profile****************************
def toProfile():
    supplier.destroy()
    call(["python", "Profile.py"])
#*********************************************************************

#Fonction pour accéder à la page Dashboard****************************
def toHome():
    supplier.destroy()
    call(["python", "Home.py"])
#*********************************************************************

#Fonction pour accéder à la page Produits****************************
def toProducts():
    supplier.destroy()
    call(["python", "Products.py"])
#*********************************************************************

#Fonction pour accéder à la page Admins****************************
def toAdmins():
    supplier.destroy()
    call(["python", "Admins.py"])
#*********************************************************************
#Fonction pour exiter****************************
def LogOut():
    if messagebox.askyesno("Confirm Please", "Are you sure you want to exit the application ?"):
        supplier.destroy()
    else :
        return True
#*********************************************************************
def btn_clicked():
    print("Button Clicked")


supplier = Tk()
supplier.geometry("1065x750")
supplier.configure(bg = "#e1f7fe")
supplier.title("G-Stock Stellantis PSA Group - Suppliers -")
supplier.iconbitmap(r'img/Logo.ico')

#Place the LoginPage in the center of the screen
x = supplier.winfo_screenwidth()//7
y = int(supplier.winfo_screenheight() * 0.030)
supplier.geometry("1065x750+"+str(x)+'+'+str(y))
#************************************************

canvas = Canvas(
    supplier,
    bg = "#e1f7fe",
    height = 750,
    width = 1065,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)


#Background Image Dotations Page
background_img = PhotoImage(file = f"img/SuppliersBG.png")
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
    x = 875, y = 83,
    width = 34,
    height = 34)
#**********************************************************


canvas.create_text(
    800, 105,
    text = "Farhate Elatoui",
    fill = "#0500ff",
    font = ("None", int(11)))

#Export to Excel Button **********************************
img1 = PhotoImage(file = f"img/Export.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    background='white',
    command = ExportExcel,
    relief = "flat")

b1.place(
    x = 630, y = 168,
    width = 124,
    height = 35)
#*********************************************************

#Refresh Table Button**********************************
img2 = PhotoImage(file = f"img/refreshTable.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command =Refresh,
    relief = "flat")

b2.place(
    x = 770, y = 167,
    width = 121,
    height = 35)
#*********************************************************


#Dashboard Button Menu************************************
img3 = PhotoImage(file = f"img/Dashboard_Menu.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = toHome,
    relief = "flat")

b3.place(
    x = 87, y = 190,
    width = 23,
    height = 23)
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
    x = 86, y = 236,
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
    x = 87, y = 289,
    width = 24,
    height = 24)
#**********************************************************


#Fournisseurs Button Menu**********************************
img6 = PhotoImage(file = f"img/Fournisseurs_Menu_On.png")
b6 = Button(
    image = img6,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b6.place(
    x = 79, y = 330,
    width = 42,
    height = 42)
#**********************************************************


#Admins Button Menu*****************************************
img7 = PhotoImage(file = f"img/Admins_Menu.png")
b7 = Button(
    image = img7,
    borderwidth = 0,
    highlightthickness = 0,
    command = toAdmins,
    relief = "flat")

b7.place(
    x = 88, y = 385,
    width = 22,
    height = 22)
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
    x = 889, y = 650,
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
    x = 450, y = 95,
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
    x = 550, y = 93,
    width = 85,
    height = 25)
#************************************************************

#Home Menu**************************************************
img11 = PhotoImage(file = f"img/Home.png")
b11 = Button(
    image = img11,
    borderwidth = 0,
    highlightthickness = 0,
    command = toHome,
    relief = "flat")

b11.place(
    x = 380, y = 95,
    width = 56,
    height = 25)
#***********************************************************


#Add Button****************************************************
img12 = PhotoImage(file = f"img/Add.png")
b12 = Button(
    image = img12,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command = Add,
    relief = "flat")

b12.place(
    x = 660, y = 505,
    width = 131,
    height = 44)
#************************************************************


#Delete Button**************************************************
img14 = PhotoImage(file = f"img/Delete.png")
b14 = Button(
    image = img14,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command = delete,
    relief = "flat")

b14.place(
    x = 550, y = 505,
    width = 131,
    height = 44)
#*************************************************************

#Clean Butoon***************************************
img18 = PhotoImage(file = f"img/Clean.png")
b18 = Button(
    image = img18,
    borderwidth = 0,
    highlightthickness = 0,
    command = Clean,
    relief = "flat")

b18.place(
    x = 795, y = 510,
    width = 92,
    height = 36)
#***************************************************

#Search Button***************************************
img19 = PhotoImage(file = f"img/Search.png")
b19 = Button(
    image = img19,
    borderwidth = 0,
    highlightthickness = 0,
    command = Research,
    relief = "flat")

b19.place(
    x = 375, y = 229,
    width = 44,
    height = 16)
#****************************************************

#Champs Pour Ajouter une nouvelle dotation
id= Entry(supplier)
id.place(x=160,y=590)

nom = Entry(supplier)
nom.place(x=310,y=590)

tél = Entry(supplier)
tél.place(x=460,y=590)

mail= Entry(supplier)
mail.place(x=610,y=590)

add= Entry(supplier)
add.place(x=760,y=590)
#*********************************************************************



#Tableau Admins******************************************************
cols=("Identifier","Name","Phone_Number","Email","Address")
listBox=ttk.Treeview(supplier, columns=cols, show='headings')

for col in cols :
    listBox.heading(col,text=col)
    listBox.grid(row=1,column=0,columnspan=2)
    listBox.place(x=150,y=270,width=750)

    listBox.column(0,width=30)
    listBox.column(1, width=70)
    listBox.column(2, width=60)
    listBox.column(3, width=60)
    listBox.column(4, width=150)


#**********************************************************************

#Search label****************************
rech=Entry(supplier,width=28,fg='#0500ff',bg='#EEEEFF',border=0)
rech.place(x=200,y=228)
#*****************************************************************

showTable()
listBox.bind('<Double-Button-1>',Remplir)

supplier.resizable(False, False)
supplier.mainloop()
