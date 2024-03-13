import sys	# sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from main_app import ProdApp
from design import MainWindow


def main():
	app = QtWidgets.QApplication(sys.argv)	# Новый экземпляр QApplication
	window = ProdApp()	# Создаём объект класса ProdApp
	window.show()	# Показываем окно
	app.exec_()	# и запускаем приложение

if __name__ == '__main__':	# Если мы запускаем файл напрямую, а не импортируем
	main()	# то запускаем функцию main()
	"""
	app = QtWidgets.QApplication(sys.argv)
	ex = MainWindow.Ui_MainWindow()
	w = QtWidgets.QMainWindow()
	ex.setupUi(w)
	w.show()
	sys.exit(app.exec_())
	"""