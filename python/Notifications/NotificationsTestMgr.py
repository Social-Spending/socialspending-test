from TestMgrBase import TestMgrBase
import requests
import json

SERVER = "http://localhost"
LOGIN_ENDPOINT = SERVER + "/login.php"
NOTIFICATIONS_ENDPOINT = SERVER + "/notifications.php"
USERNAME = "Roasted715Jr"
PASSWORD = "password"

class NotificationsTestMgr(TestMgrBase):
	def setup(self):
		self.tester_name = "NotificationsTestMgr"
		#Create a session to store all of our cookies
		self.s = requests.Session()
		return True
	
	def test_stub1(self):
		print("Fetching notifications without loggin in")
		r = self.s.get(NOTIFICATIONS_ENDPOINT)
		return r.status_code == 401
	
	def test_stub1(self):
		print("Logging In")
		r = self.s.post(LOGIN_ENDPOINT, data={"user": USERNAME, "password": PASSWORD, "remember": "false"})
		return r.status_code == 200

	def test_stub2(self):
		passed = True
		self.notification_ids = []
		notification_types = ["friend_requests", "transaction_approvals", "completed_transactions", "group_invites"]

		print("Fetching notifications")
		r = self.s.get(NOTIFICATIONS_ENDPOINT)
		if (r.status_code != 200):
			print("Request did not respond with 200")
			return False

		data = json.loads(r.text)

		for notification_type in notification_types:
			#Make sure all the notification types are returned
			if notification_type not in data:
				print(notification_type + " not found")
				passed = False
				continue
			else:
				#Keep track of the user's notifications for later
				for notification in data[notification_type]:
					self.notification_ids.append(notification["notification_id"])

		return passed

	def test_stub3(self):
		print("Performing POST with no notification_id")
		r = self.s.post(NOTIFICATIONS_ENDPOINT, json={"operation": "dismiss"})
		return r.status_code == 400

	def test_stub4(self):
		print("Performing POST with no operation")
		r = self.s.post(NOTIFICATIONS_ENDPOINT, json={"transaction_id": 1})
		return r.status_code == 400

	def test_stub5(self):
		print("Performing POST with invalid operation")
		r = self.s.post(NOTIFICATIONS_ENDPOINT, json={"operation": "test", "transaction_id": 1})
		return r.status_code == 400

	def test_stub6(self):
		i = 1
		while i in self.notification_ids:
			i += 1

		print(f"Dismissing a notification that user does not have access to (id {i})")
		r = self.s.post(NOTIFICATIONS_ENDPOINT, json={"operation": "dismiss", "notification_id": i})
		return r.status_code == 404

	#*******************Verification that the notification was removed should be done*****************
	def test_stub7(self):
		#Make sure the user has a notification to dismiss
		if (len(self.notification_ids) == 0):
			print("No notifications for user, unable to test")
			return False

		#Dismiss the first notification in the list
		print(f"Dismissing notification (id {self.notification_ids[0]})")
		r = self.s.post(NOTIFICATIONS_ENDPOINT, json={"operation": "dismiss", "notification_id": self.notification_ids[0]})
		return r.status_code == 200
