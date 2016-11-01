from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from lending import Loan_validator


 
# App config. 
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d011f27567d441f2b6132a'
 

class ProcessLoanForm(Form):
	name = TextField('Name', validators=[validators.required()])
	loan = TextField('Loan Amount', validators=[validators.required(), validators.Length(min=1, max=10)])
	p_value = TextField('Property Value', validators=[validators.required(), validators.Length(min=1, max=10)])
	fieldSsn = TextField('SSN', validators=[validators.required(), validators.Length(min=8, max=8)])


class CheckStatusForm(Form):
	loan_id = TextField('Loan ID:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def process_loan():
	form = ProcessLoanForm(request.form)
	
	if request.method == 'POST':
		name=request.form['name']
		loan=request.form['loan']
		p_value=request.form['p_value']
		fieldSsn=request.form['fieldSsn']
	#validating Form
		if form.validate():
			# calling class
			valid = Loan_validator()
			#calculating percentage of loan requested
			val = valid.calculate_loan_percentage(loan, p_value)
			result = valid.loan_status(val)
			if result:
				flash('Your loan application is accepted')
			else:
				flash('Error: Your loan application is denied')
			#saving in csv file for reference	
			loan_id = valid.insert_data(name, loan, p_value, fieldSsn, result)
			flash('Your Loan ID is generated for future references: %s' %loan_id)
		else:
			flash('Error: All the form fields are required. ')		

	return render_template('index.html', form=form)


@app.route("/checkstatus", methods=['GET', 'POST'])
def check_status():
	form = CheckStatusForm(request.form)
	
	if request.method == 'POST':
		loan_id=request.form['loan_id']
		if form.validate():
			# calling class
			valid = Loan_validator()
			# get data from csv
			data = valid.get_loan_data(loan_id)
			
			if data == 1:
				flash("Your application has been succesfully Accepted")
			elif data == 0:
				flash("Your application has been Rejected")
			else:
				flash(data)
		else:
			flash('Error: All the form fields are required. ')

	return render_template('checkstatus.html', form=form)


if __name__ == '__main__':
	app.run(host='0.0.0.0')
