"""course		name						hours	sections...		CRN	  seatstaken/total	teach			
['ACCT115', 'FUND OF FINANCIAL ACCOUNTING', 3, ['ACCT115', '002', 10001, '23 \\/ 39', 'Gomez, Steven', 0, 0, '', 'FUND OF FINANCIAL ACCOUNTING', [[3, 52200, 57000, 'KUPF 104'], [5, 52200, 57000, 'KUPF 104']]], ['ACCT115', '102', 10002, '12 \\/ 39', 'Taylor, Ming', 0, 0, '', 'FUND OF FINANCIAL ACCOUNTING', [[2, 64800, 75000, 'KUPF 105']]], ['ACCT115', '104', 10003, '15 \\/ 39', 'Gomez, Steven', 0, 0, '', 'FUND OF FINANCIAL ACCOUNTING', [[5, 64800, 75000, 'TIER 105']]]]
"""
import requests
import json
import re
from datetime import datetime
import time
import smtplib # Import smtplib for the actual sending function
from email.parser import Parser

global mySections, seatsOpen, COURSELIST, count, EMAIL
EMAIL = ""

def isOpen(string):
	global mySections, seatsOpen
	capture = re.search("(\\d*) \\\\/ (\\d*)", string)
	seatsTaken = capture[1]
	seatsAvail = capture[2]
	seatsOpen = int(seatsAvail) - int(seatsTaken)

	if seatsOpen > 0:
		return True
	return False

def printInfo(section):
	for i in range(0, len(section)):
		print(f"i:{i}, course:{section[i]}")

def getSections(course):
	sections = []
	for z in range(3, len(course)):#iterate through course sections
		section = course[z]
		sections.append(course[z][1])
	return sections

def emailMe(section):
	global mySections, seatsOpen, EMAIL
	print(f"Sending email about course {section[0]} section {section[1]}")
	FROM = "@gmail.com"
	PASSWORD = "" #gmail high security authentification needs to be off

	subject = f"{section[0]}, {section[1]} has {seatsOpen} seat open!"
	body = f"GO REGISTER NOW: http://myhub.njit.edu/StudentRegistrationSsb/ssb/registration/registration"

	message = f"Subject: {subject}\n\n {body}"
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.login(FROM, PASSWORD)
	                #(FROM, TO, MESSAGE)
	server.sendmail(FROM, EMAIL, message)
	server.quit()

def scrapeData():
	global mySections, COURSELIST
	print(f"Scraping latest data at " + datetime.now().strftime("%I:%M:%S %p"))
	req = requests.get(f'https://uisapppr3.njit.edu/scbldr/include/datasvc.php?p=/')
	# print(req.text)
	text = req.text[15:-53]

	null = None
	false = False
	COURSELIST = eval(text)

def chooseClasses():
	global mySections, COURSELIST
	mySections = {}
	picker = 1
	while picker:
		x = 1
		picker = input("Which course would you like? (ex: 'CS341') ")
		if picker != "":
			print(f"{picker} added")
			for course in COURSELIST:
				if course[0] == picker:
					mySections[picker] = []
					sections = getSections(course)
					while x:
						x = input(f"Which section would you like? {sections} ")
						if x != "" and x in sections:
							mySections[picker].append(x)
							sections.remove(x)
							print(f"{x} added")
	print(f"mySections: {mySections}")

def parseClasses():
	print("Parsing...")
	for course in COURSELIST:
		if course[0] in mySections.keys():
			for z in range(3, len(course)):#iterate through course sections
				section = course[z]
				# printInfo(section)
				if section[1] in mySections[course[0]]:
					if isOpen(section[3]):
						emailMe(section)
					# else:
					# 	print(f"No seats open for {section[0]} {section[1]}")

def main():
	count = 0
	minutes = 1
	scrapeData()
	chooseClasses()
	while True:
		count += 1
		print(f"Running iter: {count}")
		parseClasses()
		print(f"Waiting {minutes} minutes, then retry...")
		time.sleep(minutes*60) #wait 5 minutes, then do it AGAIN!
		scrapeData()

main()