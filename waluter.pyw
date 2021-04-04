#importowane biblioteki
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QBoxLayout ,QApplication, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QDate
from datetime import datetime, timedelta
from json import *
from requests import get, exceptions
from sys import argv, exit
from ctypes import windll
class Program(QWidget):
#funckja łącząca się z api NBP i wpisująca w pole tekstowe rownowartość kwoty podanej przez użytkownika w euro po kursie z poprzedniego dnia roboczego w złotych
    def currency(self):
        def datesInteraction(date1):
            date1 = date1.toPyDate()
            date1 -= timedelta(days=15)
            year = str(date1.year)
            month = str(date1.month)
            day = str(date1.day)
            if int(month) < 10:
                month = '0' + month
            if int(day) < 10:
                day = '0' + day

            return year + '-' + month + '-' + day

        code = self.slider.currentText()
        table = 'A'
        try:
            callendarDate = self.callendar.selectedDate()
            year = callendarDate.year()
            month = callendarDate.month()
            day = callendarDate.day()
            moneyPremade = self.money.text()
            if float(moneyPremade.replace(',','.')) >= 0:
                money = float(moneyPremade.replace(',','.'))
            else:
                self.answer.setText('popraw wpisywaną kwotę')
                return -1
        except ValueError:
            self.answer.setText('0,0')
            return -1
        
        if day < 10:
            day = '0' + str(day)
        if month < 10:
            month = '0' + str(month)

        date = str(year) + '-' + str(month) + '-' + str(day)
        dateBeforeUltimate = datesInteraction(callendarDate)



        #pobranie jsona
        try:
            r = get('http://api.nbp.pl/api/exchangerates/rates/' + table + '/' + code + '/' + dateBeforeUltimate + '/' + date + '/?format=json')
            response = r.json()
            if response['rates'][-1]['effectiveDate'] != str(callendarDate.toPyDate()):
                course = response['rates'][-1]['mid']
                text = str(round(money*course, 2))
                text = text.replace('.', ',')
                self.answer.setText(text)
            else:
                course = response['rates'][-2]['mid']
                text = str(round(money*course, 2))
                text = text.replace('.', ',')
                self.answer.setText(text)
        except exceptions.ConnectionError:
            self.answer.setText('brak połączenia z internetem')
            
    def __init__(self, parent=None):
        super().__init__(parent)

        self.money = QLineEdit()
        self.money.setFont(QFont('Arial', 10))
        self.answer = QLineEdit()
        self.answer.setFont(QFont('Arial', 10))
#linie tekstowe        
        moneyLine = QLabel('kwota transakcji:', self)
        moneyLine.setFont(QFont('Arial', 10))
        answerLine = QLabel('kwota w PLN:', self)
        answerLine.setFont(QFont('Arial', 10))
#kalendarz
        now = datetime.now()
        self.callendar = QCalendarWidget()
        self.callendar.setMaximumDate(now)
        self.callendar.setGridVisible(True)
        self.callendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.callendar.setFont(QFont('Arial', 10))
        self.callendar.setCursor(Qt.PointingHandCursor)
#tło aplikacji
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)
        self.answer.setToolTip('Wpisz datę transakcji i wpisz kwotę')

#strona to tabela
        tabularLayout = QGridLayout()

        tabularLayout.addWidget(moneyLine, 3, 0)
        tabularLayout.addWidget(self.money, 3, 1)
        
        tabularLayout.addWidget(answerLine, 4, 0)
        tabularLayout.addWidget(self.answer, 4, 1)

        tabularLayout.addWidget(self.callendar, 2, 0, 1, 2)
#lista rozwijana
        self.slider = QComboBox()
        self.slider.setFont(QFont('Arial', 10))
        self.slider.addItem('EUR')
        self.slider.setItemIcon(0, QIcon('iconEUR.png'))
        self.slider.addItem('USD')
        self.slider.setItemIcon(1, QIcon('iconUSD.png'))
        self.slider.addItem('GBP')
        self.slider.setItemIcon(2, QIcon('iconGBP.png'))
        tabularLayout.addWidget(self.slider, 1, 0, 1, 2)

        self.setLayout(tabularLayout)
        self.setWindowIcon(QIcon('icon.png'))
        self.setMaximumHeight(400)
        self.setMaximumWidth(400)
        self.resize(400, 400)
        self.setWindowTitle("Waluter")
        self.show()

        self.money.textChanged.connect(self.currency)
        self.slider.textActivated.connect(self.currency)
        self.callendar.selectionChanged.connect(self.currency)
        self.adjustSize()


app = QApplication(argv)
myappid = 'mycompany.myproduct.subproduct.version'
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
okno = Program()
exit(app.exec_())

    