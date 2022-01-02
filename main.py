import sys
import webbrowser
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

        # 레이블 설정
        titleLable = QLabel('Title:')
        dateLabel = QLabel('Date:')
        noteLable = QLabel('Note:')

        # 텍스트 공간 설정
        title = QLineEdit()
        date = QDateEdit(self)
        note = QTextEdit()

        # 텍스트 공간 - 날짜
        date.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        date.setCalendarPopup(True)
        date.setDate(QDate.currentDate())

        # 그리드 레이아웃에 레이블과 텍스트 공간 추가
        grid.addWidget(titleLable, 0, 0)
        grid.addWidget(dateLabel, 1, 0)
        grid.addWidget(noteLable, 2, 0)

        grid.addWidget(title, 0, 1)
        grid.addWidget(date, 1, 1)
        grid.addWidget(note, 2, 1)

        # 폰트 세부 설정
        font_init = title.font()
        font_init.setPointSize(13)
        font_init.setFamilies(['Times New Roman', 'Malgun Gothic'])

        # 폰트 적용
        title.setFont(font_init)
        date.setFont(font_init)
        note.setFont(font_init)
        titleLable.setFont(font_init)
        dateLabel.setFont(font_init)
        noteLable.setFont(font_init)

        title.setStyleSheet("background-color:#A7DEFD;"
                            "padding:3px")
        date.setStyleSheet("background-color:#A7FDD4;"
                            "padding:3px")
        note.setStyleSheet("background-color:#FEFFEB;"
                            "padding:3px")

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate() # 현재 날짜 지정
        self.initUI() # 상속으로 넘김

    def initUI(self):
        wg = Memo()
        self.setCentralWidget(wg) # Memo 위젯을 centralWidget으로 설정
        
        # Action 모음 #
        openAction = QAction(QIcon("icon/share.png"), 'Open', self) # 파일 열기
        saveAction = QAction(QIcon("icon/save.png"), 'Save', self) # 파일 저장
        printAction = QAction(QIcon("icon/print.png"), 'Print', self) # 파일 인쇄(사진으로)
        fontAction = QAction(QIcon("icon/font-size.png"), 'Font', self) # 폰트 설정
        exitAction = QAction(QIcon("icon/logout.png"), 'Exit', self) # 나가기
        titleColor = QAction(QIcon("icon/title.png"), 'Title', self) # 타이틀 배경색 설정
        dateColor = QAction(QIcon("icon/calendar.png"), 'Date', self) # 날짜 배경색 설정
        noteColor = QAction(QIcon("icon/note.png"), 'Note', self) # 노트 배경색 설정
        helpAction = QAction(QIcon("icon/link.png"), 'Help', self) # 도움말

        # 파일 열기 설정
        openAction.setShortcut('Ctrl+O')
        openAction.setToolTip('Open')
        openAction.setStatusTip('Open Memo Text')
        openAction.triggered.connect(self.open_memo)

        # 파일 저장 설정
        saveAction.setShortcut('Ctrl+S')
        saveAction.setToolTip('Save')
        saveAction.setStatusTip('Save Memo Text')
        saveAction.triggered.connect(self.save_memo)
        
        # 파일 인쇄 설정
        printAction.setShortcut('Alt+P')
        printAction.setToolTip('Print')
        printAction.setStatusTip('Print Memo')
        printAction.triggered.connect(self.print_memo)

        # 폰트 설정
        fontAction.setShortcut('Ctrl+F')
        fontAction.setToolTip('Font')
        fontAction.setStatusTip('Setting Font')
        fontAction.triggered.connect(self.show_font_dialog)

        # 색 설정
        titleColor.setToolTip('Title')
        dateColor.setToolTip('Date')
        noteColor.setToolTip('Note')

        titleColor.setStatusTip('Setting Title Background Color')
        dateColor.setStatusTip('Setting Date Background Color')
        noteColor.setStatusTip('Setting Note Background Color')

        titleColor.triggered.connect(self.show_title_color_dialog)
        dateColor.triggered.connect(self.show_date_color_dialog)
        noteColor.triggered.connect(self.show_note_color_dialog)

        # 나가기 설정
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setToolTip('Exit')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        # 도움말 설정
        helpAction.setShortcut('Ctrl+H')
        helpAction.setToolTip('Help')
        helpAction.setStatusTip('Help')
        helpAction.triggered.connect(lambda: webbrowser.open("https://github.com/SeHaan/program_researchNote"))

        # 상태바 만들기
        self.statusBar()

        # 메뉴 바 #
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        editmenu = menubar.addMenu('&Edit')
        helpmenu = menubar.addMenu('&Help')
        colormenu = QMenu('&Color', self)

        filemenu.addAction(openAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(printAction)
        filemenu.addAction(exitAction)
        
        editmenu.addAction(fontAction)
        editmenu.addMenu(colormenu) # 서브메뉴화
        colormenu.addAction(titleColor)
        colormenu.addAction(dateColor)
        colormenu.addAction(noteColor)

        helpmenu.addAction(helpAction)

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

    # 프로그램을 열 때 화면 가운데에 오도록 하는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 슬롯: 파일 열기
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
                
    # 슬롯: 파일 닫기
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
            f.write("\n======================")
            f.close()

    # 슬롯: 인쇄
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

    # 슬롯: 폰트 다이얼로그
    def show_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.centralWidget().children()[6].setFont(font)

    # 슬롯: 타이틀 컬러 다이얼로그
    def show_title_color_dialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            element = self.centralWidget().children()[5]
            element.setStyleSheet("padding:3px;"
                                    "background-color: %s;" %col.name())

    # 슬롯: 날짜 컬러 다이얼로그
    def show_date_color_dialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            element = self.centralWidget().children()[1]
            element.setStyleSheet("padding:3px;"
                                    "background-color: %s;" %col.name())

    # 슬롯: 노트 컬러 다이얼로그
    def show_note_color_dialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            element = self.centralWidget().children()[6]
            element.setStyleSheet("padding:3px;"
                                    "background-color: %s;" %col.name())

    # 경고창
    def messageBox():
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Warning")
        msgBox.setWindowIcon(QIcon("icon/icons8-note-100.png"))
        msgBox.setText("Warning")
        msgBox.setInformativeText("Invalid Format Text!\nYou cannot open this file in the app.")
        msgBox.setStandardButtons(QMessageBox.Yes)


## 메인 ##
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())