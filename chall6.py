from flask import Flask, session, redirect, url_for, escape, request, render_template_string

app = Flask(__name__)

def search_term(term):
	search_tags = ["twitter", "webpage", "inql", "electronegativity"]
	print(term)
	if any(st in term for st in search_tags):
		if "electronegativity" :
			return str(term) + ": https://github.com/doyensec/electronegativity"
		if "twitter" in term:
			return str(term) + ": https://twitter.com/doyensec"
		if "webpage" in term:
			return str(term) + ": https://www.doyensec.com/"
		if "inql" in term:
			return str(term) + ": https://github.com/doyensec/inql"


@app.route('/')
def index():
	search = request.args.get('search') or None
	print(search)
	if search is not None:
		result = search_term(search)
	else:
		result = None

	template = '''
		<h1>Search for Doyensec in media</h1>
		<p>Your search results:</p>
		{}
		'''.format(escape(result))

	return render_template_string(template)

@app.route('/doc')
def create_doc():
	template = '''  <h1>Create doc file</h1>
					<form method='post' name='f1' action='/view'>
						<textarea name='doc' rows='10' cols='40'></textarea>
						<br /><br />
						<input type='submit'/>
					</form>
				'''
	return render_template_string(template)
	
@app.route('/view',methods=['POST'])
def view_doc():
	doc_string = request.form.get('doc')
	template = '''
				<h1>Here is your doc!</h1>
				<br/>
				<div style='border: solid 1px; width:200px; height:500px;'>
					%s
				</div>''' % (doc_string)
	return template




print ('##################################################')
print ('http://127.0.0.1:8888/')
print ('##################################################')
app.run("0.0.0.0", 8888, app)
