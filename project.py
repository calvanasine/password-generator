from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

import string
import secrets

class PasswordGenerator:
    def __init__(self):
        # string 모듈에서 제공하는 문자열을 참조하고 리스트로 변환
        self.upperLetters = list(string.ascii_uppercase)
        self.lowerLetters = list(string.ascii_lowercase)
        self.digits = list(string.digits)
        self.symbols = list(string.punctuation)

        # 문자 포함 여부
        self.bUpperLetters = True
        self.bLowerLetters = True
        self.bDigits = True
        self.bSymbols = True

        # 포함할 문자의 길이
        self.lenPW = 8
        self.lenUpperLetters = 1
        self.lenLowerLetters = 1
        self.lenDigits = 1
        self.lenSymbols = 1

        # 입력 문자 제외 또는 포함
        self.lst = ''
        self.lstHowTo = 0
        self.splitString = ','

    def cut(self):
        # 초기화
        self.upperLetters = list(string.ascii_uppercase)
        self.lowerLetters = list(string.ascii_lowercase)
        self.digits = list(string.digits)
        self.symbols = list(string.punctuation)

        # 문자열을 구분자로 구분해 리스트로 변환
        self.lst = self.lst.split(self.splitString)

        # 문자열을 입력하면 예외 발생
        for i in range(len(self.lst)):
            if len(self.lst[i]) > 1:
                raise Exception('errorNotChar')

    def exclude(self):
        self.cut()

        # 문자 포함 여부를 확인해 해당 리스트에서 입력된 문자 제거
        # 해당하는 값이 없을 때 예외가 발생하면 현재 반복 건너뛰기
        if self.bUpperLetters == True:
            for item in self.lst:
                try:
                    self.upperLetters.remove(item)
                except ValueError:
                    continue
        if self.bLowerLetters == True:
            for item in self.lst:
                try:
                    self.lowerLetters.remove(item)
                except ValueError:
                    continue
        if self.bDigits == True:
            for item in self.lst:
                try:
                    self.digits.remove(item)
                except ValueError:
                    continue
        if self.bSymbols == True:
            for item in self.lst:
                try:
                    self.symbols.remove(item)
                except ValueError:
                    continue

    # 문자를 포함한다고 했음에도 모든 문자를 제외할 수 있으므로 리스트 길이 확인
    def bZeroList(self):
        if (len(self.upperLetters) < self.lenUpperLetters
                or len(self.lowerLetters) < self.lenLowerLetters
                or len(self.digits) < self.lenDigits
                or len(self.symbols) < self.lenSymbols):
            return True

    # 비밀번호 생성
    def generator(self):
        password = ''
        passwordTemp = ''
        passwordList = list()

        # 구분자가 없으면 예외 발생
        if self.splitString == '':
            raise Exception('errorZeroSplit')

        if self.lstHowTo == 0:
            self.exclude()
        elif self.lstHowTo == 1:
            self.cut()
            for i in self.lst:
                passwordList.append(i)

        # 문자 포함 여부를 확인하고 최소 길이만큼 무작위로 문자 생성
        if self.bUpperLetters == True:
            for i in range(self.lenUpperLetters):
                passwordList.append(secrets.choice(self.upperLetters))
        if self.bLowerLetters == True:
            for i in range(self.lenLowerLetters):
                passwordList.append(secrets.choice(self.lowerLetters))
        if self.bDigits == True:
            for i in range(self.lenDigits):
                passwordList.append(secrets.choice(self.digits))
        if self.bSymbols == True:
            for i in range(self.lenSymbols):
                passwordList.append(secrets.choice(self.symbols))

        # 생성한 문자열의 길이가 비밀번호 길이 이하인지 확인
        for i in range(len(passwordList)):
            passwordTemp += passwordList[i]

        # 이상이면 예외 발생
        if (self.lenPW - len(passwordTemp)) < 0:
            raise Exception('errorOutOfLength')

        # 변수 제거
        del passwordTemp
        
        # 포함 여부를 확인하고 새로운 리스트 생성
        character = list()
        if self.bUpperLetters == True:
            character += self.upperLetters
        if self.bLowerLetters == True:
            character += self.lowerLetters
        if self.bDigits == True:
            character += self.digits
        if self.bSymbols == True:
            character += self.symbols

        # 비밀번호 길이를 맞추기 위해 새로운 문자열에서 무작위로 문자 생성
        for i in range(self.lenPW - len(passwordList)):
            passwordList.append(secrets.choice(character))

        # 생성한 문자들을 섞음
        secrets.SystemRandom().shuffle(passwordList)

        # 리스트이므로 문자열로 변경
        for i in range(len(passwordList)):
            password += passwordList[i]

        return password

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.pg = PasswordGenerator()
        self.setupUI()

    def generatePushButton_clicked(self, e):
        try:
            # 문자 포함 여부 확인
            self.pg.bUpperLetters = self.bUpperLetterCheckBox.isChecked()
            self.pg.bLowerLetters = self.bLowerLetterCheckBox.isChecked()
            self.pg.bDigits = self.bDigitsCheckBox.isChecked()
            self.pg.bSymbols = self.bSymbolsCheckBox.isChecked()

            # 비밀번호 길이
            self.pg.lenPW = int(self.lengthSpinBox.text())

            # 문자 최소 길이
            if self.pg.bUpperLetters == True:
                self.pg.lenUpperLetters = int(self.lenUpperLetterSpinBox.text())
            else:
                self.pg.lenUpperLetters = 0
            if self.pg.bLowerLetters == True:
                self.pg.lenLowerLetters = int(self.lenLowerLetterSpinBox.text())
            else:
                self.pg.lenLowerLetters = 0
            if self.pg.bDigits == True:
                self.pg.lenDigits = int(self.lenDigitsSpinBox.text())
            else:
                self.pg.lenDigits = 0
            if self.pg.bSymbols == True:
                self.pg.lenSymbols = int(self.lenSymbolsSpinBox.text())
            else:
                self.pg.lenSymbols = 0

            # 문자 제거, 포함
            self.pg.lst = self.lstLineEdit.text()
            self.pg.lstHowTo = self.lstHowToComboBox.currentIndex()
            self.pg.splitString = self.splitListLineEdit.text()

            # 비밀번호 생성
            password = self.pg.generator()

            # 비밀번호 출력
            self.showPasswordLineEdit.setText(password)
            self.showPasswordLineEdit.setFocus()
            self.showPasswordLineEdit.selectAll()
        # 예외가 발생하면 경고창 출력
        except IndexError:
            self.e = 'errorIndexError'
            self.error()
        except Exception as e:
            self.e = str(e)
            self.error()
       
    def setupUI(self):
        # 글꼴
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        self.setFont(font)

        # 부모 윈도우
        self.setWindowTitle('Random Password Generator')
        self.setFixedSize(480, 870)

        # 생성 비밀번호 표시
        self.showPasswordLineEdit = QtWidgets.QLineEdit(self)
        self.showPasswordLineEdit.setGeometry(40, 20, 400, 50)
        font.setPointSize(12)
        self.showPasswordLineEdit.setFont(font)
        self.showPasswordLineEdit.setAlignment(Qt.AlignCenter)
        self.showPasswordLineEdit.setReadOnly(True)
        self.showPasswordLineEdit.setPlaceholderText("이곳에 비밀번호가 표시됩니다.")
        self.showPasswordLineEdit.setToolTip("\'비밀번호 생성하기\' 버튼을 눌러 비밀번호를 생성할 수 있습니다.")

        # 비밀번호 길이 설정
        self.lengthLabel = QtWidgets.QLabel(self)
        self.lengthLabel.setGeometry(40, 110, 40, 35)
        font.setPointSize(10)
        font.setBold(True)
        self.lengthLabel.setFont(font)
        self.lengthLabel.setText("길이")
        self.lengthSpinBox = QtWidgets.QSpinBox(self)
        self.lengthSpinBox.setGeometry(280, 110, 160, 35)
        font.setBold(False)
        self.lengthSpinBox.setFont(font)
        self.lengthSpinBox.setMinimum(1)
        self.lengthSpinBox.setMaximum(256)
        self.lengthSpinBox.setProperty("value", 8)
        self.lengthSpinBox.setToolTip("비밀번호 길이를 정합니다. (1~256)")

        # 문자 포함 여부
        self.incLabel = QtWidgets.QLabel(self)
        self.incLabel.setGeometry(40, 220, 41, 35)
        font.setBold(True)
        self.incLabel.setFont(font)
        self.incLabel.setText("포함")

        # 수직 정렬
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(280, 160, 160, 160)
        self.incVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.incVerticalLayout.setContentsMargins(0, 0, 0, 0)

        # 대문자 포함 여부
        self.bUpperLetterCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.bUpperLetterCheckBox.setChecked(True)
        font.setBold(False)
        self.bUpperLetterCheckBox.setFont(font)
        self.bUpperLetterCheckBox.setText("대문자 포함")
        self.bUpperLetterCheckBox.setToolTip("체크하면 비밀번호에 대문자를 포함합니다.")
        self.incVerticalLayout.addWidget(self.bUpperLetterCheckBox)
        self.bUpperLetterCheckBox.toggled.connect(self.bCheckBox_toggled)

        # 소문자 포함 여부
        self.bLowerLetterCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.bLowerLetterCheckBox.setChecked(True)
        font.setBold(False)
        self.bLowerLetterCheckBox.setFont(font)
        self.bLowerLetterCheckBox.setText("소문자 포함")
        self.bLowerLetterCheckBox.setToolTip("체크하면 비밀번호에 소문자를 포함합니다.")
        self.incVerticalLayout.addWidget(self.bLowerLetterCheckBox)
        self.bLowerLetterCheckBox.toggled.connect(self.bCheckBox_toggled)

        # 숫자 포함 여부
        self.bDigitsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.bDigitsCheckBox.setChecked(True)
        font.setBold(False)
        self.bDigitsCheckBox.setFont(font)
        self.bDigitsCheckBox.setText("숫자 포함")
        self.bDigitsCheckBox.setToolTip("체크하면 비밀번호에 숫자를 포함합니다.")
        self.incVerticalLayout.addWidget(self.bDigitsCheckBox)
        self.bDigitsCheckBox.toggled.connect(self.bCheckBox_toggled)

        # 특수문자 포함 여부
        self.bSymbolsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.bSymbolsCheckBox.setChecked(True)
        font.setBold(False)
        self.bSymbolsCheckBox.setFont(font)
        self.bSymbolsCheckBox.setText("특수문자 포함")
        self.bSymbolsCheckBox.setToolTip("체크하면 비밀번호에 특수문자를 포함합니다.")
        self.incVerticalLayout.addWidget(self.bSymbolsCheckBox)
        self.bSymbolsCheckBox.toggled.connect(self.bCheckBox_toggled)

        # 최소 길이 설정
        self.minLengthGroupBox = QtWidgets.QGroupBox(self)
        self.minLengthGroupBox.setGeometry(30, 340, 420, 240)
        font.setBold(True)
        self.minLengthGroupBox.setFont(font)
        self.minLengthGroupBox.setTitle("최소 길이 설정")

        # 대문자 최소 길이
        self.lenUpperLetterLabel = QtWidgets.QLabel(self.minLengthGroupBox)
        self.lenUpperLetterLabel.setGeometry(10, 40, 60, 35)
        font.setBold(True)
        self.lenUpperLetterLabel.setFont(font)
        self.lenUpperLetterLabel.setText("대문자")

        self.lenUpperLetterSpinBox = QtWidgets.QSpinBox(self.minLengthGroupBox)
        self.lenUpperLetterSpinBox.setGeometry(250, 40, 160, 35)
        font.setBold(False)
        self.lenUpperLetterSpinBox.setFont(font)
        self.lenUpperLetterSpinBox.setMinimum(1)
        self.lenUpperLetterSpinBox.setMaximum(64)
        self.lenUpperLetterSpinBox.setProperty("value", 1)
        self.lenUpperLetterSpinBox.setToolTip("비밀번호에 대문자가 최소 몇 자 있어야 하는지 정합니다. (1~64)")
        
        # 소문자 최소 길이
        self.lenLowerLetterLabel = QtWidgets.QLabel(self.minLengthGroupBox)
        self.lenLowerLetterLabel.setGeometry(10, 90, 60, 35)
        font.setBold(True)
        self.lenLowerLetterLabel.setFont(font)
        self.lenLowerLetterLabel.setText("소문자")
        self.lenLowerLetterSpinBox = QtWidgets.QSpinBox(self.minLengthGroupBox)
        self.lenLowerLetterSpinBox.setGeometry(250, 90, 160, 35)
        font.setBold(False)
        self.lenLowerLetterSpinBox.setFont(font)
        self.lenLowerLetterSpinBox.setMinimum(1)
        self.lenLowerLetterSpinBox.setMaximum(64)
        self.lenLowerLetterSpinBox.setProperty("value", 1)
        self.lenLowerLetterSpinBox.setToolTip("비밀번호에 소문자가 최소 몇 자 있어야 하는지 정합니다. (1~64)")

        # 숫자 최소 길이
        self.lenDigitsLabel = QtWidgets.QLabel(self.minLengthGroupBox)
        self.lenDigitsLabel.setGeometry(10, 140, 70, 35)
        font.setBold(True)
        self.lenDigitsLabel.setFont(font)
        self.lenDigitsLabel.setText("숫자")
        self.lenDigitsSpinBox = QtWidgets.QSpinBox(self.minLengthGroupBox)
        self.lenDigitsSpinBox.setGeometry(250, 140, 160, 35)
        font.setBold(False)
        self.lenDigitsSpinBox.setFont(font)
        self.lenDigitsSpinBox.setMinimum(1)
        self.lenDigitsSpinBox.setProperty("value", 1)
        self.lenDigitsSpinBox.setMaximum(64)
        self.lenDigitsSpinBox.setToolTip("비밀번호에 숫자가 최소 몇 자 있어야 하는지 정합니다. (1~64)")

        # 특수문자 최소 길이
        self.lenSymbolsLabel = QtWidgets.QLabel(self.minLengthGroupBox)
        self.lenSymbolsLabel.setGeometry(10, 190, 80, 35)
        font.setBold(True)
        self.lenSymbolsLabel.setFont(font)
        self.lenSymbolsLabel.setText("특수문자")
        self.lenSymbolsSpinBox = QtWidgets.QSpinBox(self.minLengthGroupBox)
        self.lenSymbolsSpinBox.setGeometry(250, 190, 160, 35)
        font.setBold(False)
        self.lenSymbolsSpinBox.setFont(font)
        self.lenSymbolsSpinBox.setMinimum(1)
        self.lenSymbolsSpinBox.setProperty("value", 1)
        self.lenSymbolsSpinBox.setMaximum(64)
        self.lenSymbolsSpinBox.setToolTip("비밀번호에 특수문자가 최소 몇 자 있어야 하는지 정합니다. (1~64)")

        # 문자 입력
        self.lstLineEdit = QtWidgets.QLineEdit(self)
        self.lstLineEdit.setGeometry(40, 610, 400, 40)
        font.setBold(False)
        self.lstLineEdit.setFont(font)
        
        # 입력한 문자 처리
        self.lstHowToLabel = QtWidgets.QLabel(self)
        self.lstHowToLabel.setGeometry(40, 660, 131, 35)
        font.setBold(True)
        self.lstHowToLabel.setFont(font)
        self.lstHowToLabel.setText("입력한 문자를")
        self.lstHowToComboBox = QtWidgets.QComboBox(self)
        self.lstHowToComboBox.setGeometry(359, 660, 80, 30)
        font.setBold(True)
        self.lstHowToComboBox.setFont(font)
        self.lstHowToComboBox.addItem("제외")
        self.lstHowToComboBox.addItem("포함")
        self.lstHowToComboBox.setToolTip("입력한 문자를 제외할지, 포함할지 정합니다.")

        # 입력한 문자 구분
        self.splitListLabel = QtWidgets.QLabel(self)
        self.splitListLabel.setGeometry(40, 710, 140, 35)
        font.setBold(True)
        self.splitListLabel.setFont(font)
        self.splitListLabel.setText("문자 구분 방법")
        self.splitListLineEdit = QtWidgets.QLineEdit(self)
        self.splitListLineEdit.setGeometry(360, 710, 80, 30)
        self.splitListLineEdit.setText(",")
        self.splitListLineEdit.setToolTip("위에서 입력한 문자를 여기에 입력한 문자를 기준으로 구분합니다.")

        # 비밀번호 생성 버튼
        self.generatePushButton = QtWidgets.QPushButton(self)
        self.generatePushButton.setGeometry(40, 790, 400, 60)
        font.setBold(False)
        self.generatePushButton.setFont(font)
        self.generatePushButton.setText("비밀번호 생성하기")
        self.generatePushButton.setToolTip("클릭하면 설정에 맞는 비밀번호를 생성합니다.")
        self.generatePushButton.setFocus()
        self.generatePushButton.clicked.connect(self.generatePushButton_clicked)

    # 문자를 포함하지 않으면 최소 길이 입력을 제한
    def bCheckBox_toggled(self):
        self.update()
        if self.bUpperLetterCheckBox.isChecked() == False:
            self.lenUpperLetterSpinBox.setEnabled(False)
        else:
            self.lenUpperLetterSpinBox.setEnabled(True)
        if self.bLowerLetterCheckBox.isChecked() == False:
            self.lenLowerLetterSpinBox.setEnabled(False)
        else:
            self.lenLowerLetterSpinBox.setEnabled(True)
        if self.bDigitsCheckBox.isChecked() == False:
            self.lenDigitsSpinBox.setEnabled(False)
        else:
            self.lenDigitsSpinBox.setEnabled(True)
        if self.bSymbolsCheckBox.isChecked() == False:
            self.lenSymbolsSpinBox.setEnabled(False)
        else:
            self.lenSymbolsSpinBox.setEnabled(True)

    # 에러가 발생하면 경고창 출력
    def error(self):
        if self.e == 'errorIndexError':
            bZeroList = self.pg.bZeroList()
            if bZeroList == True:
                self.messageZeroList = QtWidgets.QMessageBox.critical(self, "경고", "문자가 너무 많이 제외되었습니다.")
            else:
                self.messageZeroList = QtWidgets.QMessageBox.critical(self, "경고", "문자를 하나 이상 포함해야 합니다.")
        elif self.e == 'errorZeroSplit':
            self.errorZeroSplit = QtWidgets.QMessageBox.critical(self, "경고", "구분자를 입력하지 않았습니다.")
        elif self.e == 'errorOutOfLength':
            self.messageOutOfLength = QtWidgets.QMessageBox.critical(self, "경고", "비밀번호 길이가 최소 길이보다 작습니다.")
        elif self.e == 'errorNotChar':
            self.messageNotChar = QtWidgets.QMessageBox.critical(self, "경고", "문자만 입력할 수 있습니다.")
        else:
            self.messageNotChar = QtWidgets.QMessageBox.critical(self, "Random Password Generator", self.e)

def main():
    app = QtWidgets.QApplication([])

    MainWindow = MainWidget()
    MainWindow.show()

    app.exec_()

main()