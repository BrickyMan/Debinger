import sqlite3
import datetime

def check_auth(login, password):
	conn = sqlite3.connect('users.db', check_same_thread = False)
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM users WHERE login = (?) AND password = (?)', [login, password])
	result = cursor.fetchall()
	conn.close()
	if len(result) == 0:
		return False
	return True

def register_user(login, password, name):
	conn = sqlite3.connect('users.db', check_same_thread = False)
	cursor = conn.cursor()
	try:
		cursor.execute('INSERT INTO users (id, name, login, password) VALUES (?, ?, ?, ?)', (last_id() + 1, name, login, password))
		conn.commit()
		conn.close()
		return True
	except:
		conn.close()
		return False
	
def get_id(login):
	conn = sqlite3.connect('users.db', check_same_thread = False)
	cursor = conn.cursor()
	cursor.execute('SELECT id FROM users WHERE login = (?)', [login])
	result = cursor.fetchone()[0]
	conn.close()
	return result

def get_userdata_item(id, item):
	conn = sqlite3.connect('users.db', check_same_thread = False)
	cursor = conn.cursor()
	cursor.execute(f'SELECT {item} FROM users WHERE id = (?)', [id])
	result = cursor.fetchone()[0]
	conn.close()
	return result

def get_userdata(id):
	conn = sqlite3.connect('users.db', check_same_thread = False)
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM users WHERE id = (?)', [id])
	data = cursor.fetchone()
	columns = [description[0] for description in cursor.description]
	result = dict(zip(columns, data))
	conn.close()
	print(result)
	return result

def last_id():
	conn = sqlite3.connect('users.db', check_same_thread = False)
	cursor = conn.cursor()
	cursor.execute('SELECT MAX(id) FROM users')
	result = int(cursor.fetchone()[0])
	conn.close()
	return result

# Messages
def send_message(msg_text, user_id):
	msg_text = msg_text.replace('\r\n', '<br>')
	try:
		conn = sqlite3.connect('common_chat.db', check_same_thread = False)
		cursor = conn.cursor()
		now = datetime.datetime.now()
		msg_date = now.strftime("%d.%m.%Y")
		msg_time = now.strftime('%H:%M')
		cursor.execute('INSERT INTO messages (userId, msgDate, msgTime, msgText) VALUES (?, ?, ?, ?)', [user_id, msg_date, msg_time, msg_text])
		conn.commit()
		conn.close()
		return True
	except:
		conn.close()
		return False

def get_all_messages():
	conn = sqlite3.connect('common_chat.db', check_same_thread = False)
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM messages')
	data = cursor.fetchall()
	columns = [description[0] for description in cursor.description]
	result = []
	for row in data:
		result.append(dict(zip(columns, row)))
		# Добавление в данные сообщения информацию об имени отправителя считанную по его id
		result[-1]['userName'] = get_userdata_item(row[1], 'name')
	conn.close()
	return result