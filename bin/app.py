import web
import sqlite3
import time

web.config.debug = False

urls = (
  '/', 'Index',
  '/comms', 'Comms',
  '/kill', 'reset',
  '/chat', 'chat'
)

app = web.application(urls, globals())
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'nick': ''})
render = web.template.render('templates/', base="layout")


class Index(object):
	"""Create new session and start page"""

    name = ''
    def GET(self):
       if web.config.get('_session') is None:
          web.config._session = session
	      return render.hello_form()
       else:
          return render.comms()


class reset(object):
    """Logout from profile"""

    def POST(self):
	session.kill()
	web.config._session = None
	return render.hello_form()

class Comms(object):
    """Authentication and registration"""

    def POST(self):
	conn = sqlite3.connect('database/users.db')
	c = conn.cursor()
	form = web.input()
        username = form.name
        password = form.passw
	c.execute('''SELECT COUNT(*) FROM USERS WHERE name = ?''', (username, ))
	if c.fetchone()[0] == 1 :
		c.execute('''SELECT COUNT(*) FROM USERS WHERE name = ? AND password = ?''', (username, password))
		if c.fetchone()[0] == 1:
			session.nick = username
			return render.comms()
		else:
			return render.hello_form()
	else: 
		c.execute('''INSERT INTO USERS(name, password) VALUES(?, ?)''', (username, password))
		session.nick = username
		conn.commit()
		conn.close()
		return render.comms()

class chat(object):
    """Get the comments or add the comments"""

    def GET(self):
	cmnts = []
	conn = sqlite3.connect('database/users.db')
	c = conn.cursor()
	c.execute('''SELECT * FROM COMMS''')
	cmnts = c.fetchall()
	conn.close()
	return render.chat(comments = cmnts)

    def POST(self):
	form = web.input()
	comment = form.comment
	conn = sqlite3.connect('database/users.db')
	c = conn.cursor()
	c.execute('''INSERT INTO COMMS(date, username, comment) VALUES(?, ?, ?)''', (time.strftime("%c"), session.nick, comment))
	conn.commit()
	conn.close()
	return render.comms()
	


if __name__ == "__main__":
    app.run()
