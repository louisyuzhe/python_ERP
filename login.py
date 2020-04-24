import sys
from PyQt5 import QtCore, QtWidgets
import psycopg2
import pandas as pd

class engrWindow (QtWidgets.QWidget):

    switch_updateInv = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_updateModel = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_employeeView = QtCore.pyqtSignal(psycopg2.extensions.connection)  
    
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
        
        self.button3 = QtWidgets.QPushButton('Limited view of employee')
        self.button3.clicked.connect(self.switch3)
        vBox.addWidget(self.button3)
        
        self.setLayout(vBox)
    
    def switch1(self, connection):
        self.switch_updateModel.emit(connection)        
    def switch2(self, connection):
        self.switch_updateInv.emit(connection)      
    def switch3(self, connection):
        self.switch_employeeView.emit(connection)  
      
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

class saleWindow (QtWidgets.QWidget):

    switch_viewUpdateCus = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_cr8Order = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_salesReport = QtCore.pyqtSignal()  
    
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
        self.button3.clicked.connect(self.switch3)
        vBox.addWidget(self.button3)
        
        self.setLayout(vBox)
            
    def switch1(self, connection):
        self.switch_viewUpdateCus.emit(connection)      
    def switch2(self, connection):
        self.switch_cr8Order.emit(connection)
    def switch3(self):
        self.switch_salesReport.emit()      
        
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
        
class WindowTwo(QtWidgets.QWidget):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Window Two')
        layout = QtWidgets.QGridLayout()
        self.tableView = QtWidgets.QTableView(self)

                            
        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Display')
        self.button.clicked.connect(self.btn_clk)

        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        
    def btn_clk(self):
        print("starts")
        df=""
        try:
            connection = psycopg2.connect(user = "postgres",
                                          password = "yuzhelim", #Your password in psql
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "try1")   #Your db name
            
            query2 = "select * from instructor;"
            
            df = pd.read_sql(query2, connection)                                        
            
            print("Table retrieved successfully in PostgreSQL ")
            #print(df)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):            
                    connection.close()
                    print("PostgreSQL connection is closed")
        #print(df)
        model = DataFrameModel(df)
        #print(model)
        self.tableView.setModel(model)

class AdminWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Admin Page')
        vBox = QtWidgets.QVBoxLayout()
        self.cr8Employee_btn = QtWidgets.QPushButton('Create a new employee')
        self.cr8Employee_btn.clicked.connect(self.switch)
        vBox.addWidget(self.cr8Employee_btn)
        self.setupTable_btn = QtWidgets.QPushButton('Set up table')
        self.setupTable_btn.clicked.connect(self.switch)
        vBox.addWidget(self.setupTable_btn)
        self.grantAccess_btn = QtWidgets.QPushButton('Grant Access')
        self.grantAccess_btn.clicked.connect(self.switch)
        vBox.addWidget(self.grantAccess_btn)
        self.BusinessReport_btn = QtWidgets.QPushButton('Access and create the business report')
        self.BusinessReport_btn.clicked.connect(self.switch)
        vBox.addWidget(self.BusinessReport_btn)
        self.setLayout(vBox)

    def switch(self):
        self.switch_window.emit("TEST")
        
class Login(QtWidgets.QWidget):

    switch_SaleWindow = QtCore.pyqtSignal(psycopg2.extensions.connection)
    switch_AdminWindow = QtCore.pyqtSignal(str)
    switch_EngrWindow = QtCore.pyqtSignal(psycopg2.extensions.connection)
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')

        vBox = QtWidgets.QVBoxLayout()
        
        # Username
        self.username = QtWidgets.QLineEdit("John Doe")
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
                self.switch_AdminWindow.emit("Admin")
            elif 'sales' in role:
                self.switch_SaleWindow.emit(connection)    
            elif 'engineer' in role:
                self.switch_EngrWindow.emit(connection)    


class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_SaleWindow.connect(self.show_SaleWindow)
        self.login.switch_AdminWindow.connect(self.show_AdminWindow)
        self.login.switch_EngrWindow.connect(self.show_EngrWindow)
        self.login.show()

    def show_SaleWindow(self, connection):
        self.sale_Window = saleWindow(connection)
        #self.sale_Window.switch_salesReport.connect(self.show_window_salesReport)
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
        
    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        self.admin_Window.close()
        #self.sale_Window.close()
        self.window_two.show()
        self.window_two.setFixedSize(1080,720)
    
    def show_AdminWindow(self, text):
        self.admin_Window = AdminWindow(text)
        self.admin_Window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.admin_Window.show()
        self.admin_Window.setFixedSize(1080,720)
    
    def show_EngrWindow(self, connection):
        self.engr_Window = engrWindow(connection)
        self.engr_Window.switch_updateInv.connect(lambda: self.show_window_updateInv(connection))
        self.engr_Window.switch_updateModel.connect(lambda: self.show_window_updateModel(connection))
        self.engr_Window.switch_employeeView.connect(lambda: self.show_window_employeeView(connection))
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