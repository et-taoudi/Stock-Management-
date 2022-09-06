from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from subprocess import call
from datetime import date
import pandas as pd
dotation = Tk()

#Connexion with DATABASE*******************************
def connection():
    conn=mysql.connector.connect(
        host='localhost',port='3307', user='root', password='', database='estellantis'
    )
    return conn
#******************************************************************************

#Functions**********************************************************************

#Fonction pour avoir le nombre dotation effectuée aujourd'hui
def NDotation():
    lbl1.delete(0, END)
    now = date.today()
    dt_string = now.strftime("%Y-%m-%d")

    conn = connection()
    cursor = conn.cursor()

    sql=("SELECT count(*) FROM dotation WHERE date_dot LIKE '%"+dt_string+"%'")
    val = ()
    cursor.execute(sql, val)

    result = cursor.fetchone()
    found = result[0]

    lbl1.insert(0, found)
#**********************************************************************

#Fonction pour avoir le produit le plus doté**********************************
def BestP():
    lbl2.delete(0,END)
    conn = connection()
    cursor = conn.cursor()
    sql = ("SELECT P.réf_prod FROM dotation AS D INNER JOIN correspondre AS C ON C.num_dot=D.num_dot INNER JOIN produit AS P ON P.réf_prod=C.réf_prod GROUP BY P.réf_prod ORDER BY count(*) DESC LIMIT 1")
    val = ()
    cursor.execute(sql, val)
    result = cursor.fetchone()
    found = result[0]
    lbl2.insert(0,found)


    lbl3.delete(0, END)
    conn1 = connection()
    cursor1 = conn1.cursor()
    sql1 = ("SELECT P.libellé_prod FROM dotation AS D INNER JOIN correspondre AS C ON C.num_dot=D.num_dot INNER JOIN produit AS P ON P.réf_prod=C.réf_prod GROUP BY P.libellé_prod ORDER BY count(*) DESC LIMIT 1")
    val1 = ()
    cursor1.execute(sql1, val1)
    result1 = cursor1.fetchone()
    found1 = result1[0]
    lbl3.insert(0, str(found1))

    lbl4.delete(0, END)
    conn2 = connection()
    cursor2 = conn2.cursor()
    sql2 = ("SELECT P.qteEnStock_prod FROM dotation AS D INNER JOIN correspondre AS C ON C.num_dot=D.num_dot INNER JOIN produit AS P ON P.réf_prod=C.réf_prod GROUP BY P.libellé_prod ORDER BY count(*) DESC LIMIT 1")
    val2 = ()
    cursor2.execute(sql2, val2)
    result2 = cursor2.fetchone()
    found2 = result2[0]
    lbl4.insert(0, str(found2))

#*******************************************************************

#Fonction pour avoir le produit le moins doté**********************************
def LessP():
    lbl5.delete(0,END)
    conn = connection()
    cursor = conn.cursor()
    sql = ("SELECT P.réf_prod FROM dotation AS D INNER JOIN correspondre AS C ON C.num_dot=D.num_dot INNER JOIN produit AS P ON P.réf_prod=C.réf_prod GROUP BY P.réf_prod ORDER BY count(*) ASC LIMIT 1")
    val = ()
    cursor.execute(sql, val)
    result = cursor.fetchone()
    found = result[0]
    lbl5.insert(0,found)


    lbl6.delete(0, END)
    conn1 = connection()
    cursor1 = conn1.cursor()
    sql1 = ("SELECT P.libellé_prod FROM dotation AS D INNER JOIN correspondre AS C ON C.num_dot=D.num_dot INNER JOIN produit AS P ON P.réf_prod=C.réf_prod GROUP BY P.libellé_prod ORDER BY count(*) ASC LIMIT 1")
    val1 = ()
    cursor1.execute(sql1, val1)
    result1 = cursor1.fetchone()
    found1 = result1[0]
    lbl6.insert(0, str(found1))

    lbl7.delete(0, END)
    conn2 = connection()
    cursor2 = conn2.cursor()
    sql2 = ("SELECT P.qteEnStock_prod FROM dotation AS D INNER JOIN correspondre AS C ON C.num_dot=D.num_dot INNER JOIN produit AS P ON P.réf_prod=C.réf_prod GROUP BY P.libellé_prod ORDER BY count(*) ASC LIMIT 1")
    val2 = ()
    cursor2.execute(sql2, val2)
    result2 = cursor2.fetchone()
    found2 = result2[0]
    lbl7.insert(0, str(found2))

#*******************************************************************

#Fonction pour afficher les données de la base de données dans un tableau
def showTable() :
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT D.num_dot AS 'Num',P.réf_prod AS 'Référence',P.libellé_prod AS 'Produit',P.etat_prod AS 'Etat',D.qte_dot AS 'Quantité',D.date_dot AS 'Date',A.id_admin AS 'Id_Admin',S.id_sal AS 'Id Salarié',S.nom_sal AS 'Salarié' FROM dotation AS D JOIN admin AS A ON D.id_admin=A.id_admin JOIN salarié AS S ON S.id_sal=D.id_sal JOIN correspondre AS C ON C.num_dot=D.num_dot JOIN produit AS P ON P.réf_prod=C.réf_prod ORDER BY D.num_dot Asc")
    records = cursor.fetchall()
    print(records)

    for i,(Num,Référence,Produit,Etat,Quantité,Date,Admin,Id_Salarié, Salarié) in enumerate(records,start=1) :
        listBox.insert("","end",values=(Num,Référence,Produit,Etat,Quantité,Date,Admin,Id_Salarié, Salarié))
        conn.close()
#------------------------------------------------------------------------------

#Fonction pour ajouter une nouvelle dotation-------------------------------
def Add():
    dotation=num.get()
    quantité=qte.get()
    administrator=admin.get()
    salaried=sal.get()
    product=prod.get()

    if ((quantité == "") or (administrator== "") or (salaried== "") or (product== "")):
        messagebox.showinfo("Information", "Please fill all the textbox !!!")
    if dotation=="":
        messagebox.showinfo("Information", "Please insert a Dotation ID to add a new dotation !!")
    else :

        try:
            conn = connection()
            cursor = conn.cursor()

            sql1 = "SELECT count(*) FROM dotation WHERE num_dot=%s"
            val1 = (dotation,)
            cursor.execute(sql1, val1)
            result = cursor.fetchone()
            found = result[0]
            try:
                if found == 0:

                    sql1 = "UPDATE produit SET qteEnStock_prod=qteEnStock_prod-%s WHERE réf_prod=%s"
                    val1 = (quantité, product)
                    cursor.execute(sql1, val1)

                    sql="INSERT INTO dotation (num_dot,qte_dot,id_admin,id_sal) VALUES (%s,%s,%s,%s)"
                    val=(dotation,quantité,administrator,salaried)
                    cursor.execute(sql,val)

                    lastid = cursor.lastrowid

                    sql2 = "INSERT INTO correspondre VALUES (%s,%s)"
                    val2 = (product,dotation)
                    cursor.execute(sql2,val2)

                    conn.commit()

                    messagebox.showinfo("Information","Dotation inserted successfully...!!")
                    Refresh()
                    NDotation()
                    BestP()
                    LessP()

                    product.delete(0,END)
                    quantité.delete(0,END)
                    administrator.delete(0,END)
                    salaried.delete(0,END)

                    num.focus_set()
                else:
                    messagebox.showinfo("Information", "Dotation ID already exist. Try with another!!")
            except Exception as e:
                print(e)
                conn.rollback()
                conn.close()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
#----------------------------------------------------------------------------

#Fonction update------------------------------------------------------------
def Update():
    dotationId=num.get()
    quantité = qte.get()
    administrator = admin.get()
    salaried = sal.get()
    conn = connection()
    cursor = conn.cursor()

    sql1 = "SELECT count(*) FROM salarié WHERE id_sal=%s"
    val1 = (salaried,)
    cursor.execute(sql1, val1)
    result1 = cursor.fetchone()
    found1 = result1[0]

    try :
        if found1 != 0:

            sql2 = "SELECT count(*) FROM admin WHERE id_admin=%s"
            val2 = (administrator,)
            cursor.execute(sql2, val2)
            result2 = cursor.fetchone()
            found2 = result2[0]

            if found2 != 0 :
                sql3 = "SELECT qte_dot FROM dotation WHERE num_dot=%s"
                val3 = (dotationId,)
                cursor.execute(sql3, val3)
                result3 = cursor.fetchone()
                found3 = result3[0]

                diff = -found3 + int(quantité)
                print(diff)

                sql = "UPDATE dotation SET qte_dot = %s, id_admin=%s, id_sal=%s WHERE num_dot=%s"
                val = (quantité, administrator, salaried, dotationId)
                cursor.execute(sql, val)


                sql1 = "SELECT réf_prod FROM correspondre WHERE num_dot=%s"
                val1 = (dotationId,)
                cursor.execute(sql1, val1)
                result4 = cursor.fetchone()
                found4 = result4[0]

                if diff<0 :
                    sql1 = "UPDATE produit SET qteEnStock_prod=qteEnStock_prod-%s WHERE réf_prod=%s"
                    val1 = (diff, found4)
                    cursor.execute(sql1, val1)
                else :
                    sql5 = "UPDATE produit SET qteEnStock_prod=qteEnStock_prod-%s WHERE réf_prod=%s"
                    val5 = (diff, found4)
                    cursor.execute(sql5, val5)
                conn.commit()
                lastid = cursor.lastrowid
                messagebox.showinfo("Information", "Dotation updated successfully...!!")
                Refresh()

                dotationId.delete(0, END)
                quantité.delete(0, END)
                administrator.delete(0, END)
                salaried.delete(0, END)

                num.focus_set()

            else:
                messagebox.showinfo("Information", "This Admin doesn't exist. Try with a valid Admin ID!!")
        else:
            messagebox.showinfo("Information", "This Employee doesn't exist. Try with a valid Employee ID!!")
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
#*************************************************************************************************

#Fonction Delete***********************************************************************************
def delete():
    dotationId=num.get()
    product=prod.get()
    quantitédot=qte.get()

    conn = connection()
    cursor = conn.cursor()

    if messagebox.askyesno("Confirm Please", "Are you sure you want to delete this dotation ?"):
        try:
            sql = "DELETE FROM correspondre WHERE num_dot=%s AND réf_prod=%s"
            val = (dotationId,product)
            cursor.execute(sql, val)

            sql2 = "UPDATE produit SET qteEnStock_prod=qteEnStock_prod+%s WHERE réf_prod=%s"
            val2 = (quantitédot, product)
            cursor.execute(sql2, val2)

            sql1 = "DELETE FROM dotation WHERE num_dot=%s"
            val1 = (dotationId,)
            cursor.execute(sql1, val1)

            conn.commit()
            lastid = cursor.lastrowid
            messagebox.showinfo("Information", "Dotation deleted successfully...!!")
            Refresh()
            NDotation()
            BestP()
            LessP()

            dotationId.delete(0, END)
            product.delete(0, END)

            num.focus_set()

        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()

    else :
        return True

#*************************************************************************************************

#Fonction pour remplir les champs avec les données de la ligne séléctionnée depuis le tableau
def Remplir(event):
    num.delete(0,END)
    prod.delete(0, END)
    qte.delete(0,END)
    admin.delete(0,END)
    sal.delete(0,END)

    row_id=listBox.selection()[0]
    select=listBox.set(row_id)

    num.insert(0,select['Num'])
    prod.insert(0, select['Référence'])
    qte.insert(0,select['Quantité'])
    admin.insert(0,select['Admin'])
    sal.insert(0,select['Id_Salarié'])
#***********************************************************************************************

#Fonction pour rafraichir les données des tableaux************************************
def Refresh():
    for records in listBox.get_children():
        listBox.delete(records)
    showTable()
#********************************************************************

#Export data to Excel File**************************************************
def ExportExcel():

    conn = connection()
    cursor = conn.cursor()

    sql="SELECT D.num_dot ,P.réf_prod ,P.libellé_prod ,D.qte_dot ,D.date_dot ,A.id_admin ,S.id_sal ,S.nom_sal  FROM dotation AS D JOIN admin AS A ON D.id_admin=A.id_admin JOIN salarié AS S ON S.id_sal=D.id_sal JOIN correspondre AS C ON C.num_dot=D.num_dot JOIN produit AS P ON P.réf_prod=C.réf_prod ORDER BY D.num_dot Asc "
    df = pd.read_sql(sql,conn )

    df.to_excel('C:\ExportExcel.xlsx',index=False,header=["Num","Référence","Produit","Quantité","Date","Admin","Id_Salarié","Salarié"])
    messagebox.showinfo("Information", "An Excel File was genrated successfully in C:\ExportExcel.xlsx !!!")
    df = pd.read_excel('C:\ExportExcel.xlsx')

#*****************************************************************************

#Fonction pour cleaner les textbox************************************
def Clean():
    num.delete(0, END)
    prod.delete(0, END)
    qte.delete(0, END)
    admin.delete(0, END)
    sal.delete(0, END)
#********************************************************************

#Fonction pour accéder à la page Profile****************************
def toProfile():
    dotation.destroy()
    call(["python", "Profile.py"])
#*********************************************************************

#Fonction pour accéder à la page Dashboard****************************
def toHome():
    dotation.destroy()
    call(["python", "Home.py"])
#*********************************************************************

#Fonction pour accéder à la page Suppliers****************************
def toSuppliers():
    dotation.destroy()
    call(["python", "Suppliers.py"])
#*********************************************************************

#Fonction pour accéder à la page Produits****************************
def toProducts():
    dotation.destroy()
    call(["python", "Products.py"])
#*********************************************************************

#Fonction pour accéder à la page Admins****************************
def toAdmins():
    dotation.destroy()
    call(["python", "Admins.py"])
#*********************************************************************

#Fonction pour exiter****************************
def LogOut():
    if messagebox.askyesno("Confirm Please", "Are you sure you want to exit the application ?"):
        dotation.destroy()
    else :
        return True
#*********************************************************************

#Fonction pour rechercher un produit selon les données dans la barre de recherche************************************
def Research():
    rechercher = str(rech.get())

    conn = connection()
    cursor = conn.cursor()

    if rechercher == "":
        messagebox.showinfo("Information", "Please fill in the search field to find a dotation!!")
        showTable()
    else:
        try:

            sql = "SELECT D.num_dot AS 'Num',P.réf_prod AS 'Référence',P.libellé_prod AS 'Produit',P.etat_prod AS 'Etat',D.qte_dot AS 'Quantité',D.date_dot AS 'Date',A.id_admin AS 'Id_Admin',S.id_sal AS 'Id Salarié',S.nom_sal AS 'Salarié' FROM dotation AS D JOIN admin AS A ON D.id_admin=A.id_admin JOIN salarié AS S ON S.id_sal=D.id_sal JOIN correspondre AS C ON C.num_dot=D.num_dot JOIN produit AS P ON P.réf_prod=C.réf_prod WHERE D.num_dot LIKE '%"+rechercher+"%' OR P.réf_prod LIKE '%"+rechercher+"%' OR P.libellé_prod LIKE '%"+rechercher+"%' OR D.qte_dot LIKE '%"+rechercher+"%' OR D.date_dot LIKE '%"+rechercher+"%' OR A.id_admin LIKE '%"+rechercher+"%' OR S.id_sal LIKE '%"+rechercher+"%' OR S.nom_sal LIKE '%"+rechercher+"%' ORDER BY D.num_dot Asc"
            val = ()
            cursor.execute(sql, val)

            for records in listBox.get_children():
                listBox.delete(records)

            records = cursor.fetchall()
            print(records)

            for i, (Num,Référence,Produit,Etat,Quantité,Date,Admin,Id_Salarié, Salarié) in enumerate(records,start=1):
                listBox.insert("", "end", values=(Num,Référence,Produit,Etat,Quantité,Date,Admin,Id_Salarié, Salarié))
                conn.close()

        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
#********************************************************************
#Fonction pour exiter****************************
def LogOut():
    if messagebox.askyesno("Confirm Please", "Are you sure you want to exit the application ?"):
        dotation.destroy()
    else :
        return True
#*********************************************************************
def btn_clicked():
    print("Button Clicked")



dotation.geometry("1200x750")
dotation.configure(bg = "#e1f7fe")
dotation.title("G-Stock Stellantis PSA Group - Dotations -")
dotation.iconbitmap(r'img/Logo.ico')

#Place the LoginPage in the center of the screen
x = dotation.winfo_screenwidth()//10
y = int(dotation.winfo_screenheight() * 0.030)
dotation.geometry("1200x750+"+str(x)+'+'+str(y))
#************************************************

canvas = Canvas(
    dotation,
    bg = "#e1f7fe",
    height = 750,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)


#Background Image Dotations Page
background_img = PhotoImage(file = f"img/DotationsBG.png")
background = canvas.create_image(
    605, 370,
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
    x = 1080, y = 85,
    width = 34,
    height = 34)
#**********************************************************


canvas.create_text(
    1000, 105,
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
    x = 625, y = 169,
    width = 127,
    height = 36)
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
    x = 770, y = 169,
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
img4 = PhotoImage(file = f"img/Dotations_Menu.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b4.place(
    x = 83, y = 234,
    width = 36,
    height = 36)
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
img6 = PhotoImage(file = f"img/Fournisseurs_Menu_Off.png")
b6 = Button(
    image = img6,
    borderwidth = 0,
    highlightthickness = 0,
    command = toSuppliers,
    relief = "flat")

b6.place(
    x = 89, y = 340,
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
    x = 88, y = 385,
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
    x = 1085, y = 650,
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
    x = 460, y = 504,
    width = 128,
    height = 44)
#************************************************************

#Update Button***********************************************
img13 = PhotoImage(file = f"img/Update.png")
b13 = Button(
    image = img13,
    borderwidth = 0,
    background='white',
    highlightthickness = 0,
    command = Update,
    relief = "flat")

b13.place(
    x = 680, y = 504,
    width = 128,
    height = 44)
#*************************************************************

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
    x = 571, y = 504,
    width = 120,
    height = 44)
#*************************************************************

#Champs Pour Ajouter une nouvelle dotation
num = Entry(dotation)
num.place(x=160,y=590)

prod = Entry(dotation)
prod.place(x=310,y=590)

qte = Entry(dotation)
qte.place(x=460,y=590)

admin = Entry(dotation)
admin.place(x=610,y=590)

sal = Entry(dotation)
sal.place(x=760,y=590)




#*********************************************************************



#Tableau Dotation******************************************************
cols=("Num","Référence","Produit","Etat","Quantité","Date","Admin","Id_Salarié","Salarié")
listBox=ttk.Treeview(dotation, columns=cols, show='headings')

for col in cols :
    listBox.heading(col,text=col)
    listBox.grid(row=1,column=0,columnspan=2)
    listBox.place(x=150,y=270,width=750)

    listBox.column(0,width=35)
    listBox.column(1, width=70)
    listBox.column(2, width=130)
    listBox.column(3, width=70)
    listBox.column(4, width=60)
    listBox.column(5, width=100)
    listBox.column(6, width=100)
    listBox.column(7, width=100)
    listBox.column(8, width=90)

#**********************************************************************

#Search label****************************
rech=Entry(dotation,width=28,fg='#0500ff',bg='#EEEEFF',border=0)
rech.place(x=200,y=228)
#*****************************************************************


#Total number dotation in day report
lbl1=Entry(dotation,bg='#CFCDFB',border=0,font=("Inter-Bold", int(17)),width=8)
lbl1.place(x=945,y=260)

canvas.create_text(
    1016, 325,
    text = "Total number made today",
    fill = "#050505",
    font = ("Inter-Bold", int(9.0)))

canvas.create_text(
    995, 300,
    text = "Dotation this day",
    fill = "#050505",
    font = ("Inter-Light", int(10.0)))
#***********************************************************************

#Best requested Product report********************************************
lbl2=Entry(dotation,bg='#CFCDFB',border=0,font=("Inter-Bold", int(17)),width=8)
lbl2.place(x=945,y=395)

lbl3=Entry(dotation,bg='#CFCDFB',border=0,font=("Inter-Bold", int(10)),width=23)
lbl3.place(x=945,y=430)

lbl4=Entry(dotation,bg='#CFCDFB',border=0,font=("Inter-Bold", int(9)),width=23)
lbl4.place(x=945,y=455)

#******************************************************************************

#Less requested product report///////////////////////////////////////////////////
lbl5=Entry(dotation,bg='#CFCDFB',border=0,font=("Inter-Bold", int(17)),width=8)
lbl5.place(x=945,y=532)

lbl6=Entry(dotation,bg='#CFCDFB',border=0,font=("Inter-Bold", int(10)),width=23)
lbl6.place(x=945,y=567)

lbl7=Entry(dotation,bg='#CFCDFB',border=0,font=("Inter-Bold", int(9)),width=23)
lbl7.place(x=945,y=590)
#***************************************************


#Clean Butoon***************************************
img18 = PhotoImage(file = f"img/Clean.png")
b18 = Button(
    image = img18,
    borderwidth = 0,
    highlightthickness = 0,
    command = Clean,
    relief = "flat")

b18.place(
    x = 803, y = 510,
    width = 90,
    height = 35)
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
    x = 380, y = 229,
    width = 44,
    height = 16)
#****************************************************

showTable()
listBox.bind('<Double-Button-1>',Remplir)
NDotation()
BestP()
LessP()

dotation.resizable(False, False)
dotation.mainloop()
