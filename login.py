import sys
from PyQt5 import QtCore, QtWidgets
import psycopg2
import pandas as pd

class hrWindow (QtWidgets.QWidget):

    switch_updateEmp = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_EmpSales = QtCore.pyqtSignal(psycopg2.extensions.connection)
    
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('HR Page')
        vBox = QtWidgets.QVBoxLayout()
        self.button1 = QtWidgets.QPushButton('Access and update of employee information')
        self.button1.clicked.connect(lambda: self.switch1(connection))
        vBox.addWidget(self.button1)
        
        self.button2 = QtWidgets.QPushButton('View of employee and associated sales number')
        self.button2.clicked.connect(lambda: self.switch2(connection))
        vBox.addWidget(self.button2)
        
        self.setLayout(vBox)
    
    def switch1(self, connection):
        self.switch_updateEmp.emit(connection)        
    def switch2(self, connection):
        self.switch_EmpSales.emit(connection)      

  
class windowUpdateEmp(QtWidgets.QWidget):
    
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.changes = ''
        self.row_chg = -1
        self.col_chg = -1
        self.newdata = ''
        self.model=''
        self.setWindowTitle('Employee')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)

        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection))

        self.buttonUpdate = QtWidgets.QPushButton('Update')
        self.buttonUpdate.clicked.connect(lambda: self.btn_Update(connection))
        
        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        layout.addWidget(self.buttonUpdate)
        self.setLayout(layout)
        
    def btn_clk(self, connection):
        df=pd.DataFrame()
        try:  
            
            query2 = "select * from employee;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("Table retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass

        #print(df)
        self.model = DataFrameModel(df)
        self.tableView.setModel(self.model)
        #self.tableView.itemSelectionChanged.connect(self.on_selectionChanged)
             
    def btn_Update(self, connection):
        self.changes = self.model._data
        self.row_chg = self.model.rowchg
        self.col_chg = self.model.colchg
        self.newdata = self.model.newdata 
        #print(self.row_chg, self.col_chg, self.newdata)
        flag = ''
        try:
            cursor = connection.cursor()
            if(self.col_chg==1):
                login_sql = """UPDATE employee
                            SET "firstName" = %s
                            WHERE employee."employeeID" = %s;"""
                cursor.execute(login_sql, (self.newdata, str(self.changes.iloc[self.row_chg, self.col_chg-1]))) 
                flag = "first Name"
            elif(self.col_chg==2):
                login_sql = """UPDATE employee
                            SET "lastName" = %s
                            WHERE employee."employeeID"" = %s;"""
                cursor.execute(login_sql, (self.newdata, str(self.changes.iloc[self.row_chg, self.col_chg-2]))) 
                flag = "last Name"
            elif(self.col_chg==3):
                login_sql = """UPDATE employee
                            SET "SSN" = %s
                            WHERE employee."employeeID" = %s;"""
                cursor.execute(login_sql, (self.newdata, int(self.changes.iloc[self.row_chg, self.col_chg-3]))) 
                flag = "SSN"
            elif(self.col_chg==4):
                login_sql = """UPDATE employee
                            SET salary = %s
                            WHERE employee."employeeID" = %s;"""
                cursor.execute(login_sql, (self.newdata, int(self.changes.iloc[self.row_chg, self.col_chg-4]))) 
                flag = "salary"
            elif(self.col_chg==5):
                login_sql = """UPDATE employee
                            SET "payType" = %s
                            WHERE employee."employeeID" = %s;"""
                cursor.execute(login_sql, (self.newdata, str(self.changes.iloc[self.row_chg, self.col_chg-5]))) 
                flag = "payType"
            elif(self.col_chg==6):
                login_sql = """UPDATE employee
                            SET "jobType" = %s
                            WHERE employee."employeeID" = %s;"""
                cursor.execute(login_sql, (self.newdata, str(self.changes.iloc[self.row_chg, self.col_chg-6]))) 
                flag = "jobType"
            elif(self.col_chg==8):
                login_sql = """UPDATE employee
                            SET bonus = %s
                            WHERE employee."employeeID" = %s;"""
                cursor.execute(login_sql, (self.newdata, int(self.changes.iloc[self.row_chg, self.col_chg-8]))) 
                flag = "bonus"

            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            print ("Update Employee failed,", error)           
   
        finally:
            #closing database connection.
                if(connection):
                    print("Update employee successful,", flag, "updated to", self.newdata)
                    pass      
  
class windowEmpSales(QtWidgets.QWidget):

    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Employee and associated sales number')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)


        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection))

        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        
    def btn_clk(self,connection):
        df=""
        try:         
            query2 = "select * from employee_sales;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("employee_sales table retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass
        model = DataFrameModel(df)
        self.tableView.setModel(model)


class engrWindow (QtWidgets.QWidget):

    switch_updateInv = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_updateModel = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_engrView = QtCore.pyqtSignal(psycopg2.extensions.connection)  
    
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Engineer Page')
        vBox = QtWidgets.QVBoxLayout()
        self.button1 = QtWidgets.QPushButton('Access and update model')
        self.button1.clicked.connect(lambda: self.switch1(connection))
        vBox.addWidget(self.button1)
        
        self.button2 = QtWidgets.QPushButton('Access and update inventory')
        self.button2.clicked.connect(lambda: self.switch2(connection))
        vBox.addWidget(self.button2)
        
        self.button3 = QtWidgets.QPushButton('Engineer view of employee')
        self.button3.clicked.connect(lambda: self.switch3(connection))
        vBox.addWidget(self.button3)
        
        self.setLayout(vBox)
    
    def switch1(self, connection):
        self.switch_updateModel.emit(connection)        
    def switch2(self, connection):
        self.switch_updateInv.emit(connection)      
    def switch3(self, connection):
        self.switch_engrView.emit(connection)  
      
class windowUpdateInv(QtWidgets.QWidget):
    
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.changes = ''
        self.row_chg = -1
        self.col_chg = -1
        self.newdata = ''
        self.model=''
        self.setWindowTitle('Inventory')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)

        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection))

        self.buttonUpdate = QtWidgets.QPushButton('Update')
        self.buttonUpdate.clicked.connect(lambda: self.btn_Update(connection))
        
        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        layout.addWidget(self.buttonUpdate)
        self.setLayout(layout)
        
    def btn_clk(self, connection):
        df=pd.DataFrame()
        try:  
            
            query2 = "select * from inventory;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("Table retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass

        #print(df)
        self.model = DataFrameModel(df)
        self.tableView.setModel(self.model)
        #self.tableView.itemSelectionChanged.connect(self.on_selectionChanged)
        
        
    def btn_Update(self, connection):
        self.changes = self.model._data
        self.row_chg = self.model.rowchg
        self.col_chg = self.model.colchg
        self.newdata = self.model.newdata 
        #print(self.row_chg, self.col_chg, self.newdata)
        flag = ''
        try:
            cursor = connection.cursor()
            if(self.col_chg==1):
                login_sql = """UPDATE inventory
                            SET cost = %s
                            WHERE inventory."inventoryID" = %s;"""
                cursor.execute(login_sql, (self.newdata, self.changes.iloc[self.row_chg, self.col_chg-1])) 
                flag = "cost"
            elif(self.col_chg==2):
                login_sql = """UPDATE inventory
                            SET "leadTime" = %s
                            WHERE inventory."inventoryID" = %s;"""
                cursor.execute(login_sql, (self.newdata, self.changes.iloc[self.row_chg, self.col_chg-2])) 
                flag = "Lead Time"
            elif(self.col_chg==3):
                login_sql = """UPDATE inventory
                            SET category = %s
                            WHERE inventory."inventoryID" = %s;"""
                cursor.execute(login_sql, (self.newdata, self.changes.iloc[self.row_chg, self.col_chg-3])) 
                flag = "category"
            elif(self.col_chg==4):
                login_sql = """UPDATE inventory
                            SET "itemCount" = %s
                            WHERE inventory."inventoryID" = %s;"""
                cursor.execute(login_sql, (self.newdata, self.changes.iloc[self.row_chg, self.col_chg-4])) 
                flag = "item Count"
            #role = cursor.fetchone()[0]  
            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            print ("Update Inventory failed,", error)           
   
        finally:
            #closing database connection.
                if(connection):
                    print("Update inventory successful,", flag, "updated to", self.newdata)
                    pass      

class windowUpdateModel(QtWidgets.QWidget):
    
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.changes = ''
        self.row_chg = -1
        self.col_chg = -1
        self.newdata = ''
        self.model=''
        self.setWindowTitle('Model')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)

        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection))

        self.buttonUpdate = QtWidgets.QPushButton('Update')
        self.buttonUpdate.clicked.connect(lambda: self.btn_Update(connection))
        
        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        layout.addWidget(self.buttonUpdate)
        self.setLayout(layout)
        
    def btn_clk(self, connection):
        df=pd.DataFrame()
        try:  
            
            query2 = "select * from model;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("Table retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass

        #print(df)
        self.model = DataFrameModel(df)
        self.tableView.setModel(self.model)
        #self.tableView.itemSelectionChanged.connect(self.on_selectionChanged)
             
    def btn_Update(self, connection):
        self.changes = self.model._data
        self.row_chg = self.model.rowchg
        self.col_chg = self.model.colchg
        self.newdata = self.model.newdata 
        #print(self.row_chg, self.col_chg, self.newdata)
        flag = ''
        try:
            cursor = connection.cursor()
            if(self.col_chg==1):
                login_sql = """UPDATE model
                            SET "salePrice" = %s
                            WHERE model."modelNumber" = %s;"""
                cursor.execute(login_sql, (self.newdata, self.changes.iloc[self.row_chg, self.col_chg-1])) 
                flag = "salePrice"

            #role = cursor.fetchone()[0]  
            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            print ("Update Model failed,", error)           
   
        finally:
            #closing database connection.
                if(connection):
                    print("Update model successful,", flag, "updated to", self.newdata)
                    pass      

class windowEngrView(QtWidgets.QWidget):

    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Employee (Engineer View)')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)


        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection))

        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        
    def btn_clk(self,connection):
        df=""
        try:         
            query2 = "select * from engineer_view;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("Employee table retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass
                    #connection.close()
                    #print("PostgreSQL connection is closed")
        #print(df)
        model = DataFrameModel(df)
        #print(model)
        self.tableView.setModel(model)
        
class saleWindow (QtWidgets.QWidget):

    switch_viewUpdateCus = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_cr8Order = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_salesReport = QtCore.pyqtSignal(psycopg2.extensions.connection)  
    
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Sales Page')
        vBox = QtWidgets.QVBoxLayout()
        self.button1 = QtWidgets.QPushButton('View and update customer')
        self.button1.clicked.connect(lambda: self.switch1(connection))
        vBox.addWidget(self.button1)
        
        self.button2 = QtWidgets.QPushButton('Create an Order')
        self.button2.clicked.connect(lambda: self.switch2(connection))
        vBox.addWidget(self.button2)
        
        self.button3 = QtWidgets.QPushButton('Access sales reports')
        self.button3.clicked.connect(lambda: self.switch3(connection))
        vBox.addWidget(self.button3)
        
        self.setLayout(vBox)
            
    def switch1(self, connection):
        self.switch_viewUpdateCus.emit(connection)      
    def switch2(self, connection):
        self.switch_cr8Order.emit(connection)
    def switch3(self, connection):
        self.switch_salesReport.emit(connection)      
        
class windowviewUpdateCus(QtWidgets.QWidget):
    
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.changes = ''
        self.row_chg = -1
        self.col_chg = -1
        self.newdata = ''
        self.model=''
        self.setWindowTitle('Customer')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)

        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection))

        self.buttonUpdate = QtWidgets.QPushButton('Update')
        self.buttonUpdate.clicked.connect(lambda: self.btn_Update(connection))
        
        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        layout.addWidget(self.buttonUpdate)
        self.setLayout(layout)
        
    def btn_clk(self, connection):
        df=pd.DataFrame()
        try:  
            
            query2 = "select * from customer;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("Table retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass

        #print(df)
        self.model = DataFrameModel(df)
        self.tableView.setModel(self.model)
        #self.tableView.itemSelectionChanged.connect(self.on_selectionChanged)
        
        
    def btn_Update(self, connection):
        self.changes = self.model._data
        self.row_chg = self.model.rowchg
        self.col_chg = self.model.colchg
        self.newdata = self.model.newdata 
        #print(self.row_chg, self.col_chg, self.newdata)
        flag = ''
        try:
            cursor = connection.cursor()
            if(self.col_chg==1):
                login_sql = """UPDATE customer
                            SET "firstName" = %s
                            WHERE customer."customerID" = %s;"""
                cursor.execute(login_sql, (self.newdata, self.changes.iloc[self.row_chg, self.col_chg-1])) 
                flag = "First Name"
            elif(self.col_chg==2):
                login_sql = """UPDATE customer
                            SET "lastName" = %s
                            WHERE customer."customerID" = %s;"""
                cursor.execute(login_sql, (self.newdata, self.changes.iloc[self.row_chg, self.col_chg-2])) 
                flag = "last Name"
            #role = cursor.fetchone()[0]  
            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            print ("Create order failed,", error)           
   
        finally:
            #closing database connection.
                if(connection):
                    print("Update customer successful,", flag, "updated to", self.newdata)
                    pass
                
class windowcr8Order(QtWidgets.QWidget):
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Orders')

        vBox = QtWidgets.QVBoxLayout()
        hBox1 = QtWidgets.QHBoxLayout()
        hBox2 = QtWidgets.QHBoxLayout()
        hBox3 = QtWidgets.QHBoxLayout()
        hBox4 = QtWidgets.QHBoxLayout()
        vBox.setSpacing(-20)
 
        #vBox.setMargin(0)
        # orderNumber
        self.orderNumber = QtWidgets.QLineEdit("3234")
        hBox1.addWidget(QtWidgets.QLabel("orderNumber"))
        hBox1.addWidget(self.orderNumber)
    
        # billCost
        self.billCost = QtWidgets.QLineEdit("20")
        hBox2.addWidget(QtWidgets.QLabel("billCost (money only)"))
        hBox2.addWidget(self.billCost)
        
        # quantity
        self.quantity = QtWidgets.QLineEdit("1")
        hBox3.addWidget(QtWidgets.QLabel("quantity (integer only)"))
        hBox3.addWidget(self.quantity)
        
        # modelNumber
        self.modelNumber = QtWidgets.QLineEdit("4255")
        hBox4.addWidget(QtWidgets.QLabel("modelNumber (integer only)"))
        hBox4.addWidget(self.modelNumber)
        
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox3)
        vBox.addLayout(hBox4)
        self.button = QtWidgets.QPushButton('Create new order')
        self.button.clicked.connect(lambda: self.btn_clk( connection,
                                                       self.orderNumber.text(), 
                                                       self.billCost.text(),
                                                       self.quantity.text(), 
                                                       self.modelNumber.text()))
        vBox.addWidget(self.button)
        self.setLayout(vBox)
        
    def btn_clk(self, connection, orderNumber, billCost, quantity, modelNumber):
        try:   
            cursor = connection.cursor()
            login_sql = 'INSERT INTO orders ("orderNumber", "billCost", quantity, "modelNumber") VALUES (%s, %s, %s, %s);'
   
            cursor.execute(login_sql, (orderNumber, billCost, quantity, modelNumber)) #Login in ID add password
            #role = cursor.fetchone()[0]  
            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            print ("Create order failed,", error)           
   
        finally:
            #closing database connection.
                if(connection):
                    pass
        
class windowSalesReport(QtWidgets.QWidget):

    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Sales Report')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)


        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection))

        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        
    def btn_clk(self,connection):
        df=""
        try:         
            query2 = "select * from revenue_report;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("Sales Report retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass
                    #connection.close()
                    #print("PostgreSQL connection is closed")
        #print(df)
        model = DataFrameModel(df)
        #print(model)
        self.tableView.setModel(model)

class AdminWindow(QtWidgets.QWidget):
    switch_adminView = QtCore.pyqtSignal(psycopg2.extensions.connection, str)
    switch_cr8Emp = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch = QtCore.pyqtSignal(psycopg2.extensions.connection)
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Admin Page')
        vBox = QtWidgets.QVBoxLayout()
        self.cr8Employee_btn = QtWidgets.QPushButton('Create a new employee')
        self.cr8Employee_btn.clicked.connect(lambda: self.switch_cr8Emp_btn(connection))
        vBox.addWidget(self.cr8Employee_btn)
        
        self.setupTable_btn = QtWidgets.QPushButton('Set up table')
        self.setupTable_btn.clicked.connect(self.switch1)
        vBox.addWidget(self.setupTable_btn)
        self.grantAccess_btn = QtWidgets.QPushButton('Grant Access')
        self.grantAccess_btn.clicked.connect(self.switch1)
        vBox.addWidget(self.grantAccess_btn)
        
        self.btn1 = QtWidgets.QPushButton('Employee and model expense')
        self.btn1.clicked.connect(lambda: self.switch_view(connection, "employee_expense"))
        vBox.addWidget(self.btn1)
        
        self.btn2 = QtWidgets.QPushButton('Frequency Report')
        self.btn2.clicked.connect(lambda: self.switch_view(connection, "frequency_report"))
        vBox.addWidget(self.btn2)
        
        self.btn3 = QtWidgets.QPushButton('Order Report')
        self.btn3.clicked.connect(lambda: self.switch_view(connection, "order_report"))
        vBox.addWidget(self.btn3)
        
        self.btn4 = QtWidgets.QPushButton('Revenue Report')
        self.btn4.clicked.connect(lambda: self.switch_view(connection, "revenue_report"))
        vBox.addWidget(self.btn4)
        
        self.setLayout(vBox)

    def switch_view(self, connection, view_sql):
        self.switch_adminView.emit(connection, view_sql)

    def switch_cr8Emp_btn(self, connection):
        self.switch_cr8Emp.emit(connection)
    
    def switch1(self, connection):
        self.show_window_cr8Emp.emit(connection)
        
class windowcr8Emp(QtWidgets.QWidget):
    def __init__(self, connection):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Orders')

        vBox = QtWidgets.QVBoxLayout()
        hBox1 = QtWidgets.QHBoxLayout()
        hBox2 = QtWidgets.QHBoxLayout()
        hBox3 = QtWidgets.QHBoxLayout()
        hBox4 = QtWidgets.QHBoxLayout()
        hBox5 = QtWidgets.QHBoxLayout()
        hBox6 = QtWidgets.QHBoxLayout()
        hBox7 = QtWidgets.QHBoxLayout()
        hBox8 = QtWidgets.QHBoxLayout()
        hBox9 = QtWidgets.QHBoxLayout()
        vBox.setSpacing(-20)
        
        self.employeeID = QtWidgets.QLineEdit("1000")
        hBox1.addWidget(QtWidgets.QLabel("Employee ID"))
        hBox1.addWidget(self.employeeID)
        
        self.fname = QtWidgets.QLineEdit("John")
        hBox2.addWidget(QtWidgets.QLabel("First name"))
        hBox2.addWidget(self.fname)

        self.lname = QtWidgets.QLineEdit("Doe")
        hBox3.addWidget(QtWidgets.QLabel("Last name"))
        hBox3.addWidget(self.lname)

        self.ssn = QtWidgets.QLineEdit("1234")
        hBox4.addWidget(QtWidgets.QLabel("SSN"))
        hBox4.addWidget(self.ssn)

        self.salary = QtWidgets.QLineEdit("2000")
        hBox5.addWidget(QtWidgets.QLabel("salary"))
        hBox5.addWidget(self.salary)

        self.payType = QtWidgets.QLineEdit("cash")
        hBox6.addWidget(QtWidgets.QLabel("Pay Type"))
        hBox6.addWidget(self.payType)
        
        self.jobType = QtWidgets.QLineEdit("engineer")
        hBox7.addWidget(QtWidgets.QLabel("Job Type"))
        hBox7.addWidget(self.jobType)
        
        self.userID = QtWidgets.QLineEdit("6789")
        hBox8.addWidget(QtWidgets.QLabel("userID"))
        hBox8.addWidget(self.userID)
        
        self.bonus = QtWidgets.QLineEdit("20")
        hBox9.addWidget(QtWidgets.QLabel("bonus"))
        hBox9.addWidget(self.bonus)
        
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox3)
        vBox.addLayout(hBox4)
        vBox.addLayout(hBox5)
        vBox.addLayout(hBox6)
        vBox.addLayout(hBox7)
        vBox.addLayout(hBox8)
        vBox.addLayout(hBox9)
        self.button = QtWidgets.QPushButton('Create new order')
        self.button.clicked.connect(lambda: self.btn_clk( connection,
                                                       self.employeeID.text(), 
                                                       self.fname.text(),
                                                       self.lname.text(), 
                                                       self.ssn.text(),
                                                       self.salary.text(), 
                                                       self.payType.text(),
                                                       self.jobType.text(), 
                                                       self.userID.text(),
                                                       self.bonus.text(),
                                                       ))
        vBox.addWidget(self.button)
        self.setLayout(vBox)
        
    def btn_clk(self, connection, employeeID, fname, lname, ssn, salary, payType, jobType, userID, bonus):
        try:   
            cursor = connection.cursor()
            login_sql = 'INSERT INTO employee ("employeeID", "firstName", "lastName", "SSN", salary, "payType", "jobType", "userID", bonus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
   
            cursor.execute(login_sql, (employeeID, fname, lname, ssn, salary, payType, jobType, userID, bonus)) #Login in ID add password
            #role = cursor.fetchone()[0]  
            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            print ("Create employee failed,", error)           
   
        finally:
            #closing database connection.
                if(connection):
                    print("Employee created successfully")
                
class windowAdminView(QtWidgets.QWidget):
    def __init__(self, connection, view_sql):
        QtWidgets.QWidget.__init__(self)
        if(view_sql == "employee_expense"):
            self.setWindowTitle("Employee and model expense")
        else:
            self.setWindowTitle(view_sql)
        layout = QtWidgets.QGridLayout()
        
        self.tableView = QtWidgets.QTableView(self)
        
        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(lambda: self.btn_clk(connection, view_sql))

        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        if(view_sql == "employee_expense"):
            self.tableView2 = QtWidgets.QTableView(self)
            layout.addWidget(self.tableView2)
        self.setLayout(layout)
        
    def btn_clk(self,connection, view_sql):
        df=""
        try:         
            query2 = "select * from "+view_sql+";"
            print(query2)
            df = pd.read_sql(query2, connection)                                        
            
            print(view_sql+ " retrieved successfully in PostgreSQL")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):      
                    pass
        model = DataFrameModel(df)
        self.tableView.setModel(model)
        
        if(view_sql == "employee_expense"):
            try:         
                query1 = "select * from model_expense;"
                print(query1)
                df = pd.read_sql(query1, connection)                                        
                
                print(view_sql+ " retrieved successfully in PostgreSQL")
                #print(df)
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
            finally:
                #closing database connection.
                    if(connection):      
                        pass
            model2 = DataFrameModel(df)
            self.tableView2.setModel(model2)
            
class Login(QtWidgets.QWidget):

    switch_SaleWindow = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_AdminWindow = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_EngrWindow = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_hrWindow = QtCore.pyqtSignal(psycopg2.extensions.connection)
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')

        vBox = QtWidgets.QVBoxLayout()
        
        # Username
        self.username = QtWidgets.QLineEdit("admin1")
        vBox.addWidget(QtWidgets.QLabel("Username"))
        vBox.addWidget(self.username)
    
        # Password
        self.pw = QtWidgets.QLineEdit()
        self.pw.setEchoMode(QtWidgets.QLineEdit.Password)
        vBox.addWidget(QtWidgets.QLabel("Password"))
        vBox.addWidget(self.pw)
        
        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(lambda: self.login(self.username.text(), self.pw.text()))

        vBox.addWidget(self.button)

        self.setLayout(vBox)

    def login(self, username, pw):
        role=False
        connection=''
        try:
            connection = psycopg2.connect(user = username,
                                          password = pw, #Your password in psql
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "try4")   #Your db name
        
            cursor = connection.cursor()
            login_sql = """
                        with roles(usernam, role) as 
                        (SELECT r.rolname as username,r1.rolname as "role"
                        FROM pg_catalog.pg_roles r JOIN pg_catalog.pg_auth_members m
                        ON (m.member = r.oid)
                        JOIN pg_roles r1 ON (m.roleid=r1.oid)                                  
                        WHERE r.rolcanlogin
                        ORDER BY 1)
                        select role from roles where usernam = %s;
                        """
   
            cursor.execute(login_sql, [username]) #Login in ID add password
            role = cursor.fetchone()[0]    
            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            #print ("Error while connecting to PostgreSQL", error)           
            print('Error login')
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Incorrect ID or Password. The ID or password you entered is incorrect.")
            msg.setInformativeText('Please try again.')
            msg.setWindowTitle("Error Login")
            msg.exec_()
        finally:
            #closing database connection.
                if(connection):
                    pass
                    #cursor.close()
                    #connection.close()
                    #print("PostgreSQL connection is closed")
        if(role):
            print("User Id and password found in database")
            #print(type(role), a)
            #Switch case for different type of user
            if 'admin' in role:
                self.switch_AdminWindow.emit(connection)
            elif 'sales' in role:
                self.switch_SaleWindow.emit(connection)    
            elif 'engineer' in role:
                self.switch_EngrWindow.emit(connection)    
            elif 'hr' in role:
                self.switch_hrWindow.emit(connection)  

class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_SaleWindow.connect(self.show_SaleWindow)
        self.login.switch_AdminWindow.connect(self.show_AdminWindow)
        self.login.switch_EngrWindow.connect(self.show_EngrWindow)
        self.login.switch_hrWindow.connect(self.show_HrWindow)
        self.login.show()

    def show_SaleWindow(self, connection):
        self.sale_Window = saleWindow(connection)
        self.sale_Window.switch_salesReport.connect(lambda: self.show_window_salesReport(connection))
        self.sale_Window.switch_viewUpdateCus.connect(lambda: self.show_window_viewUpdateCus(connection))
        self.sale_Window.switch_cr8Order.connect(lambda: self.show_window_cr8Order(connection))
        self.login.close()
        self.sale_Window.show()
        self.sale_Window.setFixedSize(1080,720)
    
    def show_window_viewUpdateCus(self, connection):
        self.viewUpdateCus_Window = windowviewUpdateCus(connection)
        self.sale_Window.close()
        self.viewUpdateCus_Window.show()
        self.viewUpdateCus_Window.setFixedSize(1080,720)
    
    def show_window_cr8Order(self, connection):
        self.cr8Order_Window = windowcr8Order(connection)
        self.sale_Window.close()
        self.cr8Order_Window.show()
        self.cr8Order_Window.setFixedSize(1080,720)
        
    def show_window_salesReport(self, connection):
        self.salesReport_Window = windowSalesReport(connection)
        self.sale_Window.close()
        self.salesReport_Window.show()
        self.salesReport_Window.setFixedSize(1080,720)
    
    def show_AdminWindow(self, connection):
        self.admin_Window = AdminWindow(connection)
        self.admin_Window.switch_adminView.connect(self.show_window_adminView)
        self.admin_Window.switch_cr8Emp.connect(lambda: self.show_window_cr8Emp(connection))
        self.admin_Window.switch.connect(lambda: self.show_window_cr8Emp(connection))
        self.login.close()
        self.admin_Window.show()
        self.admin_Window.setFixedSize(1080,720)

    def show_window_cr8Emp(self, connection):
        self.cr8Emp_Window = windowcr8Emp(connection)
        self.admin_Window.close()
        self.cr8Emp_Window.show()
        self.cr8Emp_Window.setFixedSize(1080,720)
        
    def show_window_adminView(self, connection, view_sql):
        self.adminView_Window = windowAdminView(connection, view_sql)
        self.admin_Window.close()
        self.adminView_Window.show()
        self.adminView_Window.setFixedSize(1080,720)  
    
    def show_EngrWindow(self, connection):
        self.engr_Window = engrWindow(connection)
        self.engr_Window.switch_updateInv.connect(lambda: self.show_window_updateInv(connection))
        self.engr_Window.switch_updateModel.connect(lambda: self.show_window_updateModel(connection))
        self.engr_Window.switch_engrView.connect(lambda: self.show_window_engrView(connection))
        self.login.close()
        self.engr_Window.show()
        self.engr_Window.setFixedSize(1080,720)
       
    def show_window_updateInv(self, connection):
        self.updateInv_Window = windowUpdateInv(connection)
        self.engr_Window.close()
        self.updateInv_Window.show()
        self.updateInv_Window.setFixedSize(1080,720)  
     
    def show_window_updateModel(self, connection):
        self.updateModel_Window = windowUpdateModel(connection)
        self.engr_Window.close()
        self.updateModel_Window.show()
        self.updateModel_Window.setFixedSize(1080,720)  
    
    def show_window_engrView(self, connection):
        self.engrView_Window = windowEngrView(connection)
        self.engr_Window.close()
        self.engrView_Window.show()
        self.engrView_Window.setFixedSize(1080,720)  
    
    def show_HrWindow(self, connection):
        self.hr_Window = hrWindow(connection)
        self.hr_Window.switch_updateEmp.connect(lambda: self.show_window_updateEmp(connection))
        self.hr_Window.switch_EmpSales.connect(lambda: self.show_window_EmpSales(connection))
        self.login.close()
        self.hr_Window.show()
        self.hr_Window.setFixedSize(1080,720)
        
    def show_window_updateEmp(self, connection):
        self.updateEmp_Window = windowUpdateEmp(connection)
        self.hr_Window.close()
        self.updateEmp_Window.show()
        self.updateEmp_Window.setFixedSize(1080,720)  

    def show_window_EmpSales(self, connection):
        self.empSales_Window = windowEmpSales(connection)
        self.hr_Window.close()
        self.empSales_Window.show()
        self.empSales_Window.setFixedSize(1080,720)  
        
class DataFrameModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self.rowchg=0
        self.colchg=0
        self.newdata=''
            
    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role != QtCore.Qt.EditRole:
            return False
        row = index.row()
        if row < 0 or row >= len(self._data.values):
            return False
        column = index.column()
        if column < 0 or column >= self._data.columns.size:
            return False
        self._data.iloc[row, column] = value
        self.dataChanged.emit(index, index)    
        #print(self.rowchg, self.colchg, self.newdata)
        self.rowchg=row
        self.colchg=column
        self.newdata=value
        #print(self.rowchg, self.colchg, self.newdata)
        return True

    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        flags |= QtCore.Qt.ItemIsDragEnabled
        flags |= QtCore.Qt.ItemIsDropEnabled
        return flags
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()