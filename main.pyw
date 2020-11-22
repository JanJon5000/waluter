#importowane biblioteki
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QBoxLayout ,QApplication, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import datetime
import json
import requests
class Program(QWidget):
#funckja łącząca się z api NBP i wpisująca w pole tekstowe rownowartość kwoty podanej przez użytkownika w euro po kursie z poprzedniego dnia roboczego w złotych
    def currency(self):
        def datesInteraction(date1):
            year = int(date1[0:4])
            month = int(date1[5:6])
            day = int(date1[8:9])
            if day - 10 <=0 :
                day = 20
                if month - 1 <=0:
                    month = 12
                    year -=1
                else:
                    month -= 1
            return str(year) + '-' + str(month) + '-' + str(day)

        code = self.slider.currentText()
        table = 'A'
        try:
            date = self.callendar.selectedDate()
            year = date.year()
            month = date.month()
            day = date.day()
            moneyPremade = self.money.text()
            if float(moneyPremade.replace(',','.')) >= 0:
                money = float(moneyPremade.replace(',','.'))
            else:
                self.answer.setText('popraw wpisywaną kwotę')
                return -1
        except ValueError:
            self.answer.setText('coś poszło nie tak')
            return -1
        
        if day < 10:
            day = '0' + str(day)
            if month < 10:
                month = '0' + str(month)

        date = str(year) + '-' + str(month) + '-' + str(day)
        dateBeforeUltimate = datesInteraction(date)
        r = requests.get('http://api.nbp.pl/api/exchangerates/rates/' + table + '/' + code + '/' + dateBeforeUltimate + '/' + date + '/?format=json')

        try:
            response = r.json()
            if response['rates'][-1]['effectiveDate'] != date:
                course = response['rates'][-1]['mid']
            else:
                course = response['rates'][-2]['mid']
            text = str(round(money*course, 2))
            text = text.replace('.', ',')
            self.answer.setText(text)
        except ValueError:
            self.answer.setText('coś poszło nie tak')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.month = QLineEdit()
        self.day = QLineEdit()
        self.year = QLineEdit()
        self.money = QLineEdit()
        self.answer = QLineEdit()
#linie tekstowe        
        moneyLine = QLabel('kwota transakcji:', self)
        moneyLine.setFont(QFont('Arial', 10))
        answerLine = QLabel('kwota w PLN:', self)
        answerLine.setFont(QFont('Arial', 10))
#kalendarz
        now = datetime.datetime.now()
        self.callendar = QCalendarWidget()
        self.callendar.setMaximumDate(now)
        self.callendar.setGridVisible(True)
        self.callendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.callendar.setFont(QFont('Arial', 10))
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
#przycisk
        button = QPushButton("OBLICZ", self)
        tabularLayout.addWidget(button, 5, 0, 1, 2)
        button.setFont(QFont('Arial', 10))
        self.setLayout(tabularLayout)
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(20, 20, 300, 100)
        self.resize(300, 300)
        self.setFixedSize(400, 400)
        self.setWindowTitle("Waluter")
        self.show()
        button.clicked.connect(self.currency)    


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    okno = Program()
    sys.exit(app.exec_())