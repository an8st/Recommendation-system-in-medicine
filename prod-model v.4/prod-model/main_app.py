from PyQt5 import QtCore, QtGui, QtWidgets
from design import ResultWindow
from design import MainWindow
from design import NewFormulWindow
from design import ThanksWindow

import re # Для запросов
import os # Для БД
import json # Для БД
import pymorphy3 # Для Нормальной Формы
import locale
locale.setlocale(locale.LC_ALL, '')
import sys
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
import membership as membership


sys.stdout.encoding

morph = pymorphy3.MorphAnalyzer()

DB_RULES_PATH = os.path.join(os.path.dirname(__file__), 'db', 'formuls_json.json')
DB_PREDS_PATH = os.path.join(os.path.dirname(__file__), 'db', 'sympthoms_json.json')
text_if = None
current_symptoms = []
s = {}


class ProdApp(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
	def __init__(self):
		super(ProdApp, self).__init__(parent=None)
		self.main_widow()

	def main_widow(self):
		# Это здесь нужно для доступа к переменным, методам
		# и т.д. в design
		self.ui = MainWindow.Ui_MainWindow()
		self.ui.setupUi(self)  # Это нужно для инициализации дизайна

		# Подключение кнопки
		self.ui.result_button.clicked.connect(self.searchAnswer)

		"""
		Признаки
		"""
		self._preds = {}
		# self.pred_load_btn.clicked.connect(self.loadPredFromDb)
		self.loadPredFromDb()
		"""
		Правила
		"""
		self._rules = {}  # Глобальная база данных
		self.loadRuleFromDb()

		#загружаем симптомы и их значения в ComboBox
		self.ui.S1_edit.addItems(self._preds[self.ui.S1_label.text().lower()])
		self.ui.S2_edit.addItems(self._preds[self.ui.S2_label.text().lower()])
		self.ui.S3_edit.addItems(self._preds[self.ui.S3_label.text().lower()])
		self.ui.S4_edit.addItems(self._preds[self.ui.S4_label.text().lower()])
		self.ui.S5_edit.addItems(self._preds[self.ui.S5_label.text().lower()])
		self.ui.S6_edit.addItems(self._preds[self.ui.S6_label.text().lower()])
		self.ui.S7_edit.addItems(self._preds[self.ui.S7_label.text().lower()])
		self.ui.S8_edit.addItems(self._preds[self.ui.S8_label.text().lower()])
		self.ui.S9_edit.addItems(self._preds[self.ui.S9_label.text().lower()])
		self.ui.S10_edit.addItems(self._preds[self.ui.S10_label.text().lower()])
		self.ui.S11_edit.addItems(self._preds[self.ui.S11_label.text().lower()])
		self.ui.S12_edit.addItems(self._preds[self.ui.S12_label.text().lower()])
		self.ui.S13_edit.addItems(self._preds[self.ui.S13_label.text().lower()])
		# добавляем пустое значение
		self.ui.S1_edit.addItem("")
		self.ui.S2_edit.addItem("")
		self.ui.S3_edit.addItem("")
		self.ui.S4_edit.addItem("")
		self.ui.S5_edit.addItem("")
		self.ui.S6_edit.addItem("")
		self.ui.S7_edit.addItem("")
		self.ui.S8_edit.addItem("")
		self.ui.S9_edit.addItem("")
		self.ui.S10_edit.addItem("")
		self.ui.S11_edit.addItem("")
		self.ui.S12_edit.addItem("")
		self.ui.S13_edit.addItem("")

		if not current_symptoms:
			# выставляем значения по умолчанию. Эти значения соответсвуют здоровому человеку
			self.ui.S1_edit.setCurrentIndex(int(self._preds[self.ui.S1_label.text().lower()][0]))
			self.ui.S2_edit.setCurrentIndex(int(self._preds[self.ui.S2_label.text().lower()][0]))
			self.ui.S3_edit.setCurrentIndex(26) #температура
			self.ui.S4_edit.setCurrentIndex(int(self._preds[self.ui.S4_label.text().lower()][0]))
			self.ui.S5_edit.setCurrentIndex(int(self._preds[self.ui.S5_label.text().lower()][0]))
			self.ui.S6_edit.setCurrentIndex(int(self._preds[self.ui.S6_label.text().lower()][0]))
			self.ui.S7_edit.setCurrentIndex(int(self._preds[self.ui.S7_label.text().lower()][0]))
			self.ui.S8_edit.setCurrentIndex(int(self._preds[self.ui.S8_label.text().lower()][0]))
			self.ui.S9_edit.setCurrentIndex(30) # пульс
			self.ui.S10_edit.setCurrentIndex(70) # верхнее давление
			self.ui.S11_edit.setCurrentIndex(45) # нижнее давление
			self.ui.S12_edit.setCurrentIndex(int(self._preds[self.ui.S12_label.text().lower()][0]))
			self.ui.S13_edit.setCurrentIndex(int(self._preds[self.ui.S13_label.text().lower()][0]))
		else:
			# меняем стиль, если нужно дообследоваться
			if s[self.ui.S1_label.text().lower()] == 'неизвестно' or s[self.ui.S1_label.text().lower()] == 'некорректно':
				#self.ui.S1_label.setStyleSheet("QLabel#S1_label {background: #ffff00;}")
				self.ui.S1_edit.setStyleSheet("QComboBox#S1_edit {background: #ffff00;}")
			if s[self.ui.S2_label.text().lower()] == 'неизвестно' or s[self.ui.S2_label.text().lower()] == 'некорректно':
				self.ui.S2_edit.setStyleSheet("QComboBox#S2_edit {background: #ffff00;}")
			if s[self.ui.S3_label.text().lower()] == 'неизвестно' or s[self.ui.S3_label.text().lower()] == 'некорректно':
				self.ui.S3_edit.setStyleSheet("QComboBox#S3_edit {background: #ffff00;}")
			if s[self.ui.S4_label.text().lower()] == 'неизвестно' or s[self.ui.S4_label.text().lower()] == 'некорректно':
				self.ui.S4_edit.setStyleSheet("QComboBox#S4_edit {background: #ffff00;}")
			if s[self.ui.S5_label.text().lower()] == 'неизвестно' or s[self.ui.S5_label.text().lower()] == 'некорректно':
				self.ui.S5_edit.setStyleSheet("QComboBox#S5_edit {background: #ffff00;}")
			if s[self.ui.S6_label.text().lower()] == 'неизвестно' or s[self.ui.S6_label.text().lower()] == 'некорректно':
				self.ui.S6_edit.setStyleSheet("QComboBox#S6_edit {background: #ffff00;}")
			if s[self.ui.S7_label.text().lower()] == 'неизвестно' or s[self.ui.S7_label.text().lower()] == 'некорректно':
				self.ui.S7_edit.setStyleSheet("QComboBox#S7_edit {background: #ffff00;}")
			if s[self.ui.S8_label.text().lower()] == 'неизвестно' or s[self.ui.S8_label.text().lower()] == 'некорректно':
				self.ui.S8_edit.setStyleSheet("QComboBox#S8_edit {background: #ffff00;}")
			if s[self.ui.S9_label.text().lower()] == 'неизвестно' or s[self.ui.S9_label.text().lower()] == 'некорректно':
				self.ui.S9_edit.setStyleSheet("QComboBox#S9_edit {background: #ffff00;}")
			if s[self.ui.S10_label.text().lower()] == 'неизвестно' or s[self.ui.S10_label.text().lower()] == 'некорректно':
				self.ui.S10_edit.setStyleSheet("QComboBox#S10_edit {background: #ffff00;}")
			if s[self.ui.S11_label.text().lower()] == 'неизвестно' or s[self.ui.S11_label.text().lower()] == 'некорректно':
				self.ui.S11_edit.setStyleSheet("QComboBox#S11_edit {background: #ffff00;}")
			if s[self.ui.S12_label.text().lower()] == 'неизвестно' or s[self.ui.S12_label.text().lower()] == 'некорректно':
				self.ui.S12_edit.setStyleSheet("QComboBox#S12_edit {background: #ffff00;}")
			if s[self.ui.S13_label.text().lower()] == 'неизвестно' or s[self.ui.S13_label.text().lower()] == 'некорректно':
				self.ui.S13_edit.setStyleSheet("QComboBox#S13_edit {background: #ffff00;}")
			# выставляем сохраненные значения
			self.ui.S1_edit.setEditText(current_symptoms[0])
			self.ui.S2_edit.setEditText(current_symptoms[1])
			self.ui.S3_edit.setEditText(current_symptoms[2])
			self.ui.S4_edit.setEditText(current_symptoms[3])
			self.ui.S5_edit.setEditText(current_symptoms[4])
			self.ui.S6_edit.setEditText(current_symptoms[5])
			self.ui.S7_edit.setEditText(current_symptoms[6])
			self.ui.S8_edit.setEditText(current_symptoms[7])
			self.ui.S9_edit.setEditText(current_symptoms[8])
			self.ui.S10_edit.setEditText(current_symptoms[9])
			self.ui.S11_edit.setEditText(current_symptoms[10])
			self.ui.S12_edit.setEditText(current_symptoms[11])
			self.ui.S13_edit.setEditText(current_symptoms[12])

		#self.ui.S1_label.setStyleSheet("QLabel#S1_label {color: #f00;background: #ffff00;}")
		#self.ui.S1_edit.setStyleSheet("QComboBox#S1_edit {color: #f00;background: #ffff00;}")

	def searchAnswer(self):
		"""
		Поиск ответа
		"""
		# получаем значения введенных полей
		global s
		s.clear()
		s = {
			self.ui.S1_label.text().lower(): self.ui.S1_edit.currentText(),
			self.ui.S2_label.text().lower(): self.ui.S2_edit.currentText(),
			self.ui.S3_label.text().lower(): self.ui.S3_edit.currentText(),
			self.ui.S4_label.text().lower(): self.ui.S4_edit.currentText(),
			self.ui.S5_label.text().lower(): self.ui.S5_edit.currentText(),
			self.ui.S6_label.text().lower(): self.ui.S6_edit.currentText(),
			self.ui.S7_label.text().lower(): self.ui.S7_edit.currentText(),
			self.ui.S8_label.text().lower(): self.ui.S8_edit.currentText(),
			self.ui.S9_label.text().lower(): self.ui.S9_edit.currentText(),
			self.ui.S10_label.text().lower(): self.ui.S10_edit.currentText(),
			self.ui.S11_label.text().lower(): self.ui.S11_edit.currentText(),
			self.ui.S12_label.text().lower(): self.ui.S12_edit.currentText(),
			self.ui.S13_label.text().lower(): self.ui.S13_edit.currentText()
		}
		current_symptoms.clear()
		# запоминаем текущие значения
		for s_i in s:
			current_symptoms.append(s[s_i])
		print(current_symptoms)

		# проверяем корректность введенных данных
		for s_i in s:
			is_find=False
			for value_pred in self._preds[s_i]:
				if s[s_i] == value_pred:
					is_find = True
			if is_find == False:
				if s[s_i] == '':
					s[s_i]="неизвестно"
				else:
					s[s_i] = "некорректно"
		# собираем данные в виде симптом=значение
		s_data=[]
		for s_i in s:
			s_data.append(s_i + '=' + s[s_i])

		# загружаем окно с результатами
		self.ui = ResultWindow.Ui_ResultWindow()
		self.ui.setupUi(self)

		# Для масштабирования виджета таблицы
		header = self.ui.result_table.horizontalHeader()
		header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
		header1 = self.ui.result_weight_table.horizontalHeader()
		header1.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

		# дальше считаем и описываем, что заносим в это окно
		
		symptoms_formuls = {}
		important_symptoms = []
		sympt_result_weight_table = '' # симптомы для вывода во вторую таблицу


		# для подсчета весов
		all_weights = {}

		for b_i in range(len(self._rules)):
			# проходимся по каждой болезни
			b = self._rules["b" + str(b_i)]

			# для таблицы весов
			sympt_result_weight_table=''

			for f_i in range(len(b) - 1):
				# проходимся по каждой формуле в этой болезни
				f = b["f" + str(f_i)]
				formula = f["formula"]
				find_s = 0 # количество найденных в формуле симптомов
				count_i = 0  # для подсчета количества И, относящихся к диапазону
				important_symptoms.clear()

				split_formula_only_pred = []
				# разделяем формулу на скобки по И
				split_formula_by_i = formula.replace("\n", "").replace("(", "").replace(")", "").split(' и ')
				for split_formula1_i in split_formula_by_i:
					# разделяем формулу на предикаты
					split_formula2 = split_formula1_i.split(' или ')
					for split_formula2_i in split_formula2:
						# соединяем все вместе, остаются только предикаты
						split_formula_only_pred.append(split_formula2_i)

				# флаг для того, чтобы вовремя остановить поиски
				find_pred=False
				# проходимся по всем частям формулы, разделяемых или
				for split_formula_by_i_j in split_formula_by_i:
					# разделяем формулу по ИЛИ
					split_formula_by_ili = split_formula_by_i_j.split(' или ')
					for split_formula_by_ili_j in split_formula_by_ili:
						# найдем такие параметры, которые принимают значение в диапазоне, а не конкретные значения
						if split_formula_by_ili_j.count('>') > 0:
							# узнаем, какой симптом нам нужен
							sympt_diapazon = split_formula_by_ili_j.split('>')[0]
							# значение симптома
							value_diapazon = float(split_formula_by_ili_j.split('>')[1])

							# проверяем совпадение введенных значений с формулой
							for s_i in range(len(s_data)):
								# проверяем совпадение симптомов, его ли мы сейчас рассматриваем
								if sympt_diapazon == s_data[s_i].split('=')[0]:
									if s_data[s_i].split('=')[1] != "неизвестно" and s_data[s_i].split('=')[1] != "некорректно":
										# если значение подходит
										if float(s_data[s_i].split('=')[1]) > value_diapazon:
											# добавляем в список причин
											important_symptoms.append(s_data[s_i])
											# прибавляем счетчик и выходим из цикла прохождения по симптомам
											find_s += 1
											find_pred = True
											break

						# то же самое, но для знака меньше
						elif split_formula_by_ili_j.count('<') > 0:
							# узнаем, какой симптом нам нужен
							sympt_diapazon = split_formula_by_ili_j.split('<')[0]
							# значение симптома
							value_diapazon = float(split_formula_by_ili_j.split('<')[1])

							# проверяем совпадение введенных значений с формулой
							for s_i in range(len(s_data)):
								# проверяем совпадение симптомов, его ли мы сейчас рассматриваем
								if sympt_diapazon == s_data[s_i].split('=')[0]:
									if s_data[s_i].split('=')[1] != "неизвестно" and s_data[s_i].split('=')[1] != "некорректно":
										# если значение подходит
										if float(s_data[s_i].split('=')[1]) < value_diapazon:
											# добавляем в список причин
											important_symptoms.append(s_data[s_i])
											# прибавляем счетчик и выходим из цикла прохождения по симптомам
											find_s += 1
											find_pred = True
											break

						# если в формуле лингвистическая переменная, рассчитаем функцию принадлежности
						elif split_formula_by_ili_j.count('высок') > 0 or split_formula_by_ili_j.count('норм') > 0 or split_formula_by_ili_j.count('низк') > 0:
							# узнаем, какой симптом нам нужен в формуле из БЗ
							sympt = split_formula_by_ili_j.split('=')[0]
							# значение симптома в формуле из БЗ
							bz_value = split_formula_by_ili_j.split('=')[1]
							# проверяем совпадение введенных значений с формулой
							for s_i in range(len(s_data)):
								# проверяем совпадение симптомов, его ли мы сейчас рассматриваем
								if sympt == s_data[s_i].split('=')[0]:
									if s_data[s_i].split('=')[1] != "неизвестно" and s_data[s_i].split('=')[1] != "некорректно":
										# рассчитываем функцию принадлежности
										# передаем название симптома, его значение и значение из БЗ
										current_value = float(s_data[s_i].split('=')[1])
										# проверяем, что введенное число принадлежит классу
										if membership.f_is_in_class(sympt, current_value, bz_value):
											# добавляем в список симптомов
											important_symptoms.append(s_data[s_i])
											find_s += 1
											find_pred = True
											break

						# ищем совпадение значений для S=*
						else:
							for s_i in range(len(s_data)):
								if split_formula_by_ili_j.find(s_data[s_i]) >= 0:
									important_symptoms.append(s_data[s_i])
									find_s += 1
									find_pred = True
									break

						# останавливаем поиски, если в этой части формулы уже нашли совпадения
						if find_pred:
							break

				# считаем вероятность, что ответ верный
				probability_true = round(float(float(f["true"]) / (float(f["false"]) + float(f["true"]))), 2)

				# если количество совпадений равно количеству частей в формуле, разделенных И, то формула выполняется
				if find_s == len(split_formula_by_i):
					# собираем симптомы в строку
					for d in range(len(important_symptoms)):
						if d == 0:
							symptoms_formuls[formula] = important_symptoms[d] + '\n'
						else:
							# избавляемся от повторений
							if symptoms_formuls[formula].count(important_symptoms[d]) == 0:
								symptoms_formuls[formula] += important_symptoms[d] + '\n'







					"""
					1 таблица
					"""
					current_row = self.ui.result_table.rowCount()
					self.ui.result_table.setRowCount(current_row + 1)
					self.ui.result_table.setItem(current_row, 1, QtWidgets.QTableWidgetItem("да"))  # результат
					self.ui.result_table.setItem(current_row, 2, QtWidgets.QTableWidgetItem(b["name"]))  # врач
					self.ui.result_table.setItem(current_row, 3,
												 QtWidgets.QTableWidgetItem(str(probability_true)))  # корректность
					self.ui.result_table.setItem(current_row, 4,
												 QtWidgets.QTableWidgetItem(symptoms_formuls[formula]))  # причина
					self.ui.result_table.setItem(current_row, 5, QtWidgets.QTableWidgetItem(f["formula"]))  # формула

					"""
                    2 таблица
                    """
					# добавляем в список весов
					all_weights[formula] = {"result": 1, "weight": probability_true}
					sympt_result_weight_table += symptoms_formuls[formula]

				else:
					# если формула не выполняется
					"""
                    1 таблица
                    """
					current_row = self.ui.result_table.rowCount()
					self.ui.result_table.setRowCount(current_row + 1)
					self.ui.result_table.setItem(current_row, 1, QtWidgets.QTableWidgetItem("нет"))  # нужно посетить
					self.ui.result_table.setItem(current_row, 2, QtWidgets.QTableWidgetItem(b["name"]))  # врач
					self.ui.result_table.setItem(current_row, 3,
												 QtWidgets.QTableWidgetItem(str(probability_true)))  # корректность
					self.ui.result_table.setItem(current_row, 4, QtWidgets.QTableWidgetItem(""))  # причина
					self.ui.result_table.setItem(current_row, 5, QtWidgets.QTableWidgetItem(f["formula"]))  # формула
					"""
                    2 таблица
                    """
					# добавляем в список весов
					all_weights[formula] = {"result": -1, "weight": probability_true}


								









			# нормализация
			sum_weights = 0.0 # сумма весов
			diagnoz_result = 0.0 # итоговое значение диагноза

			for all_weights_i in all_weights:
				sum_weights += float(all_weights[all_weights_i]["weight"])
			for all_weights_i in all_weights:
				diagnoz_result += all_weights[all_weights_i]["weight"] / sum_weights * all_weights[all_weights_i]["result"]
			diagnoz_result = round(diagnoz_result,2)
			all_weights.clear()
			"""
			2 таблица
			"""
			current_row = self.ui.result_weight_table.rowCount()
			self.ui.result_weight_table.setRowCount(current_row + 1)
			if diagnoz_result>=0:
				self.ui.result_weight_table.setItem(current_row, 0, QtWidgets.QTableWidgetItem("да"))  # нужно посетить
			else:
				self.ui.result_weight_table.setItem(current_row, 0, QtWidgets.QTableWidgetItem("нет"))  # нужно посетить
			self.ui.result_weight_table.setItem(current_row, 1, QtWidgets.QTableWidgetItem(b["name"]))  # врач
			self.ui.result_weight_table.setItem(current_row, 2,	 QtWidgets.QTableWidgetItem(str(diagnoz_result)))  # результат
			self.ui.result_weight_table.setItem(current_row, 3, QtWidgets.QTableWidgetItem(sympt_result_weight_table))  # причина


		"""
		1 таблица
		"""
		# добавляем чекбоксы
		for row in range(self.ui.result_table.rowCount()):
			widget = QWidget()
			checkbox = QCheckBox()
			checkbox.setCheckState(Qt.Unchecked)
			layoutH = QHBoxLayout(widget)
			layoutH.addWidget(checkbox)
			layoutH.setAlignment(Qt.AlignCenter)
			layoutH.setContentsMargins(0, 0, 0, 0)
			self.ui.result_table.setCellWidget(row, 0, widget)
		"""
		3 таблица
		"""
		check_not=0
		# проверяем, есть ли врачи, которых нужно посетить
		for i in range(self.ui.result_weight_table.rowCount()):
			if self.ui.result_weight_table.item(i, 0).text() == 'нет':
				check_not+=1

		# Подключение кнопки
		self.ui.continue_button.clicked.connect(self.f_continue)



	# прибавляем true false в зависимости от чекбоксов
	def f_continue(self):
		# проверяем, где врач поставил галочки
		checked_list = []
		for i in range(self.ui.result_table.rowCount()):
			# если чекбокс отмечен
			if self.ui.result_table.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
				for b_i in range(len(self._rules)):
					# проходимся по каждой болезни
					b = self._rules["b" + str(b_i)]
					if b["name"] == self.ui.result_table.item(i, 2).text():
						for f_i in range(len(b) - 1):
							# проходимся по каждой формуле в этой болезни
							f = b["f" + str(f_i)]
							if f["formula"] == self.ui.result_table.item(i, 5).text():
								f["true"] += 1
			# если чекбокс не отмечен
			else:
				for b_i in range(len(self._rules)):
					# проходимся по каждой болезни
					b = self._rules["b" + str(b_i)]
					if b["name"] == self.ui.result_table.item(i, 2).text():
						for f_i in range(len(b) - 1):
							# проходимся по каждой формуле в этой болезни
							f = b["f" + str(f_i)]
							if f["formula"] == self.ui.result_table.item(i, 5).text():
								f["false"] += 1
		self.saveRuleToDb()
		self.thanks_widow()

	# окно с 3 кнопками
	def thanks_widow(self):
		self.ui = ThanksWindow.Ui_ThanksWindow()
		self.ui.setupUi(self)
		# Подключение кнопки
		self.ui.start_button.clicked.connect(self.main_widow) # вернуться в начало
		self.ui.new_formul_button.clicked.connect(self.add_new_rule_window)
		self.ui.exit_button.clicked.connect(lambda:self.close())

	"""
	Здесь все для нашего "калькулятора"
	"""
	def add_new_rule_window(self):
		self.ui = NewFormulWindow.Ui_NewFormulWindow()
		self.ui.setupUi(self)
		# Подключение кнопки
		self.ui.start_button.clicked.connect(self.main_widow) # вернуться в начало
		self.ui.add_to_BZ_button.clicked.connect(self.add_new_rule)  # добавить правило в БЗ

		self.ui.button_0.clicked.connect(self.add_digit)
		self.ui.button_1.clicked.connect(self.add_digit)
		self.ui.button_2.clicked.connect(self.add_digit)
		self.ui.button_3.clicked.connect(self.add_digit)
		self.ui.button_4.clicked.connect(self.add_digit)
		self.ui.button_5.clicked.connect(self.add_digit)
		self.ui.button_6.clicked.connect(self.add_digit)
		self.ui.button_7.clicked.connect(self.add_digit)
		self.ui.button_8.clicked.connect(self.add_digit)
		self.ui.button_9.clicked.connect(self.add_digit)
		self.ui.button_i.clicked.connect(self.add_digit)
		self.ui.button_ili.clicked.connect(self.add_digit)
		self.ui.button_equal.clicked.connect(self.add_digit)
		self.ui.button_more.clicked.connect(self.add_digit)
		self.ui.button_no_name.clicked.connect(self.add_digit)
		self.ui.button_not_correct.clicked.connect(self.add_digit)
		self.ui.button_no.clicked.connect(self.add_digit)
		self.ui.button_then.clicked.connect(self.add_digit)
		self.ui.button_if.clicked.connect(self.add_digit)
		self.ui.button_dot.clicked.connect(self.add_digit)
		self.ui.button_less.clicked.connect(self.add_digit)
		self.ui.button_10.clicked.connect(self.add_digit)
		self.ui.button_11.clicked.connect(self.add_digit)
		self.ui.button_space.clicked.connect(self.add_digit)
		self.ui.clear_button.clicked.connect(self.backspace)

		# списки симптомов и врачей
		for pred in self._preds:
			self.ui.pred_list.addItem(pred)
		for b_i in range(len(self._rules)):
			b = self._rules["b" + str(b_i)]
			self.ui.doctor_list.addItem(b['name'])

		# добавляем в строку симптомы и врачей
		self.ui.pred_list.itemClicked.connect(self.add_item)
		self.ui.doctor_list.itemClicked.connect(self.add_item)

	def add_item(self, item):
		self.ui.vvod_edit.setText(self.ui.vvod_edit.toPlainText() + item.text())

	# символы
	def add_digit(self):
		btn = self.sender()
		digit_buttons = ('button_space')
		if btn.objectName() in digit_buttons:
			self.ui.vvod_edit.setText(self.ui.vvod_edit.toPlainText() + ' ')
		else:
			self.ui.vvod_edit.setText(self.ui.vvod_edit.toPlainText() + btn.text())

	# стирание последнего символа
	def backspace(self):
		entry = self.ui.vvod_edit.toPlainText()
		if len(entry) != 1:
			self.ui.vvod_edit.setText(entry[:-1])
		else:
			self.ui.vvod_edit.setText('')


	# добавление правила
	def add_new_rule(self):
		flag=True
		# получаем текст из интерфейса
		if len(self.ui.vvod_edit.toPlainText()) > 0:
			new_formul = self.ui.vvod_edit.toPlainText()
			new_formul = str(new_formul).lower()

			new_formul=new_formul.replace("если ", "")
			# разделяем на консеквент и антецедент
			bolezn=[]
			if len(new_formul) > 0 and new_formul.count(", то "):
				bolezn = new_formul.split(", то ")[1]
				new_formul=new_formul.split(", то ")[0]

			# проверка формулы на ошибки
			if self.check_formul(new_formul) == False:
				flag = False
			else:
				# проверяем, существует ли уже такая болезнь
				x = 0
				index_bolezn = 0
				for b_i in range(len(self._rules)):
					b = self._rules["b" + str(b_i)]
					if b['name'] != bolezn:
						x += 1
					else:
						index_bolezn = b_i

				# если нет такой болезни, добавляем новую
				if x == len(self._rules) and len(new_formul) > 0:
					self._rules['b'+str(len(self._rules))]= {
							"name": bolezn,
							"f0": {
								"formula": new_formul,
								"true": 1,
								"false": 0
							}
						}
				# если уже есть такая болезнь, добавляем к ней формулу
				else:
					self._rules['b'+str(index_bolezn)][str('f' + str(len(self._rules['b'+str(index_bolezn)])-1))]= {
						"formula": new_formul.split(", то ")[0],
						"true": 1,
						"false": 0
					}
				self.saveRuleToDb()

			if flag:
				self.thanks_widow()


	def check_formul(self, formul):
		formul = formul.replace(" ", "_")
		formul = formul.replace("_и_", " ")
		formul = formul.replace("_или_", " ")
		formul = formul.replace("<", "=")
		formul = formul.replace(">", "=")
		formul = formul.split()
		for f in formul:
			f=f.replace("_", " ")
			f_pred=f.split("=")[0]
			f_value = f.split("=")[1]

			str=''
			for p in self._preds:
				str+=p

			if str.find(f_pred) < 0:
				self.showMessage("Такого предиката не существует!", f)
				return False

			if self._preds[f_pred].count(f_value)<=0:
				self.showMessage("Такого значения предиката не существует!", f)
				return False

		return True

	def showMessage(self, info, details):
		"""
		Выведение сообщения на экран
		"""
		msg = QtWidgets.QMessageBox()
		msg.setText(info)
		msg.setWindowTitle("Ошибка!")
		msg.setDetailedText(details)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		msg.exec_()

	def loadRuleFromDb(self):
		"""
		Загрузка правил из базы данных (файл формата JSON)
		"""
		rules_path = DB_RULES_PATH
		with open(rules_path, 'r', encoding="utf-8") as infile:
			data = json.load(infile)
		self._rules = data

	def saveRuleToDb(self):
		"""
		Сохранение в Базу Данных (файл формата JSON)
		"""
		data = self._rules
		rules_path = DB_RULES_PATH

		with open(rules_path, 'w', encoding="utf-8") as outfile:
			json.dump(data, outfile, indent=1, ensure_ascii=False)

	def loadPredFromDb(self):
		"""
		Загрузка правил из Базы Данных (файл формата JSON)
		"""
		preds_path = DB_PREDS_PATH
		with open(preds_path, 'r', encoding="utf-8") as infile:
			data = json.load(infile)
		self._preds = data












# ПРИЗНАКИ

	def addPred(self):
		text = self.getNormal(self.pred_line.text())
		if(text not in self._preds):
			self._preds.add(text)
		else:
			self.showMessage('Ошибка! Такой признак уже присутствует в Базе Признаков', str())

	def savePredToDb(self):
		"""
		Сохранение в базу данных (файл формата JSON)
		"""
		data = list(self._preds)
		preds_path = DB_PREDS_PATH

		with open(preds_path, 'w', encoding="utf-8") as outfile:
			json.dump(data, outfile, indent=1, ensure_ascii=False)

		self.showMessage('Атрибуты "{}" сохранены в {}\n'.format(self._preds, preds_path), str())
		self.loadPredFromDb()

# ПРАВИЛА

	def addRule(self):
		"""
		Добавление правила
		"""
		global text_if
		text_if = self.getNormal(self.rule_if_line.text())
		text_then = self.getNormal(self.rule_then_line.text())

		print(text_if)
		if self.checkIf(text_if):
			print(text_if)
			i = self.rules_table.rowCount()
			self._rules[text_if] = text_then
			self.rules_table.setRowCount(i + 1)

			new_if = QtWidgets.QTableWidgetItem(text_if)
			self.rules_table.setItem(i, 0, new_if)
			text_then = self.rule_then_line.text()

			new_then = QtWidgets.QTableWidgetItem(text_then)
			self.rules_table.setItem(i, 1, QtWidgets.QTableWidgetItem(new_then))

	def getNormal(self, offer):
		offer = offer.lower()
		words = offer.split()
		new_offer = ""
		for word in words:
			p = morph.parse(word)[0]
			if(new_offer != ""):
				new_offer += " "
			# анализ слова, перевод в именительный падеж
			new_offer += p.normal_form
		return new_offer

	def checkIf(self, text):
		or_terms = self.offerToTerms(text)
		for and_terms in or_terms:
			for term in and_terms:
				if(term not in self._preds):
					self.showMessage('Признак \' '+term+' \' отсутствует в Базе Признаков', str())
					return False

		return True

	def offerToTerms(self, offer):
		"""
		Создание правил из предложений
		"""
		offer = self.getNormal(offer)

		or_terms = []
		or_strings = self.splitOr(offer)

		for or_str in or_strings:
			and_terms = self.splitAnd(or_str)
			or_terms.append(and_terms)
		return or_terms

	def splitAnd(self,offer):
		str_and = re.split(r" и ", offer)
		return self.listToDict(str_and)

	def splitOr(self,offer):
		str_or = re.split(r" или ", offer)
		return str_or

	def listToDict(self, list):
		dict = set()
		for str in list:
			dict.add(str)
		return dict


