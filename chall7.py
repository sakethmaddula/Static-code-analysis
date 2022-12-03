#!/usr/bin/env python
from base64 import b64decode,b64encode
import pickle
from flask import Flask, session, redirect, url_for, escape, request, render_template_string
from lxml import etree

app = Flask(__name__)

def safe_xml(xml):
    kp = ["CDATA", "data", "foo", "result", "soap", "svg"]
    if [element for element in kp if(element in kp)]:
        return False
    return xml


@app.route('/', methods=['GET'])
def index():
    template = """
        <html>
            <body>
                <form action = "/viewxml" method="POST">
                    <h1>Please provide xml to parse by app</h1>
                    <textarea name="xml" cols="41" rows="6"></textarea><br />
                    <input type="hidden" value="utf8" name="encoding" />
                    <input type="submit" value="ParseXMLv1.0"/><br />
                </form> 
            </body>
        </html>
    """
    return render_template_string(template)

@app.route('/viewxml', methods=['POST'])
def viewxml():
    xml = None
    if not request.method == 'POST':
        template = """
            <html>
                <body>
                    <a href="/">Go back</a>
                </body>
            </html> 
        """
        return render_template_string(template)
    else:
        if "sc21" not in request.cookies or request.cookies.get("sc21") is None:
            template = """
                <html>
                    <body>
                        Something went wrong, try again! <a href="/">Go back</a>
                    </body>
                </html>                 
            """
            return render_template_string(template)
        else:
            xml = request.form['xml']
            cv = pickle.loads(b64decode(request.cookies.get("sc21")))
            pxml = safe_xml(xml)
            par = etree.XMLParser(load_dtd=True,dtd_validation=False,no_network=False)
            try:
                document = etree.fromstring(pxml.encode(), par)
                pxml = etree.tostring(document).decode(request.form['encoding'])
            except:
                return render_template_string("ERROR parsing XML")
            template = """
                <html>
                    <body>
                        <a href="/">Go back</a><br /><br />
                        The cookie val was properly set<br />
                        Thank you for submiting the XML file!
                    </body>
                </html> 
            """
            return render_template_string(template)


print ('##################################################')
print ('http://127.0.0.1:8888/')
print ('##################################################')
app.run("0.0.0.0", 8888, app)
