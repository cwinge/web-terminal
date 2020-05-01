from flask import Flask, render_template, request, redirect
import os, re, subprocess, time
from socket import socket
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
		redir = "http://127.0.0.1:{}".format(port)
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
	input += "curl -s -H \"Authorization: JWT ${{TOKEN}}\" \"https://hub.docker.com/v2/repositories/library/{}/tags/?page_size=100\" | jq -r \'.results[] | select(.name == \"latest\") | .images[0].size\'".format(field.data)
	stream = os.popen(input)
	output = stream.read()
	try:
		# If larger than 1GB, print error
		if (int(output) > 1000000000):
			raise ValidationError("Size must be smaller than {}".format(output))
	except ValueError:
		raise ValidationError("Invalid container name")
	
	

class ReusableForm(Form):
    # Enter name of docker image
    dname = TextField('Enter name of docker container (max 1GB in size):',
                         validators=[validators.InputRequired(), validate_size])
    # Submit button
    submit = SubmitField("Submit")



if __name__ == "__main__":
    # Run app
    app.run(host='0.0.0.0', port=8080)