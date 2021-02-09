import mysql.connector
import smtplib
from email.message import EmailMessage

#conect db
mydb = mysql.connector.connect(
       host="localhost",
       user = "root",
       password = "",
       database = "schoolsupply" 
    )
mycursor = mydb.cursor()


def menu():
    print("Wellcome to Peter School Supply")
    print(" [1] Add new Customer ")
    print(" [2] Add new Item ")
    print(" [3] Item Brought entry")
    print(" [4] Item add entry")
    print(" [5] Show All Customer detail")
    print(" [6] Show All item detail")
    print(" [7] Show All Customer History detail")
    option = int(input("Enter your choice : "))
    print("")
    return option

def addcust():
    print("Customer Entry")
    name = input("Enter Customer Name : ")
    adress = input("Enter Customer Address : ")
    contact = input("Enter Customer Contact : ")
    email = input("Enter Customer Email : ")
    sql = "INSERT INTO customer (name, address, contact,email) VALUES (%s, %s,%s,%s)"
    val = (name,adress,contact,email)
    #print(val)
    mycursor.execute(sql, val)
    mydb.commit()

def additem():
    print("Item Entry")
    itemname = input("Enter Item name : ")
    price = input("Enter Item price (Rs) : ")
    itemnumber = input("Enter total number of item : ")
    sql = "INSERT INTO item (itemname, price, itemnumber) VALUES (%s, %s,%s)"
    val = (itemname,price,itemnumber)
    #print(val)
    mycursor.execute(sql, val)
    mydb.commit()

def checkstock():
    #mail modular      
    #read password form file 
    f = open("password.txt","r")
    password = f.read()
    #item
    mycursor.execute("SELECT * FROM item")
    myitem = mycursor.fetchall()
    for x in myitem:
        # print(x[3],x[1])
        if(int(x[3]) < 10):  
            msg = EmailMessage()
            msg.set_content(x[1]+" is running out of stock, Left : "+x[3])
            msg['Subject'] = "Going out of stock"
            msg['From'] = "peterkarki99@gmail.com"
            msg['To'] = "peter.karki0422@gmail.com"

            # Send the message via our own SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("peterkarki99@gmail.com", password)
            server.send_message(msg)
            server.quit()


   

def itementry():
    print("Item Entry ")
    name = input("Enter Customer Name : ")
    item = input("Enter Product Name Customer brought : ")
    quantity = input("Enter Quantity : ")
    mycursor.execute("SELECT * FROM item")
    myitem = mycursor.fetchall()
    price = 0
    for i in myitem:
        if(i[1] == item):
            price = int(i[2])
    totalprice = price*int(quantity)
    
    mycursor.execute("SELECT * FROM supplydetail")
    mysupply = mycursor.fetchall()
    discount = 0
    for i in mysupply:
        if(i[1] == name):
            discount = statdiss(i[4])
    totalprice = totalprice - totalprice*discount
    print("Total price : "+str(totalprice))
    




    print()
    res = checkdb(name,item)
    if(res == True):
        
        #decrease Quantity 
        #item
       
        for i in myitem:
            temp = 0
            if(i[1] == item):
                if(int(quantity) <= int(i[3])):
                    temp = int(i[3])
                    temp = temp - int(quantity)
                    mycursor.execute("UPDATE item SET itemnumber = '"+str(temp)+"'WHERE itemid = "+str(i[0])+";")
                    mydb.commit()
                else:
                    print("Item reamining in stock : "+i[3]+" and item customer buying is : "+item)

        mycursor.execute("SELECT * FROM supplydetail")
        myrecord = mycursor.fetchall()
        for i in myrecord:
            tempmoney = 0
            tempitem =""
            tempstat = ""
            if(i[1] == name):
                tempmoney = int(i[3])
                tempitem = i[2]
                tempmoney = tempmoney+totalprice
                tempitem = "|"+tempitem + item +"*"+quantity+" | "
                stat = custstat(tempmoney)
                mycursor.execute("UPDATE supplydetail SET item='"+tempitem+"',money='"+str(tempmoney)+"',stat='"+stat+"'  WHERE supplyid = "+str(i[0])+";")
                mydb.commit()
            else:
                stat = custstat(totalprice)
                tempitem = item + "*" +quantity
                mycursor.execute("INSERT INTO supplydetail (custname, item, money,stat) VALUES ('"+name+"','"+tempitem+"','"+str(totalprice)+"','"+stat+"');")
                mydb.commit()

    else:
        print("Either Name or item doesnt exist")

def custstat(money):
    if(money >= 50000):
        return "Gold"
    elif(money >= 30000 and money <= 49999):
        return "Silver"
    elif(money >= 15000 and money <= 29999):
        return "bronze"
    else:
        return "normal"

def statdiss(stat):
    if(stat == "normal"):
        return 0.02
    elif(stat == "bronze"):
        return 0.15
    elif(stat == "Silver"):
        return 0.25
    elif(stat == "Gold"):
        return 0.40

def itemadd():
    mycursor.execute("SELECT * FROM item")
    myitem = mycursor.fetchall()
    print("Item add")
    name = input("Enter Item name : ")
    quantity = int(input("Enter Added Item : "))
    for i in myitem:
        temp = 0
        if(i[1] == name):
            temp = int(i[3])
            temp = temp+quantity
            mycursor.execute("UPDATE item SET itemnumber = '"+str(temp)+"'WHERE itemid = "+str(i[0])+";")
            mydb.commit()
            break
    
    

def checkdb(name, item):
    flag1,flag2 = True,False
    #customer
    mycursor.execute("SELECT * FROM customer")
    myresult = mycursor.fetchall()
    #item
    mycursor.execute("SELECT * FROM item")
    myitem = mycursor.fetchall()
    #name check
    for i in myresult:
        if(i[1] == name):
            flag1 = True
            break
        else:
            flag1 = False
    for i in myitem:
        if(i[1] == item):
            flag2 = True
            break
        else:
            flag2 = False
    if(flag1 == True and flag2 == True):
        return True
    else:
        return False

def custdetail():
    mycursor.execute("SELECT * FROM customer")
    myresult = mycursor.fetchall()
    print("Cust Id   Name \t\t address \t contact \t email")
    for i in myresult:
        print(str(i[0])+" \t "+i[1]+" \t "+i[2]+" \t "+i[3]+" \t "+i[4])

def itemdetail():
    mycursor.execute("SELECT * FROM item")
    myresult = mycursor.fetchall()
    print("item Id   Name \t\t price \t Quantity")
    for i in myresult:
        print(str(i[0])+" \t "+i[1]+" \t "+i[2]+" \t "+i[3])

def supplydetail():
    mycursor.execute("SELECT * FROM supplydetail")
    myresult = mycursor.fetchall()
    print("Supply Id   Name \t Stat \t\t Total Spend \t Total Item brought")
    for i in myresult:
        print(str(i[0])+" \t "+i[1]+" \t "+i[4]+" \t "+i[3]+" \t\t "+i[2])



def main():
    option = menu()
    if(option == 1):
        addcust()
    elif(option == 2):
        additem()
    elif(option ==3):
        itementry()
    elif(option ==4):
        itemadd()
    elif(option ==5):
        custdetail()
    elif(option ==6):
        itemdetail()
    elif(option ==7):
        supplydetail()





# checkstock()
main()

    
