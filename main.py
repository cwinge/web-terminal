from flask import Flask, render_template, request, redirect
import os, re, subprocess, time, sys
from socket import socket
from decimal import Decimal
from wtforms import Form, TextField, validators, SubmitField, ValidationError, SelectField

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
	form = ReusableForm(request.form)

	if request.method == 'POST' and form.validate():		
		port = ""
		with socket() as s:
			s.bind(('', 0))
			port = s.getsockname()[1]
		command = "timeout 3600s gotty -p {0} -w --close-timeout 10 --timeout 30 docker run -it --rm {1}".format(port, request.form['dname'])
		subprocess.Popen(command, close_fds=True, shell=True)
		redir = "http://{}:{}".format(app.config.get('ext_ip'), port)
		time.sleep(0.1)
		return redirect(redir, code=302)

	return render_template('index.html', form=form)

# Check docker size
def validate_size(form, field):
	if(field.data == "customenv"):
		return
	input = "export HUBUSER=webtermdemo &&"
	input += "export HUBPASS=webtermdemo &&"
	input += "export HUBTOKEN=$(curl -s -H \"Content-Type: application/json\" -X POST -d \'{\"username\": \"\'${HUBUSER}\'\", \"password\": \"\'${HUBPASS}\'\"}\' https://hub.docker.com/v2/users/login/ | jq -r .token) &&"
	if ":" in field.data and "/" in field.data:
		a = field.data.split("/")[0]
		b = field.data.split("/")[1].split(":")[0]
		c = field.data.split(":")[1]
		input += "curl -s -H \"Authorization: JWT ${{TOKEN}}\" \"https://hub.docker.com/v2/repositories/{}/{}/tags/?page_size=1000\" | jq -r \'.results[] | select(.name == \"{}\") | .images[0].size\'".format(a,b,c)
	elif "/" in field.data:
		a = field.data.split("/")[0]
		b = field.data.split("/")[1]
		input += "curl -s -H \"Authorization: JWT ${{TOKEN}}\" \"https://hub.docker.com/v2/repositories/{}/{}/tags/?page_size=100\" | jq -r \'.results[] | select(.name == \"latest\") | .images[0].size\'".format(a,b)
    elif ":" in field.data:
		a = field.data.split(":")[0]
		b = field.data.split(":")[1]
		input += "curl -s -H \"Authorization: JWT ${{TOKEN}}\" \"https://hub.docker.com/v2/repositories/library/{}/tags/?page_size=1000\" | jq -r \'.results[] | select(.name == \"{}\") | .images[0].size\'".format(a,b)
	else:
		input += "curl -s -H \"Authorization: JWT ${{TOKEN}}\" \"https://hub.docker.com/v2/repositories/library/{}/tags/?page_size=100\" | jq -r \'.results[] | select(.name == \"latest\") | .images[0].size\'".format(field.data)
	stream = os.popen(input)
	output = stream.read()
	try:
		output = int(output)
	except ValueError:
		raise ValidationError("Invalid container name")
	print(output)
	# If larger than 1GB, print error
	if (output > 1000000000):
		raise ValidationError("Container ize must be smaller than 1 GB, this is {} GB".format(round((output/1000000000),2)))
	
	
	

class ReusableForm(Form):
    # Enter name of docker image
    dname = TextField('Enter name of docker container (max 1GB in size):',
                         validators=[validators.InputRequired(), validate_size])
    # Submit button
    submit = SubmitField("Submit")



if __name__ == "__main__":
    # Run app
    app.config['ext_ip'] = sys.argv[1]
    app.run(debug='true', host='0.0.0.0', port=8080)
