from PyQt5 import QtWidgets, QtGui, QtCore
from Ui_main import Ui_MainWindow
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QMessageBox
import sys
# issue1 tableWidget 點 header_column to sort
# issue2 刪除,修改功能  containeters 元件

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit_roy1.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_roy2.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_roy3.setValidator(QtGui.QDoubleValidator())
        
        self.ui.lineEdit_bookname.editingFinished.connect(lambda:contract.setbookname(self.ui.lineEdit_bookname.text()))
        self.ui.lineEdit_unit.editingFinished.connect(lambda:contract.setunit(self.ui.lineEdit_unit.text()))
        self.ui.lineEdit_area.editingFinished.connect(lambda:contract.setauthorizedarea(self.ui.lineEdit_area.text()))
        self.ui.lineEdit_agent.editingFinished.connect(lambda:contract.setagent(self.ui.lineEdit_agent.text()))
        self.ui.lineEdit_author.editingFinished.connect(lambda:contract.setauthor(self.ui.lineEdit_author.text()))
        self.ui.comboBox_interval.activated.connect(lambda:contract.setclacinterval(self.ui.comboBox_interval.currentIndex()))
        self.ui.dateEdit_startdate.dateChanged.connect(lambda:contract.setstartdate(self.ui.dateEdit_startdate.date().toString("yyyy-MM-dd")))
        self.ui.dateEdit_enddate.dateChanged.connect(lambda:contract.setenddate(self.ui.dateEdit_enddate.date().toString("yyyy-MM-dd")))
        self.ui.lineEdit_roy1.editingFinished.connect(lambda:contract.setroalty1(float(self.ui.lineEdit_roy1.text())))
        self.ui.lineEdit_roy2.editingFinished.connect(lambda:contract.setroalty2(float(self.ui.lineEdit_roy2.text())))
        self.ui.lineEdit_roy3.editingFinished.connect(lambda:contract.setroalty3(float(self.ui.lineEdit_roy3.text())))
        self.ui.lineEdit_roy4.editingFinished.connect(lambda:contract.setroalty4(self.ui.lineEdit_roy4.text()))
        
        self.ui.pushButton_insert.clicked.connect(lambda:contract.sql_insert())
        self.ui.pushButton_search.clicked.connect(self.loadData)
        #self.ui.pushButton_insert.clicked.connect(self.sorttable)

        #self.ui.tableWidget.horizontalHeader().sectionClicked.connect(your_callable)
        #self.ui.tableWidget.cellClicked(0,1).connect(lambda:print("{} {}".format(self.ui.tableWidget.currentRow(),self.ui.tableWidget.currentColumn())))
        #self.ui.tableWidget.horizontalHeaderItem.cellClicked().connect(self.sorttable)

    def loadData(self):
        sql_search = contract.makesql()
        sql = "SELECT * FROM `contract` WHERE `bookname` LIKE '{}' and `unit` LIKE '{}' and `authorized_area` LIKE  '{}'\
            and `agent` LIKE '{}' and `author` LIKE '{}' and `calc_interval` LIKE '{}' and `start_date` LIKE '{}'\
            and `end_date` LIKE '{}' and `royalty1` LIKE '{}' and `royalty2` LIKE '{}' and `royalty3` LIKE '{}' and `royalty4` LIKE '{}'"\
            .format(sql_search[0],sql_search[1],sql_search[2],sql_search[3],sql_search[4],sql_search[5],sql_search[6],sql_search[7],sql_search[8],sql_search[9],sql_search[10],sql_search[11])
        print(sql)
        data,col_title = sqlsearch(sql)
        if (data == False and col_title == False):
            return
        for i in range(len(data)):
            data[i] = data[i][1:]
        collist = []
        for i in range(1,len(col_title)):
             collist.append(col_title[i][0])
        self.ui.tableWidget.setHorizontalHeaderLabels(collist)
        self.ui.tableWidget.setColumnCount(len(collist))
        self.ui.tableWidget.setRowCount(0)

        for row in data:
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            for i,column in enumerate(row):     
                self.ui.tableWidget.setItem(rowPosition,i,QtWidgets.QTableWidgetItem(str(column)))
        self.ui.tableWidget.resizeColumnsToContents()

    def clearlineedit(self):
        self.ui.lineEdit_bookname.setText('')
        self.ui.lineEdit_unit.setText('')
        self.ui.lineEdit_area.setText('')
        self.ui.lineEdit_agent.setText('')
        self.ui.lineEdit_author.setText('')
        self.ui.comboBox_interval.setCurrentIndex(0)
        self.ui.dateEdit_startdate.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit_enddate.setDate(QtCore.QDate.currentDate())
        self.ui.lineEdit_roy1.setText('')
        self.ui.lineEdit_roy2.setText('')
        self.ui.lineEdit_roy3.setText('')
        self.ui.lineEdit_roy4.setText('')
    
    def sorttable(self):
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.sortByColumn(0,QtCore.Qt.AscendingOrder)
        
def sqlsearch(sql):
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='royalty_db', # 資料庫名稱
            user='root',        # 帳號
            password='')  # 密碼

        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        col_title = cursor.description
        cursor.close()
        connection.close()
        return data,col_title
    except Error as e:
        QMessageBox.critical(window, '資料庫連接失敗：', str(e))
        return False,False
        
            
            
class ccontract():
    def __init__(self):
        self.bookname = ''
        self.unit = ''
        self.authorizedarea = ''
        self.agent = ''
        self.author = ''
        self.clacinterval = 0
        self.startdate = ''
        self.enddate = ''
        self.roalty1 = 0.0
        self.roalty2 = 0.0
        self.roalty3 = 0.0
        self.roalty4 = ''
        self.tr_dict = {'bookname': '簽約書名', 'unit': '簽約單位','authorizedarea':'授權地區','agent':'代理商',
                    'author':'作者','clacinterval':'結算期限','startdate':'合約開始日期','enddate':'合約結束日期',
                    'roalty1':'版稅稅率(1~5000)','roalty2':'版稅稅率(5001~10000)','roalty3':'版稅稅率(10001以上)','roalty4':'版稅稅率(自訂)'}

    def initvariable(self):
        self.bookname = ''
        self.unit = ''
        self.authorizedarea = ''
        self.agent = ''
        self.author = ''
        self.clacinterval = 0
        self.startdate = ''
        self.enddate = ''
        self.roalty1 = 0.0
        self.roalty2 = 0.0
        self.roalty3 = 0.0
        self.roalty4 = ''

    def makesql(self):
        sql = []
        if(self.bookname != ''):
            sql.append(self.bookname)
        else:
            sql.append('%')
        if(self.unit != ''):
            sql.append(self.unit)
        else:
            sql.append('%')
        if(self.authorizedarea != ''):
            sql.append(self.authorizedarea)
        else:
            sql.append('%')
        if(self.agent != ''):
            sql.append(self.agent)
        else:
            sql.append('%')
        if(self.author != ''):
            sql.append(self.author)
        else:
            sql.append('%')
        if(self.clacinterval != 0):
            sql.append(self.clacinterval)
        else:
            sql.append('%')
        if(self.startdate != ''):
            sql.append(self.startdate)
        else:
            sql.append('%')
        if(self.enddate != ''):
            sql.append(self.enddate)
        else:
            sql.append('%')
        if(self.roalty1 != 0.0):
            sql.append(self.roalty1)
        else:
            sql.append('%')
        if(self.roalty2 != 0.0):
            sql.append(self.roalty2)
        else:
            sql.append('%')
        if(self.roalty3 != 0.0):
            sql.append(self.roalty3)
        else:
            sql.append('%')
        if(self.roalty4 != ''):
            sql.append(self.roalty4)
        else:
            sql.append('%')
        return sql
    
    def setbookname(self,text):
        self.bookname = text
    def setunit(self,text):
        self.unit = text
    def setauthorizedarea(self,text):
        self.authorizedarea = text     
    def setagent(self,text):
        self.agent = text
    def setauthor(self,text):
        self.author = text
    def setclacinterval(self,number):
        self.clacinterval = number
    def setstartdate(self,date):
        self.startdate = date
    def setenddate(self,date):
        self.enddate = date
    def setroalty1(self,number):
        self.roalty1 = number
    def setroalty2(self,number):
        self.roalty2 = number
    def setroalty3(self,number):
        self.roalty3 = number
    def setroalty4(self,text):
        self.roalty4 = text

    def sql_insert(self):
        error = ''
        error += self.checknull('bookname',self.bookname)
        error += self.checknull('unit',self.unit)
        error += self.checknull('authorizedarea',self.authorizedarea)
        error += self.checknull('agent',self.agent)
        error += self.checknull('author',self.author)
        error += self.checkfloatnull('roalty1',self.roalty1)
        error += self.checkfloatnull('roalty2',self.roalty2)
        error += self.checkfloatnull('roalty3',self.roalty3)
        if(error == ''):
            sql = 'INSERT INTO `contract`(`bookname`,`unit`,`authorized_area`,`agent`,`author`,`calc_interval`,`start_date`,`end_date`,`royalty1`,`royalty2`,`royalty3`,`royalty4`) \
                   VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            data = (contract.bookname,contract.unit,contract.authorizedarea,contract.agent,contract.author,contract.clacinterval,contract.startdate,contract.enddate,contract.roalty1,contract.roalty2,contract.roalty3,contract.roalty4)
                   
            try:
                # 連接 MySQL/MariaDB 資料庫
                connection = mysql.connector.connect(
                host='localhost',          # 主機名稱
                database='royalty_db', # 資料庫名稱
                user='root',        # 帳號
                password='')  # 密碼
                cursor = connection.cursor()
                cursor.execute(sql,data)
                connection.commit()
                connection.close()
                cursor.close()
                QMessageBox.information(window, '新增成功', '新增成功')
                window.loadData()
                self.initvariable()
                window.clearlineedit()

            except Error as e:
                QMessageBox.critical(window, '資料庫連接失敗：', str(e))

        else:
            QMessageBox.critical(window, '錯誤', error)
        
    def checknull(self,id,intext):
        if intext == '':
            return ('"{}"  不能是空白的\n'.format(self.tr_dict[id]))
        return ''
        
    def checkfloatnull(self,id,intext):
        if intext == 0:
            return('"{}"  不能是空白的\n'.format(self.tr_dict[id]))
        return ''

if __name__ == '__main__':
    contract = ccontract()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.loadData()
    sys.exit(app.exec_())