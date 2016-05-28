from flask import Flask, render_template, request, redirect, session, Response, send_file, make_response
import MySQLdb as mdb
import json
import math
import hashlib
import csv
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

#data query functions
def getSchoolName(school):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select name from schools where ident = \'" + school + "\'"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows[0]['name']

def updateTeacherStatus(school, value, id, zone):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "update " + school + zone + " set value = " + value + " where id = " + id
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)

def getIdList():
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select id from schools"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows

groups = {}

for i in getIdList():
	groups.update({i['id']:[]})

def getSchools():
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select ident from schools"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows


def getSchoolId(ident):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select id from schools where ident = \'" + ident + "\'" 
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows[0]['id']

def getId(ident):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select id from schools where ident = \'" + ident + "\';"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows[0]['id']

def getZones(i):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select zone from " + i + "zone"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows

def getTeachers(zone):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select * from " + zone
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows

def getPercent(school, zone):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select value from " + school + zone
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    x = 0.0
    for i in rows:
    	x += int(i['value'])
    return str(int(round((x/len(rows)) * 100)))

def getPercentFromZone(inp):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select value from " + inp
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows

def getSchoolNames():
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select name, id, ident from schools"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows

def getSchoolPercent(school):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select zone from " + school + "zone"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows

def getPasswords(school):
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select password from password where id = " + school
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows[0]['password']

def getAdminPassword():
    con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
    query = "select password from adminpassword"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows[0]['password']

def getIdent(i):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select ident from schools where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]['ident']

def getI(i):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select id from schools where ident = \'" + i + "\'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]['id']

def getSchoolInfo():
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select * from schools"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def updatePassword(password, i):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "update password set password = \'" + encrypt(password) + "\' where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def updateAdminPassword(password):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "update adminpassword set password = \'" + encrypt(password) + "\'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def schoolNameFromId(i):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select name from schools where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]['name']

def getAllZones(school):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select zone from " + str(school) + "zone"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	tot = []
	for i in rows:
		z = i['zone']
		for n in getTeachers(z):
			tot.append(n)
	new = ""
	for i in tot:
		va = "absent"
		if i['value'] == 1:
			va = "present"
		new +=  "\"" + i['name'] + "\", \"" + va + "\"\n"
	return new

def getNewestZone(school):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select zone from " + school + "zone"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	if rows:
		return rows[len(rows)-1]['zone'][len(rows[len(rows)-1]['zone'])-1]
	else:
		return chr(96)

def addZone(school, letter):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "insert into " + school + "zone values('" + school + letter + "')"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def addZoneTable(school, letter):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "create table " + school + letter + " (id int auto_increment primary key, name varchar(500), value tinyint(1));"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def addToZone(name, zone):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "insert into " + zone + "(name, value) values ('" + name + "', 0);"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def deleteTable(table):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "drop table " + table
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def deleteTableEntry(school, table):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "delete from " + school + "zone where zone = '" + table + "'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def renameTable(table, name):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	if table != name:
		query = "rename table " + table + " to " + name
		with con:
			cur = con.cursor(mdb.cursors.DictCursor)
			cur.execute(query)
			rows = cur.fetchall()

def renameTableEntry(school, table, name):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "update " + school + "zone set zone = '" + name + "' where zone = '" + table + "'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def addTeacher(table, name):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "insert into " + table + " (name, value) values ('" + name + "', 0)"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def howManyZones(school):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select zone from " + school + "zone"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return len(rows)

def deleteTeacher(zone, teacher):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "delete from " + zone + " where id = " + teacher
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def getSpecificTeacher(zone, teacher):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select * from " + zone + " where id = " + teacher
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def updateTeacherName(zone, name, teacher):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "update " + zone + " set name = '" + name + "' where id = " + teacher
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getZoneLength(zone):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select * from " + zone
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return len(rows)

def createNewSchool(name, ident, i):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "insert into schools (id, name, ident) values (" + i + ", '" + name + "', '" + ident + "')"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return len(rows)

def getIdents():
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select ident from schools"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getIdFromIdent(ident):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select id from schools where ident = '" + ident + "'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def createTableTable(i):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "create table " + i + "zone (zone varchar(500))"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getNewestId():
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select id from schools"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return str(int(rows[len(rows)-1]['id']) + 1)

def addNewPassword(i, password):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "insert into password (id, password) values (" + i + ", '" + encrypt(password) + "')"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def deleteSchoolfromSchool(school):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "delete from schools where id = " + school
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def deleteSchoolZone(school):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "drop table " + school + "zone"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def deleteZoneTable(name):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "drop table " + name
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def deletePassword(school):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "delete from password where id = " + school
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()

def getNumberOfSchools():
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select name from schools"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return len(rows)

#login functions
def adminLogin():
	session['admin'] = "true"

def adminIsIn():
	if 'admin' in session:
		return True
	else:
		return False

def adminLogout():
	session.pop('admin', None)

def schoolLogin(school):
	session[school] = "true"

def schoolIsIn(school):
	if school in session:
		return True
	else:
		return False

def schoolLogOut(school):
	session.pop(school, None)

#random functions
def encrypt(string):
	return hashlib.sha512(string).hexdigest()

def getCSV(a):
	return getAllZones(a)

#api routes
@app.route('/api/getzones', methods=['GET', 'POST'])
def getzonesfunc():
	if adminIsIn():
		if request.method == "GET":
			return json.dumps(getZones(request.args['school']))
		if request.method == "POST":
			school = request.form['school']
			if howManyZones(school) == 1:
				return "false"
			zone = request.form['zone']
			table = school + zone
			deleteTable(table)
			deleteTableEntry(school, table)
			x = 0
			for i in getZones(school):
				t = i['zone']
				n = school + chr(ord('a') + x)
				renameTable(t, n)
				renameTableEntry(school, t, n)
				x += 1
			return "true"
	else:
		return "false"

@app.route('/api/modifyteacher', methods=['GET', 'POST'])
def modifyteachfunc():
	if adminIsIn():
		if request.method == "GET":
			zone = request.args['zone']
			teacher = request.args['teacher']
			return json.dumps(getSpecificTeacher(zone,teacher))
		if request.method == "POST":
			name = request.form['name']
			teacher = request.form['teacher']
			zone = request.form['zone']
			updateTeacherName(zone, name, teacher)
			return "true"
	else:
		return "false"

@app.route('/api/getteachers', methods=['GET', 'POST'])
def getteachersfunc():
	if adminIsIn():
		if request.method == "GET":
			return json.dumps(getTeachers(request.args['zone']))
		if request.method == "POST":
			teacher = request.form['teacher']
			zone = request.form['zone']
			if getZoneLength(zone) == 1:
				return "false"
			deleteTeacher(zone, teacher)
			return "true"
	else:
		return "false"

#routes
@app.route('/')
def index():
	vals = []
	for i in getSchoolNames():
		name = i['name']
		ident = i['ident']
		theId = i['id']
		x = 0.0
		tot = 0.0
		for i in getSchoolPercent(str(i['id'])):
			tot += len(getPercentFromZone(i['zone']))
			for a in getPercentFromZone(i['zone']):
				x += int(a['value'])
		vals.append([name, ident, str(int(math.ceil((x/tot) * 100))), theId])
	return render_template("home.html", vals=vals)

#admin panel routers
@app.route('/admin')
def loginfunc():
	if adminIsIn():
		return render_template("admin.html")
	else:
		return redirect("/adminlogin")

@app.route('/download')
def downloadfunc():
	if adminIsIn():
		c = getCSV(request.args['school'])
		response = make_response(c)
		response.headers["Content-Disposition"] = "attachment; filename=log.csv"
		return response
	else:
		return redirect("/adminlogin")

@app.route('/admin/stats')
def statsfunc():
	if adminIsIn():
		return render_template("stats.html", schools=getSchoolInfo())
	else:
		return redirect("/adminlogin")

@app.route('/admin/deleteschool', methods=['GET', 'POST'])
def deleteschoolfunc():
	if adminIsIn():
		if request.method == "GET":
			return render_template("deleteschool.html", schools=getSchoolInfo())
		if request.method == "POST":
			school = request.form['school']
			if getNumberOfSchools() <= 1:
				r = getSchoolInfo()
				r[0]['status'] = "falsef"
				return json.dumps(r)
			for i in getZones(school):
				deleteZoneTable(i['zone'])
			deletePassword(school)
			deleteSchoolZone(school)
			deleteSchoolfromSchool(school)
			r = getSchoolInfo()
			r[0]['status'] = "true"
			return json.dumps(r)
	else:
		return redirect("/adminlogin")

@app.route('/admin/deletezone')
def deletezonefunc():
	if adminIsIn():
		return render_template("deletezone.html", schools=getSchoolInfo())
	else:
		return redirect("/adminlogin")

@app.route('/admin/deleteteacher')
def deleteteacherfunc():
	if adminIsIn():
		return render_template("deleteteacher.html", schools=getSchoolInfo())
	else:
		return redirect("/adminlogin")

@app.route('/admin/modifyteacher')
def modifyteacherfunc():
	if adminIsIn():
		return render_template("modifyteacher.html", schools=getSchoolInfo())
	else:
		return redirect("/adminlogin")

@app.route('/admin/addteacher', methods=["GET", "POST"])
def addteacherfunc():
	if adminIsIn():
		if request.method == "GET":
			return render_template("addteacher.html", schools=getSchoolInfo())
		if request.method == "POST":
			name = request.form['name']
			zone = request.form['zone']
			addTeacher(zone, name)
			return "true"
	else:
		return redirect("/adminlogin")

@app.route('/admin/addschool', methods=["GET", "POST"])
def addschoolfunc():
	if adminIsIn():
		if request.method == "GET":
			return render_template("addschool.html")
		if request.method == "POST":
			return "true"
	else:
		return redirect("/adminlogin")

@app.route('/admin/addzone', methods=['GET', 'POST'])
def addzonefunc():
	if adminIsIn():
		if request.method == "GET":
			return render_template("addzone.html", schools=getSchoolInfo())
		if request.method == "POST":
			teachers = json.loads(request.form['teachers'])
			school = request.form['school']
			nz = chr(ord(getNewestZone(school)) + 1)
			addZone(school, nz)
			addZoneTable(school, nz)
			for i in teachers:
				last = i['last'].capitalize()
				first = i['first'].capitalize()
				room = i['room'].capitalize()
				addToZone(last + ", " + first + " - " + room, school + nz)
			return "true"
	else:
		return redirect("/adminlogin")

@app.route('/api/addteacher', methods=['POST'])
def apiaddteacherfunc():
	if adminIsIn():
		if request.method == "POST":
			teachers = json.loads(request.form['teachers'])
			newId = getNewestId()
			name = request.form['name']
			ident = request.form['school']
			password = request.form['password']
			for ide in getIdents():
				if ide['ident'] == ident:
					return "used"
			addNewPassword(newId, password)
			createNewSchool(name, ident, newId)
			school = str(getIdFromIdent(ident)[0]['id'])
			createTableTable(school)
			nz = chr(ord(getNewestZone(school)) + 1)
			addZone(school, nz)
			addZoneTable(school, nz)
			for i in teachers:
				last = i['last'].capitalize()
				first = i['first'].capitalize()
				room = i['room'].capitalize()
				addToZone(last + ", " + first + " - " + room, school + nz)
			"""
			global groups
			groups = {}
			for i in getIdList():
				groups.update({i['id']:[]})
			"""
			global groups
			groups.update({newId:[]})
			return "true"
	else:
		return redirect("/adminlogin")

@app.route('/admin/stats/school')
def stattablefunc():
	if adminIsIn():
		school = request.args['i']
		tables = []
		for n in getZones(school):
			a = getTeachers(n['zone'])
			a[0]['zone'] = n['zone'][len(n['zone']) - 1]
			tables.append(a)
		return render_template("stattable.html", schools=getSchoolInfo(), name=schoolNameFromId(school), zones=getZones(school), tables=tables, i=request.args['i'])
	else:
		return redirect("/adminlogin")

@app.route('/admin/management', methods=['GET', 'POST'])
def managementfunc():
	if adminIsIn():
		if request.method == "GET":
			return render_template("management.html", schools=getSchoolInfo())
		if request.method == "POST":
			vals = request.form
			if vals['school'] == "admin":
				updateAdminPassword(vals['password'])
				return render_template("management.html", schools=getSchoolInfo(), up=True)
			updatePassword(vals['password'], vals['school'])
			return render_template("management.html", schools=getSchoolInfo(), up=True)
	else:
		return redirect("/adminlogin")

@app.route('/logout')
def logoutfunc():
	i = request.args['i']
	if i == "admin":
		adminLogout()
	else:
		try:
			schoolLogOut(i)
		except:
			return redirect("/")
	return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def admin():
	if request.method == "GET":
		school = request.args['school']
		if schoolIsIn(school):
			return redirect("/school/" + getIdent(school))
		else:
			boo = False
			for i in getIdList():
				if str(i['id']) == school:
					boo = True
			if not boo:
				return redirect("/")
			else:
				return render_template("login.html", school=school)
	if request.method == "POST":
		if encrypt(request.form['password']) == str(getPasswords(request.form['school'])):
			schoolLogin(request.form['school'])
			return redirect("/school/" + str(getIdent(request.form['school'])))
		else:
			return render_template("incorrect.html")

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminloginfunc():
	if request.method == "GET":
		if adminIsIn():
			return redirect("/admin")
		else:
			return render_template("adminlogin.html")
	if request.method == "POST":
		password = request.form['password']
		if encrypt(password) == getAdminPassword():
			adminLogin()
			return redirect("/admin")
		else:
			return render_template("incorrect.html")

@app.route('/school/<school>')
def schoolfunc(school):
	schools = getSchools()
	boo = False
	for i in schools:
		if i["ident"] == school:
			boo = True
	if not boo: #tests if school exists
		return "this school does not exist"
	else:
		if schoolIsIn(str(getI(school))):
			i = str(getId(school)) #id of school
			zones = [] #list of zones for the school
			for a in getZones(i):
				zones.append(str(a['zone']))
			full = [] #array for all the zones
			for i in zones:
				az = getTeachers(i) #gets teachers for that zone
				a = sorted(az, key = lambda user: (user['name'])) #sorts it
				a[0]["zone"] = i[1] #adds zone name
				full.append(a)
			length = len(full)
			name = getSchoolName(school)
			test = []
			for z in getZones(str(getSchoolId(school))):
				test.append(getPercent(str(getSchoolId(school)), z["zone"][len(z['zone']) - 1]))
			inc = 0
			while inc < len(test):
				full[inc][0]['percent'] = test[inc]
				inc += 1
			return render_template("index.html", full=full, zones=zones, length=length, name=name, i=str(getSchoolId(school)))
		else:
			return redirect("/")

#these are rest apis for an app that i am testing out
#they can be deleted and the website will still work fine

def apiGetSchoolList():
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select * from schools"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getSchoolZones(school):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select zone from " + school + "zone"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getZoneFromSchool(zone):
	con = mdb.connect('localhost', 'root', 'visibilitymatters', 'multifire')
	query = "select * from " + zone
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

@app.route("/ionic/api/getschoollist")
def ionicgetschoollist():
	return json.dumps(apiGetSchoolList())

@app.route("/ionic/api/getschool")
def ionicapigetschool():
	i = request.args['id']
	zones = getSchoolZones(i)
	info = []
	for j in zones:
		info.append({"name": j['zone'][len(j['zone']) - 1].upper(), "teachers" : getZoneFromSchool(j['zone'])})
	return json.dumps(info)








#end of the rest apis part
###################################################

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTDALKSFJLDSKJFKLSDJF'

import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback,IOLoop
import tornado.wsgi
import sockjs.tornado




class ChatConnection(sockjs.tornado.SockJSConnection): #ebsocket tornado class
    school = 0
    def on_open(self, info):
        self.school = int(info.get_argument('school'))
        groups[self.school].append(self)
    def on_message(self, message):
		val = 0
		if (json.loads(message)['data'] == "true"):
			val = 1
		updateTeacherStatus(str(self.school), str(val), json.loads(message)['to'][1:], json.loads(message)['to'][0])
		updated = json.loads(message)
		updated['percent'] = str(getPercent(str(self.school), str(json.loads(message)['to'][0])))
		self.broadcast(groups[self.school], json.dumps(updated))
    def on_close(self):
        groups[self.school].remove(self)

wsgi_app=tornado.wsgi.WSGIContainer(app)
ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat') #class for websocket
application=tornado.web.Application(
	ChatRouter.urls +
	[(r'.*',tornado.web.FallbackHandler,{'fallback':wsgi_app })]
	)

application.listen(80)
IOLoop.instance().start()