import sys
from PyQt5 import QtCore, QtWidgets
import psycopg2
import pandas as pd

class saleWindow (QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Sales Page')
        vBox = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton('Query One')
        self.button.clicked.connect(self.switch)
        vBox.addWidget(self.button)

        self.setLayout(vBox)

    def switch(self):
        self.switch_window.emit("TEST")


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
        try:
            connection = psycopg2.connect(user = "postgres",
                                          password = "G8h8y8@@", #Your password in psql
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "test1")   #Your db name
            
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

    switch_SaleWindow = QtCore.pyqtSignal()
    switch_AdminWindow = QtCore.pyqtSignal(str)
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
        success=False
        try:
            connection = psycopg2.connect(user = "postgres",
                                          password = "G8h8y8@@", #Your password in psql
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "test1")   #Your db name
        
            cursor = connection.cursor()
            login_sql = """SELECT id 
                    from instructor
                    WHERE name = %s AND dept_name = %s AND
                    EXISTS (SELECT * FROM instructor WHERE name = %s AND dept_name = %s) 
                    """
        
            cursor.execute(login_sql, (username, pw, username, pw)) #Login in ID add password
            success = cursor.fetchone()[0]    
            connection.commit()    
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
        if(success):
            print("User Id and password found in database")
            a=[success]
            print(type(success), a)
            #Switch case for different type of user
            if '3' in success:
                self.switch_AdminWindow.emit("Admin")
            elif '1' in success:
                self.switch_SaleWindow.emit()    
        else:
            print('Error login')
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Incorrect ID or Password. The ID or password you entered is incorrect.")
            msg.setInformativeText('Please try again.')
            msg.setWindowTitle("Error Login")
            msg.exec_()

class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_SaleWindow.connect(self.show_SaleWindow)
        self.login.switch_AdminWindow.connect(self.show_AdminWindow)
        self.login.show()

    def show_SaleWindow(self):
        self.sale_Window = saleWindow()
        self.sale_Window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.sale_Window.show()
        self.sale_Window.setFixedSize(1080,720)

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
    
class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QtCore.QVariant()

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()