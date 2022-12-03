import sqlite3
from sqlite3 import Error
from lxml import etree
from flask import Flask, request, make_response, abort, g, render_template_string, escape
import random, string
from Cryptodome import Random
from Cryptodome.Cipher import AES
from base64 import b64decode,b64encode
from binascii import hexlify, unhexlify
import hashlib
import uuid
import os
import discardthesefiles.env_init


app = Flask(__name__)

# Super important configuration
APP_NAME = 'Server 1.'
APP_VERSION = "1.0"
APP_WEBSITE = ""
APP_DESCRIPTION = "SWISS TOOL"
APP_ADMIN_TMP_PASSWORD = uuid.uuid4()
KEY = Random.new().read(32)
SECRET = Random.new().read(32)
BLOCKSIZE = AES.block_size


CFG = {
	'crypto_key': b64encode(KEY),
	'secret_val': b64encode(SECRET),
	'application_name': APP_NAME,
	'application_version': APP_VERSION,
	'application_site': APP_WEBSITE,
	'application_description': APP_DESCRIPTION,
	os.environ.get('SECRET_KEY'): os.environ.get('SMCP98')
}



def check_user_permissions():
	if request.cookies.get('user_session_cookie') is None:
		return False
	else:
		cookie_value = request.cookies.get('user_session_cookie').split(".")[1]
		if hashlib.md5(str(cookie_value).encode('utf-8')).hexdigest() == "28c8edde3d61a0411511d3b1866f0636":
			return True

	return False


@app.before_request
def before_request():
	g.conn = create_conn()
	if g.conn is None:
		abort(500, description="Problem connecting to database")


def create_conn():
	conn = None
	try:
		conn = sqlite3.connect('discardthesefiles/db.sqlite')
	except Error as e:
		print(e)

	return conn

def user_login(username, password):
	SQL_QUERY = "SELECT * FROM users WHERE username Like ? AND password LIKE ?;"
	cursor = g.conn.cursor()
	cursor.execute(SQL_QUERY, (username, hashlib.md5(str(password).encode('utf-8')).hexdigest()))
	row = cursor.fetchone()

	if row is not None:
		role = row[4]
		if role == 'admin':
			return (True,1)
		else:
			return (True,2)
	return False



@app.route('/admin', methods = ["POST", "GET"])
def admin_dashboard():
	if check_user_permissions() == True:
		return "<h1> Welcome Admin </h1>"
	return "<h1> You don't have permissions to view this area </h1>"


@app.route('/login', methods = ["POST", "GET"])
def login():
	if request.method == "POST":
		username = request.values.get('username')
		password = request.values.get('password')
		ul = user_login(username, password)
		if ul == False:
			return """
				<h1> Wrong username or password </h1>
			"""
		else:
			response = make_response(render_template_string("<h1>Hello logged in user!</h1>"))
			string_1 = hashlib.md5(Random.new().read(32)).hexdigest()
			string_2 = hashlib.md5(str(ul[1]).encode('utf-8')).hexdigest()
			string_3 = hashlib.md5(Random.new().read(32)).hexdigest()
			final = str(string_1) + "." + str(string_2) + "." + str(string_3)
			response.set_cookie('user_session_cookie', final)
			return response

	else:
		return """
			<html>
				<body>
					<form action='/login' method='post'>
						Username <input type='text' name='username' /><br />
						Password <input type='password' name='password' /><br />
						<input type='submit' />
					</form>
				</body>
			</html>
		"""

@app.route('/', methods = ['POST', 'GET'])
def home():
	return """
		<html>
			<body>
				<h1> Hello ! </h1>
				<a href="/admin"> Admin dashboard </a><br />
				<a href="/login"> Login </a><br />
				<a href="/cfg"> Config viewer </a><br />
			</body>
		</html>
	"""

def u_p(value, bs=BLOCKSIZE):
    pv = value[-1]
    if pv > bs:
        raise Exception('Bad padding')
    padding = value[-pv:]
    if len(padding) != pv or len(set([a for a in padding])) != 1:
        raise Exception('Bad padding')
    return value[:-pv]


def p(value, bs=BLOCKSIZE):
    pv = bs - (len(value) % bs)
    return value + (chr(pv) * pv).encode()


def encrypt(value, key):
    iv = Random.new().read(BLOCKSIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_value = p(value)
    return iv + cipher.encrypt(padded_value)


def decrypt(value, key):
    iv = value[:BLOCKSIZE]
    decrypt_value = value[BLOCKSIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(decrypt_value)
    return u_p(decrypted)

@app.route('/cfg', methods = ['GET'])
def cfg():
    key = None
    config_out = None
    decrypted_key = None
    key = request.args.get('key')
    viewable = [a for a in CFG.keys() if a.startswith('application_')]
    crypt = lambda x : hexlify(encrypt(x.encode(), KEY)).decode('utf8')
    configs = '\n'.join(['<a href="/cfg?key=%s">%s</a><br>' %(crypt(a), a) for a in viewable])
    configs += '\n' + '<a href="/cfg?key=%s">%s</a><br>' %(crypt(CFG['secret_most_secret_password_98132y928hasdb21387gbasd123873g1bdashjaldb1231v23jbashdbab123j']),"No viewers here.")
    if key:
        try:
            s = key
            if all(c in string.hexdigits for c in s):
                kv = unhexlify(key)
                decrypted_key = decrypt(kv, KEY).decode('utf8')
            else:
                decrypted_key = s
        except Exception as e:
            return str(e)
        
        if decrypted_key and decrypted_key in CFG.keys():
            config_out = CFG[decrypted_key]
        else:
        	config_out = "????"

    return """
    <html>
      <body>
         <p><h4>Select one of the values to view it</h4></p>
        """ + configs + "\n" + """
        """ + ('\n<br><br>Loaded value: [<b>{}</b>: <b>' + config_out + '</b>]<br>\n' if decrypted_key or key else '') + """
      </body>
    </html>
    """.format(escape(key))

def run_app():
	print ('##################################################')
	print ('http://127.0.0.1:8888/')
	print ('##################################################')
	app.run("0.0.0.0", 8888)


run_app()