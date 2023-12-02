from TestMgrBase import TestMgrBase
import requests
import json
import os

SERVER = "http://localhost"
LOGIN_ENDPOINT = SERVER + "/login.php"
RECEIPT_UPOAD_ENDPOINT = SERVER + "/receipt_upload.php"
TRANSACTION_ENDPOINT = SERVER + "/transactions.php"
USERNAME = "Roasted715Jr"
PASSWORD = "password"

class ReceiptsTestMgr(TestMgrBase):
	def setup(self):
		self.tester_name = "ReceiptsTestMgr"

		#Create a session to store all of our cookies
		self.s = requests.Session()
		r = self.s.post(LOGIN_ENDPOINT, data={"user": USERNAME, "password": PASSWORD, "remember": "false"})

		if (r.status_code != 200):
			return False

		#Create a new transaction to test the receipts on
		r = self.s.post(TRANSACTION_ENDPOINT, json={
			"transaction_name": "Receipt Test",
			"transaction_date": "2023-11-29",
			"transaction_description": "Transaction to test receipt uploads",
			"group_id": None,
			"transaction_participants": [
				{
					"user_id": 1,
					"amount": -100
				},
				{
					"user_id": 2,
					"amount": 100
				}
			]
		})

		if (r.status_code == 200):
			self.transaction_id = json.loads(r.text)["transaction_id"]
			return True

		return False

	#Test upload with no existing receipt
	def test_1_upload_receipt(self):
		receipt_path = os.path.dirname(os.path.abspath(__file__)) + "/Images/Normal_Receipt.jpg"
		r = self.s.post(RECEIPT_UPOAD_ENDPOINT, data={"transaction_id": self.transaction_id}, files={"receipt": open(receipt_path, "rb")})

		if (r.status_code != 200):
			print(json.loads(r.text)["message"])
			return False
		
		return True
 
	#Test replacing receipt
	def test_2_replace_receipt(self):
		#Perform the same test again since it's the same process
		return self.test_1_upload_receipt()

	#Test missing transaction_id
	def test_missing_transaction_id(self):
		receipt_path = os.path.dirname(os.path.abspath(__file__)) + "/Images/Normal_Receipt.jpg"
		r = self.s.post(RECEIPT_UPOAD_ENDPOINT, files={"receipt": open(receipt_path, "rb")})
		
		if (r.status_code != 400):
			print(json.loads(r.text)["message"])
			return False
		
		return True
 
	#Test missing image
	def test_missing_image(self):
		r = self.s.post(RECEIPT_UPOAD_ENDPOINT, data={"transaction_id": self.transaction_id})

		if (r.status_code != 400):
			print(json.loads(r.text)["message"])
			return False
		
		return True

	#Test wrong filetype
	def test_wrong_filetype(self):
		receipt_path = os.path.dirname(os.path.abspath(__file__)) + "/Images/Wrong_Filetype.ico"
		r = self.s.post(RECEIPT_UPOAD_ENDPOINT, data={"transaction_id": self.transaction_id}, files={"receipt": open(receipt_path, "rb")})

		if (r.status_code != 400):
			print(json.loads(r.text)["message"])
			return False
		
		return True

	#Test too big of an image
	# def test_large_file(self):
	# 	return False

	#Test rotated image (?)
	# def test_rotated_image(self):
	# 	return False
