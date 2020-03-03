import sys
import threading
import time

#pyqt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, 
							QLineEdit, QWidget, QLabel, QGridLayout, QRadioButton, 
							QComboBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPen, QIntValidator

import trello_process

class App(QMainWindow):

	def __init__(self):
		super().__init__()

		#################################################
		##	STATIC VAR
		self.INITIALIZATION = "src/img/init.png"
		self.BG = "src/img/bg.png"
		self.ERROR = "src/img/error.png"

		# INIT LOGGER
		self.LOGGER = ""

		self.pixmap = QPixmap(self.INITIALIZATION)
		self.title = "Conversor XLSX"
		self.LEFT = 10
		self.TOP = 10
		self.WIDTH = 800
		self.HEIGHT = 600

		## Destroying Windows Flags
		self.setWindowFlags(
						QtCore.Qt.Window |
						QtCore.Qt.CustomizeWindowHint |
						QtCore.Qt.WindowTitleHint |
						QtCore.Qt.WindowCloseButtonHint |
						QtCore.Qt.WindowStaysOnTopHint
						)

		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT)

		#Initializing trello
		'''try:
			self.LOGGER = "Inicializando..."
			self.TRELLO = trello_process.TrelloProcess()
			self.LOGGER = "Conectando ao servidor..."
			self.TRELLO.connection()
			self.LOGGER = "Buscando Board..."
			self.TRELLO.get_board()
			self.LOGGER = "Buscando usuários..."
			self.TRELLO.get_board_users()
			self.LOGGER = "Processando usuários..."'''

		#starting
		self.draw_initialization()
		try:
			x =threading.Thread(target=self.load_system, args=())
			x.start()
		except:
			print("ERROR")

		## Draw product btn
		#self.drawProductButton()

		self.show()


	def load_system(self):
		self.init_label.setText("Inicializando...")
		self.update()
		self.TRELLO = trello_process.TrelloProcess()
		self.init_label.setText("Conectando ao trello...")
		self.update()
		self.TRELLO.connection()
		self.init_label.setText("Procurando Board...")
		self.update()
		self.TRELLO.get_board()
		self.init_label.setText("Procurando usuários...")
		self.update()
		self.TRELLO.get_board_users()
		self.init_label.setText("Processando usuários...")
		self.update()
		self.TRELLO.convert_user()
		self.init_label.setText("Inicializando componentes...")
		self.update()
		self.TRELLO.setCards()
		self.init_label.setText("Buscando listas...")
		self.update()
		self.TRELLO.get_lists()
		self.init_label.setText("Processando dados recebidos")
		self.update()
		time.sleep(1)
		self.init_label.setText("Processando dados recebidos.")
		self.update()
		self.TRELLO.process_data()
		self.init_label.setText("Processando dados recebidos..")
		self.update()
		time.sleep(1)
		self.init_label.setText("Processando dados recebidos...")
		self.update()
		time.sleep(1)
		self.init_label.setText("Processando dados recebidos... Pronto")
		self.update()
		time.sleep(1)
		self.init_label.setText("Logando")
		self.update()
		time.sleep(1)

		#Changing layout
		self.turn_off_all([self.init_label])
		self.pixmap = QPixmap(self.BG)
		self.update()

	def turn_off_all(self, elements):
		for data in elements:
			data.setVisible(False)

	def start_main_screen(self):
		self.LABEL_FILE_MANAGER = "Selecione a planilha:"
		self.BUTTON_NAME = "Gerar Planilha"
		self.LOGGER = TRELLO.getLogger() 	#Getting initial logger

		#Shows errors if existent
		if self.LOGGER != "":
			msg = QMessageBox()
			msg.setText(self.LOGGER)
			msg.setWindowsTitle("Atenção")
			msg.setStandardButtons(QMessageBox.Ok)

		self.draw_main_screen()

	#####################################################
	##	Paint event
	def paintEvent(self, e):
		painter = QtGui.QPainter(self)
		painter.drawPixmap(self.rect(), self.pixmap)
		painter.setRenderHint(QPainter.Antialiasing, True)

		pen = QtGui.QPen()
		pen.setWidth(3)
		pen.setColor(QtCore.Qt.black)
		pen.setCapStyle(QtCore.Qt.RoundCap)
		pen.setJoinStyle(QtCore.Qt.RoundJoin)
		painter.setPen(pen)

	#####################################################
	## SCREENS
	def draw_main_screen(self):
		# Label for path
		self.pathLabel = QLabel(self)
		self.pathLabel.setVisible(True)
		#self.pathLabel.move()
		#self.pathLabel.resize()
		self.pathLabel.setText("Arquivo: ")

		# Path
		self.textPath = QLine(self)
		self.textPath.setVisible(True)
		self.textPath.disabled(True)
		#self.textPath.width()
		self.setText("Escolha um arquivo")

		# Button for path search
		self.pathBtn = QPushButton("Buscar", self)
		self.pathBtn.setVisible(True)
		#self.pathBtn.resize()
		#self.pathBtn.setStylesheet()
		#self.pathBtn.move()
		self.pathBtn.clicked.connect(self.findPath)

	def call_file_explorer(self):
		#	File manager
		options = QFileDialog.Options()
		opstions |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Excel Files (*xlsx)", options=options)
		if fileName:
			print(files)
			return fileName
		return None

	def draw_initialization(self):
		self.init_label = QLabel(self.LOGGER, self)
		self.init_label.setVisible(True)
		self.init_label.setAlignment(QtCore.Qt.AlignCenter)
		self.init_label.move(200, 500)
		self.init_label.setFixedWidth(400)
		self.init_label.setStyleSheet("border:1px solid black; color: #4C0000; font-family: Calibri; font-size: 20px")

	def drawProductButton(self):
		## This conditional will tell the button what to display
		self.ProductBtn = QPushButton("Botão qualquer", self)


		self.ProductBtn.setVisible(True)
		self.ProductBtn.resize(490,120)
		self.ProductBtn.move(157,345)
		self.ProductBtn.setStyleSheet("QPushButton {background-color: #CAB8B2}"
				"QPushButton {color: white}"
				"QPushButton {border-radius: 12px}"
				"QPushButton {font-family: Calibri}"
				"QPushButton {font-size: 20px}"
				"QPushButton:hover {background-color: #a3867c}"
				"QPushButton:hover:!pressed {background-color: #6e5f5a}")

		## This conditional will acept action (or not)
		self.ProductBtn.clicked.connect(self.productAppAction)

	#	End of painting events
	#########################################################
	#	Python slots
	@pyqtSlot()
	def findPath(self):
		self.call_file_explorer()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.resize(ex.pixmap.width(), ex.pixmap.height())
	ex.move(500, 500)
	ex.setFixedSize(ex.size())
	ex.update()
	sys.exit(app.exec_())