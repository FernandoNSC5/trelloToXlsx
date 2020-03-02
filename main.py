import sys
import _thread

#pyqt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton,
			 QApplication, QMessageBox, QLineEdit, QWidget, QLabel, 
			 QGridLayout, QRadioButton, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPen, QIntValidator

import trello_process

class App(QMainWindow):

	def __init__(self):
		super().__init__()

		#################################################
		##	STATIC VAR
		self.pixmap = QPixmap("src/bg.png")
		self.title = "Trello to XLSX"
		self.LEFT = 10
		self.TOP = 10
		self.WIDTH = 800
		self.HEIGHT = 600
		_trello = trello_process.TrelloProcess() 

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



		## Draw product btn
		#self.drawProductButton()

		self.show()

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
	def productAppAction(self):
		print("Button is working")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.resize(ex.pixmap.width(), ex.pixmap.height())
	ex.move(500, 500)
	ex.setFixedSize(ex.size())
	ex.update()
	sys.exit(app.exec_())