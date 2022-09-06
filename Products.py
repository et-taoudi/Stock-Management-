from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from subprocess import call
import pandas as pd

#Fonction pour afficher les données de produits la base de données dans un tableau
def showTableP() :
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.réf_prod AS 'Num',P.libellé_prod AS 'Libellé',P.qteEnStock_prod AS 'Quantité en Stock',P.etat_prod AS 'Etat',P.description_prod AS 'Description',C.num_cat AS 'Num Catégorie', C.nom_cat AS 'Catégorie' FROM produit AS P JOIN catégorie AS C ON P.num_cat=C.num_cat")
    records = cursor.fetchall()
    print(records)

    for i,(ID,Libellé,QuantitéEnStock,Etat,Description,NumCatégorie,Catégorie) in enumerate(records,start=1) :
        listBox.insert("","end",values=(ID,Libellé,QuantitéEnStock,Etat,Description,NumCatégorie,Catégorie))
        conn.close()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

product = Tk()

#Connexion with DATABASE*******************************
def connection():
    conn=mysql.connector.connect(
        host='localhost',port='3307', user='root', password='', database='estellantis'
    )
    return conn
#******************************************************************************


#Fonction pour afficher les données de catégorie de la base de données dans un tableau
def showTableC() :
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT C.num_cat AS 'Numéro',C.nom_cat AS 'Catégorie',SUM(P.qteEnStock_prod) AS 'Total Number' FROM catégorie AS C LEFT JOIN produit AS P ON P.num_cat=C.num_cat GROUP BY C.num_cat ORDER BY C.num_cat ASC")
    records1 = cursor.fetchall()
    print(records1)

    for i,(Num,Catégorie,Total) in enumerate(records1,start=1) :
        listBox1.insert("","end",values=(Num,Catégorie,Total))
        conn.close()
#------------------------------------------------------------------------------

#Fonction pour ajouter un nouveau produit-------------------------------
def AddP():
    numéro=num.get()
    produit=prod.get()
    quantité=qte.get()
    statut=etat.get()
    description=desc.get()
    idcategorie=id.get()
    catégorie=cat.get()

    if numéro=="":
        messagebox.showinfo("Information", "Please insert a Product Reference to add a new product !!")
    if idcategorie=="":
        messagebox.showinfo("Information", "Please select the category of the product to add !!")
    if ((produit == "") or (quantité == "")):
        messagebox.showinfo("Information", "Please fill all the textbox !!!")
    else :

        try:

            conn = connection()
            cursor = conn.cursor()

            sql1 = "SELECT count(*) FROM produit WHERE réf_prod=%s"
            val1 = (numéro,)
            cursor.execute(sql1, val1)
            result = cursor.fetchone()
            found = result[0]

            try:
                if found == 0:
                    sql="INSERT INTO produit (réf_prod,libellé_prod,qteEnStock_prod,etat_prod,description_prod,num_cat) VALUES (%s,%s,%s,%s,%s,%s)"
                    val=(numéro,produit,quantité,statut,description,idcategorie)
                    cursor.execute(sql,val)

                    conn.commit()
                    lastid=cursor.lastrowid
                    messagebox.showinfo("Information","Product inserted successfully...!!")
                    Refresh()

                    numéro.delete(0,END)
                    produit.delete(0, END)
                    quantité.delete(0,END)
                    statut.delete(0,END)
                    description.delete(0,END)
                    idcategorie.delete(0, END)
                    catégorie.delete(0, END)

                    num.focus_set()
                else :
                    messagebox.showinfo("Information", "Product reference already exist. Try with another!!")
            except Exception as e:
                print(e)
                conn.rollback()
                conn.close()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
#----------------------------------------------------------------------------

#Fonction pour ajouter une nouvelle catégorie-------------------------------
def AddC():
    catégorie = cat.get()

    if id.get() != "":
        messagebox.showinfo("Information", "Category ID is auto increment!! Please just insert the name of new category.")
    elif catégorie=="":
        messagebox.showinfo("Information","Please insert the name of new category.")
    else :
        conn = connection()
        cursor = conn.cursor()

        try:
            sql="INSERT INTO catégorie (nom_cat) VALUES (%s)"
            val=(catégorie,)
            cursor.execute(sql,val)

            conn.commit()
            lastid=cursor.lastrowid
            messagebox.showinfo("Information","Category inserted successfully...!!")
            Refresh()

            catégorie.delete(0, END)

            id.focus_set()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
#----------------------------------------------------------------------------

#Fonction update------------------------------------------------------------
def Update():
    numéro = num.get()
    produit = prod.get()
    quantité = qte.get()
    statut = etat.get()
    description = desc.get()
    idcategorie = id.get()
    catégorie = cat.get()

    if ((numéro == "") or  (produit=="") or (quantité=="") or (statut=="") or (description=="") or (idcategorie=="")):
        messagebox.showinfo("Information", "Please fill all the textbox !!!")
    else :
        conn = connection()
        cursor = conn.cursor()

        try :
            sql="UPDATE produit SET libellé_prod=%s, qteEnStock_prod = %s, etat_prod=%s, description_prod=%s, num_cat=%s WHERE réf_prod=%s"
            val=(produit,quantité,statut,description,idcategorie,numéro)
            cursor.execute(sql, val)

            conn.commit()
            lastid = cursor.lastrowid
            messagebox.showinfo("Information", "Product updated successfully...!!")
            Refresh()

            numéro.delete(0, END)
            produit.delete(0, END)
            quantité.delete(0, END)
            statut.delete(0, END)
            description.delete(0, END)
            idcategorie.delete(0, END)
            catégorie.delete(0, END)

            num.focus_set()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
#*******************************************************************************

#Fonction Delete Category***********************************************
def DeleteC():
    catégorieId=id.get()
    catégorie=cat.get()

    if catégorieId == "":
        messagebox.showinfo("Information", "Please fill in the Category ID field to delete a category or select a category from the table!!")
    else :
        conn = connection()
        cursor = conn.cursor()
        if messagebox.askyesno("Confirm Please", "Are you sure you want to delete this category ? As a remind, all products belonging to this category will be deleted automatically !!"):
            try:

                sql = "DELETE FROM produit WHERE num_cat=%s"
                val = (catégorieId,)
                cursor.execute(sql, val)

                sql1 = "DELETE FROM catégorie WHERE num_cat=%s"
                val1 = (catégorieId,)
                cursor.execute(sql1, val1)


                conn.commit()
                lastid = cursor.lastrowid
                messagebox.showinfo("Information", "Category deleted successfully...!!")
                Refresh()

                catégorieId.delete(0, END)
                catégorie.delete(0, END)

                id.focus_set()

            except Exception as e:
                print(e)
                conn.rollback()
                conn.close()
        else :
            return True
#****************************************************************************************

#Fonction Delete Product*****************************************************************
def DeleteP():
    numéroP=num.get()

    if numéroP == "":
        messagebox.showinfo("Information", "Please fill in the Product ID field to delete a product or select a product from the table!!")
    else :
        conn = connection()
        cursor = conn.cursor()
        if messagebox.askyesno("Confirm Please", "Are you sure you want to delete this product ? As a remind, all dotations belonging to this product will be deleted automatically "):
            try:
                msg='Indisponible'

                sql = "UPDATE produit SET etat_prod=%s,qteEnStock_prod=0 WHERE réf_prod=%s".format(numéroP)
                val = (msg, numéroP)
                cursor.execute(sql, val)


                conn.commit()
                lastid = cursor.lastrowid
                messagebox.showinfo("Information", "Product deleted successfully...!!")
                Refresh()

                numéroP.delete(0, END)

                num.focus_set()

            except Exception as e:
                print(e)
                conn.rollback()
                conn.close()
        else :
            return True
#*****************************************************************************************

#Fonction pour remplir les champs avec les données de la ligne séléctionnée depuis le tableau
def RemplirP(event):
    num.delete(0,END)
    prod.delete(0, END)
    qte.delete(0,END)
    etat.delete(0,END)
    desc.delete(0,END)
    id.delete(0, END)
    cat.delete(0, END)

    row_id=listBox.selection()[0]
    select=listBox.set(row_id)

    num.insert(0,select['ID'])
    prod.insert(0, select['Libellé'])
    qte.insert(0,select['QuantitéEnStock'])
    etat.insert(0,select['Etat'])
    desc.insert(0,select['Description'])
    id.insert(0,select['NumCatégorie'])
    cat.insert(0, select['Catégorie'])
#***********************************************************************************************

#Fonction pour remplir les champs de catégorie from table
def RemplirC(event):
    id.delete(0, END)
    cat.delete(0, END)

    row_id = listBox1.selection()[0]
    select = listBox1.set(row_id)

    id.insert(0, select['Num'])
    cat.insert(0, select['Catégorie'])
#********************************************************************

#Fonction pour rafraichir les données des tableaux************************************
def Refresh():
    for records in listBox.get_children():
        listBox.delete(records)
    for records1 in listBox1.get_children():
        listBox1.delete(records1)
    showTableC()
    showTableP()
#********************************************************************

#Fonction pour cleaner les textbox************************************
def Clean():
    num.delete(0, END)
    prod.delete(0, END)
    qte.delete(0, END)
    etat.delete(0, END)
    desc.delete(0, END)
    id.delete(0, END)
    cat.delete(0, END)
#********************************************************************

#Fonction pour rechercher un produit selon les données dans la barre de recherche************************************
def Research():
    rechercher = str(rech.get())

    conn = connection()
    cursor = conn.cursor()

    if rechercher == "":
        messagebox.showinfo("Information", "Please fill in the search field to find a dotation!!")
        showTableP()
    else :
        try:

            sql = "SELECT P.réf_prod AS 'Num',P.libellé_prod AS 'Libellé',P.qteEnStock_prod AS 'QuantitéEnStock',P.etat_prod AS 'Etat',P.description_prod AS 'Description',C.num_cat AS 'Num Catégorie', C.nom_cat AS 'Catégorie' FROM produit AS P JOIN catégorie AS C ON P.num_cat=C.num_cat WHERE P.réf_prod LIKE '%"+rechercher+"%' OR P.libellé_prod LIKE '%"+rechercher+"%' OR P.qteEnStock_prod LIKE '%"+rechercher+"%' OR P.etat_prod LIKE '%"+rechercher+"%' OR P.description_prod LIKE '%"+rechercher+"%' OR C.num_cat LIKE '%"+rechercher+"%' OR C.nom_cat LIKE '%"+rechercher+"%' "
            val = ()
            cursor.execute(sql, val)

            for records in listBox.get_children():
                listBox.delete(records)

            records = cursor.fetchall()
            print(records)

            for i, (ID, Libellé, QuantitéEnStock, Etat, Description, NumCatégorie, Catégorie) in enumerate(records,start=1):
                listBox.insert("", "end", values=(ID, Libellé, QuantitéEnStock, Etat, Description, NumCatégorie, Catégorie))
                conn.close()

        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
#********************************************************************

#Fonction pour accéder à la page Dotations****************************
def toDotations():
    product.destroy()
    call(["python", "Dotations.py"])
#*********************************************************************

#Fonction pour accéder à la page Profile****************************
def toProfile():
    product.destroy()
    call(["python", "Profile.py"])
#*********************************************************************

#Fonction pour accéder à la page Dashboard****************************
def toHome():
    product.destroy()
    call(["python", "Home.py"])
#*********************************************************************

#Fonction pour accéder à la page Admins****************************
def toAdmins():
    product.destroy()
    call(["python", "Admins.py"])
#*********************************************************************

#Fonction pour accéder à la page Suppliers****************************
def toSuppliers():
    product.destroy()
    call(["python", "Suppliers.py"])
#*********************************************************************
#Fonction pour exiter****************************
def LogOut():
    if messagebox.askyesno("Confirm Please", "Are you sure you want to exit the application ?"):
        product.destroy()
    else :
        return True
#*********************************************************************

#Export data to Excel File**************************************************
def ExportExcel():

    conn = connection()
    cursor = conn.cursor()

    sql="SELECT P.réf_prod ,P.libellé_prod ,P.qteEnStock_prod ,P.etat_prod ,P.description_prod ,C.num_cat , C.nom_cat FROM produit AS P JOIN catégorie AS C ON P.num_cat=C.num_cat "
    df = pd.read_sql(sql,conn )

    df.to_excel('C:\ExportExcel.xlsx',index=False,header=['Référence', 'Libellé', 'Quantité en stock', 'Etat','Description','Num Catégorie','Catégorie'])
    messagebox.showinfo("Information", "An Excel File was genrated successfully in C:\ExportExcel.xlsx !!!")
    df = pd.read_excel('C:\ExportExcel.xlsx')

#*****************************************************************************


def btn_clicked():
    print("Button Clicked")



product.geometry("1200x750")
product.configure(bg = "#e1f7fe")
product.title("G-Stock Stellantis PSA Group")
product.iconbitmap(r'img/Logo.ico')

#Place the LoginPage in the center of the screen
x = product.winfo_screenwidth()//10
y = int(product.winfo_screenheight() * 0.030)
product.geometry("1200x750+"+str(x)+'+'+str(y))
#************************************************

#+++++++++++++++++++++++++++++++++++++++++++++++++
#Window Canvas***********************************
canvas = Canvas(
    product,
    bg = "#e1f7fe",
    height = 750,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)
#********************************************************

#BackGround **************************************************
background_img = PhotoImage(file = f"img/ProductsBG.png")
background = canvas.create_image(
    600, 370,
    image=background_img)
#**************************************************************

#Profile Image *******************************************

img0 = PhotoImage(file=f"img/profile.png")
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=toProfile,
    relief="flat")

b0.place(
    x=1070, y=85,
    width=34,
    height=34)

canvas.create_text(
    1000, 105,
    text = "Farhate Elatoui",
    fill = "#0500ff",
    font = ("None", int(11)))
#**********************************************************

#Name Session Admin************************************
canvas.create_text(
    307.0, -264.5,
    text = "Farhate Elatoui",
    fill = "#0500ff",
    font = ("None", int(14.0)))
#********************************************************

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
    x = 615, y = 168,
    width = 127,
    height = 35)
#*********************************************************

#Refresh Table Button**********************************
img2 = PhotoImage(file = f"img/refreshTable.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command = Refresh,
    relief = "flat")

b2.place(
    x = 755, y = 167,
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
    x = 75, y = 190,
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
    x = 74, y = 238,
    width = 23,
    height = 23)
#**********************************************************


#Products Button Menu**************************************
img5 = PhotoImage(file = f"img/Products_Menu_ON.png")
b5 = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b5.place(
    x = 68, y = 285,
    width = 38,
    height = 38)
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
    x = 75, y = 340,
    width = 24,
    height = 24)
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
    x = 74, y = 385,
    width = 24,
    height = 24)
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
    x = 1080, y = 650,
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
    command = btn_clicked,
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


#Add Product Button****************************************************
img12 = PhotoImage(file = f"img/Add.png")
b12 = Button(
    image = img12,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command = AddP,
    relief = "flat")

b12.place(
    x = 400, y = 504,
    width = 131,
    height = 44)
#************************************************************

#Update Product Button***********************************************
img13 = PhotoImage(file = f"img/Update.png")
b13 = Button(
    image = img13,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command = Update,
    relief = "flat")

b13.place(
    x = 650, y = 504,
    width = 128,
    height = 44)
#*************************************************************

#Delete product Button**************************************************
img14 = PhotoImage(file = f"img/Delete.png")
b14 = Button(
    image = img14,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command = DeleteP,
    relief = "flat")

b14.place(
    x = 525, y = 504,
    width = 131,
    height = 44)
#*************************************************************

#Champs Pour Ajouter une nouvelle dotation
global num,prod,qte,etat,desc,id,cat

num = Entry(product)
num.place(x=150,y=590)

prod = Entry(product)
prod.place(x=298,y=590)

qte = Entry(product)
qte.place(x=448,y=590)

etat = Entry(product)
etat.place(x=600,y=590)

desc = Entry(product)
desc.place(x=752,y=590)

id = Entry(product)
id.place(x=925,y=516)

cat = Entry(product)
cat.place(x=925,y=578,width=150)
#*********************************************************************



#Tableau Product******************************************************
cols=("ID","Libellé","QuantitéEnStock","Etat","Description","NumCatégorie","Catégorie")
listBox=ttk.Treeview(product, columns=cols, show='headings')

for col in cols :
    listBox.heading(col,text=col)
    listBox.grid(row=1,column=0,columnspan=2)
    listBox.place(x=150,y=270,width=730)

    listBox.column(0,width=12)
    listBox.column(1, width=70)
    listBox.column(2, width=70)
    listBox.column(3, width=20)
    listBox.column(4, width=150)
    listBox.column(5, width=50)
    listBox.column(6, width=30)

#**********************************************************************

#Tableau Catégorie******************************************************
cols1=("Num","Catégorie","Total")
listBox1=ttk.Treeview(product, columns=cols1, show='headings')

for col in cols1 :
    listBox1.heading(col,text=col)
    listBox1.grid(row=1,column=0,columnspan=2)
    listBox1.place(x=925,y=220,width=172,height=250)

    listBox1.column(0,width=30)
    listBox1.column(1, width=80)
    listBox1.column(2, width=40)

#**********************************************************************


#Add New Category Button*****************************
img15 = PhotoImage(file = f"img/AddCat.png")
b15 = Button(
    image = img15,
    borderwidth = 0,
    highlightthickness = 0,
    command = AddC,
    relief = "flat")

b15.place(
    x = 1090, y = 475,
    width = 30,
    height = 32)
#*****************************************************

#Products Menu ON***************************************
img16 = PhotoImage(file = f"img/Products_Menu_ON.png")
b16 = Button(
    image = img16,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b16.place(
    x = -448, y = -100,
    width = 54,
    height = 66)
#******************************************************

#Delete Category Button**********************************
img17 = PhotoImage(file = f"img/DeleteCat.png")
b17 = Button(
    image = img17,
    borderwidth = 0,
    highlightthickness = 0,
    command = DeleteC,
    relief = "flat")

b17.place(
    x = 1090, y = 540,
    width = 31,
    height = 32)
#************************************************


#Clean Butoon***************************************
img18 = PhotoImage(file = f"img/Clean.png")
b18 = Button(
    image = img18,
    borderwidth = 0,
    highlightthickness = 0,
    command = Clean,
    relief = "flat")

b18.place(
    x = 785, y = 510,
    width = 90,
    height = 35)
#***************************************************

#Search label****************************
rech=Entry(product,width=28,fg='#0500ff',bg='#EEEEFF',border=0)
rech.place(x=185,y=228)
#*****************************************************************


#Search Button***************************************
img19 = PhotoImage(file = f"img/Search.png")
b19 = Button(
    image = img19,
    borderwidth = 0,
    highlightthickness = 0,
    command = Research,
    relief = "flat")

b19.place(
    x = 362, y = 229,
    width = 44,
    height = 16)
#****************************************************


showTableP()
showTableC()

listBox.bind('<Double-Button-1>',RemplirP)
listBox1.bind('<Double-Button-1>',RemplirC)

product.resizable(False, False)
product.mainloop()
