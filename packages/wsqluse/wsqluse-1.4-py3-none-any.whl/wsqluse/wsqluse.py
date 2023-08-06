import psycopg2
import logging
from wsqluse import functions
from traceback import format_exc


class Wsqluse:
	def __init__(self, dbname, user, password, host, debug=False):
		self.dbname = dbname
		self.user = user
		self.password = password
		self.host = host
		self.debug = debug

	def try_execute(self, command, returning='id'):
		# Попытка выполнить заданную команду. Если успешно - возвращает словарь с id строки и кодом 1
		# Если же нет - код 0 и Tracebaсk
		self.show_print("\n", locals(), debug=True)
		command = self.pre_execute_format(command, returning)
		self.show_print('\nПопытка выполнить комманду', command, debug=True)
		cursor, conn = self.get_cursor_conn()
		try:
			cursor.execute(command)
			conn.commit()
			record_id = cursor.fetchall()
			response = functions.get_execute_result(status='success', info=record_id)
			self.show_print('\tУспешно!', debug=True)
		except psycopg2.Error:
			response = self.transaction_fail(cursor)
		return response

	def pre_execute_format(self, command, returning):
		"""
		Операции форматирования, выполняемые над командой перед выполнением,
		могут быть предопледенеы
		:param command:
		:param returning:
		:return:
		"""
		if returning:
			command = self.add_returning(command, returning)
		return command

	def add_returning(self, command, some_id):
		# Расширяет передаеваемую комманду параметром RETURNING <ID>
		command += " RETURNING {}".format(some_id)
		return command

	def get_cursor_conn(self):
		self.show_print("\n", locals(), debug=True)
		# Создает и возвращает cursor & conn для дальнейших операций с ними
		conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
		cursor = conn.cursor()
		return cursor, conn

	def transaction_fail(self, cursor):
		# При неудачной транзакции - logging & rollback. Вернуть текст ошибки
		self.show_print(format_exc())
		logging.error(format_exc())
		cursor.execute("ROLLBACK")
		self.show_print('\tТранзакция провалилась. Откат.', debug=True)
		response = functions.get_execute_result(status='failed', info=str(format_exc()))
		return response

	def try_execute_get(self, command, mode='usual', returning='id'):
		# Используется для извлечения данных из БД. Возвращает словарь, с кодом status=success, если все успешно и под кодом
		# info будут данные. Либо, если транзакция проварилась, код status=fail, с traceback в info
		self.show_print("\n", locals(), debug=True)
		self.show_print('Попытка выполнить комманду:', command, debug=True)
		cursor, conn = self.get_cursor_conn()
		try:
			cursor.execute(command)
			record = cursor.fetchall()
			if mode == 'usual':
				self.show_print('\tДанные получены -', record, debug=True)
				response = functions.get_execute_result(status='success', info=record)
				return record
			elif mode == 'col_names':
				column_names = [desc[0] for desc in cursor.description]
				response = functions.get_execute_result(status='success', records=record, column_names=column_names)
				return response
		except psycopg2.Error:
			response = self.transaction_fail(cursor)
			return response

	def join_tuple_string(self, msg):
		return ' '.join(map(str, msg))

	def show_print(self, *msg, debug=False):
		# Показать сообщение в общий поток вывода. Если debug=False показывает не все сообщения.
		msg = self.join_tuple_string(msg)
		if not debug:
			print(msg)
		elif debug and self.debug:
			print(msg)

	def get_table_dict(self, command):
		# Возвращает данные из таблицы, в виде имя поле-значение
		self.show_print("\n", locals(), debug=True)
		self.show_print('Попытка выполнить комманду:', command, debug=True)
		response = self.try_execute_get(command, mode='col_names')
		if response['status'] == 'success':
			records = response['records']
			column_names = response['column_names']
			if records and len(records) > 0:
				table_dict = functions.zip_dicts(records, column_names)
				response = functions.get_execute_result(status='success', info=table_dict)
			else:
				response = functions.get_execute_result(status='failed', info='records is None or len of records < 1')
			return response
		else:
			return response


	def try_execute_double(self, command, values):
		self.show_print('\nПопытка выполнить комманду', command, debug=True)
		command = self.pre_execute_format(command, 'id')
		cursor, conn = self.get_cursor_conn()
		try:
			cursor.execute(command, values)
			conn.commit()
			record_id = cursor.fetchall()
			response = functions.get_execute_result(status='success',
													info=record_id)
		except psycopg2.Error:
			response = self.transaction_fail(cursor)
		return response
