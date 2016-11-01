import base64
import csv
import os

import pymysql.cursors

NAME = 'name'
LOAN_AMOUNT = 'loan_amount'
PROPERTY_VALUE = 'property_value'
SSN = 'ssn'
LOAN_ID = 'loan_id'
STATUS = 'status'

class Loan_validator(object):
	"""docstring for validator"""
	def calculate_loan_percentage(self,loan_amount, property_value):
		# calculating the percentage requested
		val = (float(loan_amount)/float(property_value))*100
		return val

	def loan_status(self,val):
		# rejected if percentage of loan requested is greater than 40%
		if val > 40:
			return False
		else:
			return True

	def data_to_csv(self,input_name, input_loan_amount, input_property_value, input_ssn,input_status):
		fieldnames = [ NAME, LOAN_AMOUNT, PROPERTY_VALUE, SSN, LOAN_ID, STATUS]
		#creating a csv file to write data
		if not os.path.isfile('data.csv'):
			with open('data.csv', 'w') as f:
				writer = csv.DictWriter(f, fieldnames=fieldnames)
				writer.writeheader()

		with open('data.csv','a') as f:
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			
			# Creating unique_id with ssn
			unique_id= base64.b64encode(input_ssn)

			writer.writerow({NAME : input_name, LOAN_AMOUNT : input_loan_amount,
				PROPERTY_VALUE : input_property_value, SSN : input_ssn,
				LOAN_ID : unique_id, STATUS : input_status})
			return unique_id


	def data_from_csv(self,loan_id):
		if not os.path.isfile('data.csv'):
			return 'Error: Please try again'
		#opening the file to retrieve data using id
		with open('data.csv', 'rb') as f:
			reader = csv.DictReader(f)
			for i in reader:
				if i['loan_id'] == loan_id:
					return i['status']
			return 'Error: Please check your loan id'

	def insert_data(self,input_name, input_loan_amount, input_property_value, input_ssn,input_status):

		# Creating unique_id with ssn
		unique_id= base64.b64encode(input_ssn)

		# Connect to the database
		connection = pymysql.connect(host='localhost',
							 user='root',
							 db='loanprocessdb',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)
		
		with connection.cursor() as cursor:
			# Create a new record
			sql = "INSERT INTO `enquiry` VALUES (%s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (input_name, input_loan_amount, input_property_value, input_ssn, unique_id, int(input_status)))
			connection.commit()
			connection.close()

		return unique_id

	def get_loan_data(self,loan_id):

		# Connect to the database
		connection = pymysql.connect(host='localhost',
							 user='root',
							 db='loanprocessdb',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

		with connection.cursor() as cursor:
			# Read a single record
			sql = "SELECT STATUS FROM `enquiry` WHERE `LOAN_ID`=%s"
			cursor.execute(sql, (loan_id))
			result = cursor.fetchone()
			connection.close()
			if result is not None:
				return result['STATUS']
			else:
				return 'Error: Please check your loan id'
		
