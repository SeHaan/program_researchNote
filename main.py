import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

class Memo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  
        grid = QGridLayout()
        self.setLayout(grid)

        titleLable = QLabel('Title:')
        dateLabel = QLabel('Date:')
        noteLable = QLabel('Note:')

        title = QLineEdit()
        date = QDateEdit(self)
        note = QTextEdit()

        date.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        date.setCalendarPopup(True)
        date.setDate(QDate.currentDate())

        grid.addWidget(titleLable, 0, 0)
        grid.addWidget(dateLabel, 1, 0)
        grid.addWidget(noteLable, 2, 0)

        grid.addWidget(title, 0, 1)
        grid.addWidget(date, 1, 1)
        grid.addWidget(note, 2, 1)

        font_init = note.font()
        font_init.setPointSize(11)
        font_init.setFamily('Times New Roman')

        title.setFont(font_init)
        date.setFont(font_init)
        note.setFont(font_init)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        wg = Memo()
        self.setCentralWidget(wg)

        """for i in range(len(self.centralWidget().children())):
            print(self.centralWidget().children()[i], end="\n")"""
        
        # Action 모음 #
        openAction = QAction(QIcon("icon/share.png"), 'Open', self)
        saveAction = QAction(QIcon("icon/save.png"), 'Save', self)
        printAction = QAction(QIcon("icon/print.png"), 'Print', self)
        fontAction = QAction(QIcon("icon/font-size.png"), 'Font', self)
        exitAction = QAction(QIcon("icon/logout.png"), 'Exit', self)

        openAction.setShortcut('Ctrl+O')
        openAction.setToolTip('Open Memo Text')
        openAction.triggered.connect(self.open_memo)

        saveAction.setShortcut('Ctrl+S')
        saveAction.setToolTip('Save Memo Text')
        saveAction.triggered.connect(self.save_memo)
        
        printAction.setShortcut('Alt+P')
        printAction.setStatusTip('Print Memo')
        printAction.triggered.connect(self.print_memo)

        fontAction.setShortcut('Ctrl+F')
        fontAction.setToolTip('Setting Font')
        fontAction.triggered.connect(self.show_font_dialog)

        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        # 메뉴 바 #
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        editmenu = menubar.addMenu('&Edit')

        filemenu.addAction(openAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(printAction)
        filemenu.addAction(exitAction)
        
        editmenu.addAction(fontAction)

        # 툴 바 #
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(exitAction)

        # 윈도우 #
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))
        self.setWindowTitle("Research Note for Minami")
        self.setWindowIcon(QIcon("icon/icons8-note-100.png"))
        self.resize(800, 800)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_memo(self):
        openfile = QFileDialog.getOpenFileName(self, 'Open File', './')
        print(openfile)
        if openfile[0] != '':
            f = open(openfile[0], 'r', encoding='utf-8')

            title = self.centralWidget().children()[5]
            dateE = self.centralWidget().children()[1]
            content = self.centralWidget().children()[6]

            content_all = []
            content_text = ''

            while True:
                line = f.readline()
                if not line: break
                content_all.append(line)
            f.close()

            if content_all[0] == "======================\n":
                year = int(content_all[3].split("-")[0])
                month = int(content_all[3].split("-")[1])
                day = int(content_all[3].split("-")[2])
                
                date_text = QtCore.QDate(year, month, day)

                for i in range(5, len(content_all)-1):
                    content_text = content_text + content_all[i]

                title.setText(content_all[1][:len(content_all[1])-1])
                dateE.setDate(date_text)
                content.setText(content_text)
            else:
                msgBox = QMessageBox.critical(self, "Warning", "Invalid Format Text!\nYou cannot open this file in the app.")
                

    def save_memo(self):
        year = str(self.centralWidget().children()[1].date().year())
        month = str(self.centralWidget().children()[1].date().month())
        day = str(self.centralWidget().children()[1].date().day())

        titleText = self.centralWidget().children()[5].text()
        dateText = year + "-" + month + "-" + day + "\n"
        content = self.centralWidget().children()[6].toPlainText()

        saveFile = QFileDialog.getSaveFileName(self, 'Save File', titleText+'.txt')

        if saveFile[0] != '':
            f = open(saveFile[0], 'w', encoding='utf-8')
            f.write("======================\n")
            f.write(titleText)
            f.write("\n----------------------\n")
            f.write(dateText)
            f.write("----------------------\n")
            f.write(content)
            f.write("\n======================\n")
            f.close()

    def print_memo(self):
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QDialog.Accepted:
            # Painter 생성
            qp = QPainter()
            qp.begin(printer)
            screen = self.centralWidget().grab()
            qp.drawPixmap(20, 20, screen)
            qp.end()

    def show_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.centralWidget().children()[6].setFont(font)

    def messageBox():
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Warning")
        msgBox.setWindowIcon(QIcon("icon/icons8-note-100.png"))
        msgBox.setText("Warning")
        msgBox.setInformativeText("Invalid Format Text!\nYou cannot open this file in the app.")
        msgBox.setStandardButtons(QMessageBox.Yes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())