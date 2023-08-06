
SMS Alert
==========

A simple python client for SMS Alert APIs.
To use this package, you must have a valid account on https://www.smsalert.co.in.

* Free software: ISC license

Features
--------

* Send sms to any mobile number using SMS Alert username, password, senderid, route.


Requirements
------------

* username : SMS Alert account username

* password : SMS Alert account password

* mobileno : Destination mobile number (Keep number in international format)

* message : Message Content to send

* senderid : Receiver will see this as sender's ID

* route : If your operator supports multiple routes then give one route name


How to use
----------

//import smsAlert.py where you want to send msg

	from smsAlert import smsAlertMsg

	class smsAlertMsg(unittest.TestCase):
   
    def setUp(self):
	username='' # add your SMS Alert username
        password='' # add your SMS Alert password
	
	self.client = smsAlertMsg(username=username,password=password)

    def tearDown(self):
        pass

    def test_send_sms(self):
        self.client.send_sms('918010551055','Test SMS','CVDEMO','demo') #(mobileno, message, senderid, route)
		
	if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())	


Credits
---------

This package was created with Cozy Vision Pvt. Ltd.
