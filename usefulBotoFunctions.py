import boto3
import time
import os
import configparser
import sys
import json
from datetime import datetime


def createSandboxClient(user):
	"""
	Generates a sandbox client for a given username. username must be present inside config file
	:param user: name of user for which you would like to create a client. Usernames are listed at the head of each block in the config file
	:return: Boto3 mturk client object. The client contains all credential information for a user. Use it for everything when working with mturk api
	"""
	config = configparser.ConfigParser()
	config.read('config.ini')
	region_name = 'us-east-1'
	endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	client =  boto3.client('mturk',
		endpoint_url = endpoint_url,
		region_name = region_name,
		aws_access_key_id = config[user]['awskey'], ## Put AWS Access keys in Config File
		aws_secret_access_key = config[user]['awssakey'],
	)
	return client

def createRealClient(user):
	"""
	Generates a production client for a given username. username must be present inside config file
	:param user: Username to create a production client. Username stored at head of each block in config file
	:return: Boto3 mturk client object
	"""
	config = configparser.ConfigParser()
	config.read('config.ini')
	region_name = 'us-east-1'
	endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
	client =  boto3.client('mturk',
		endpoint_url = endpoint_url,
		region_name = region_name,
		aws_access_key_id = config[user]['awskey'], ## Put AWS Access keys in Config File
		aws_secret_access_key = config[user]['awssakey'],
	)
	return client


def deleteSandbox(user) :
	"""
	Delete all hits inside a user's sandbox
	:param user: username of sandbox to delete
	:return: no return. deletes all hits inside this user's sandbox.
	username is passed in instead of client object to ensure this method will only ever empty sandboxes and not real data from production servers
	"""

	client = createSandboxClient(user)
	allHits = client.list_hits(MaxResults=100)['HITs']
	print(len(allHits))
	print(allHits)
	while len(allHits) == 100:
		print('Going through iteration')
		revHits = client.list_reviewable_hits(MaxResults=100)
		revHits = revHits['HITs']
		approveHitArr(client, revHits)
		for hit in allHits:
			hid = hit['HITId']
			client.update_expiration_for_hit(ExpireAt = datetime(2015, 1,1), HITId = hid)
			client.delete_hit(HITId = hid)
		allHits = client.list_hits()
		allHits = allHits['HITs']
		print(len(allHits))

def checkStatus(client, a):
	"""
	:param client: Mturk client
	:param a: the assignment ID
	:return: the status, submitted, approved, or rejected
	"""
	response = client.get_assignment(
		AssignmentId= a,
	)
	return response['Assignment']['AssignmentStatus']


def approveAllHits(client):
	"""
	Approves all hits associated with this client
	:param client: name of client for which to approve all hits
	:return: none
	"""
	allHits = client.list_reviewable_hits()
	allHits = allHits['HITs']
	approveHitArr(client, allHits)

def approveHitArr(client, har):
	"""
	Approves a list of hits
	:param client: client with home the hits are associated
	:param har: array of hit objects. Retrievable by using get_hit(), list_reviewable_hits(), etc Note: not an array of hit-id strings
	:return: Approves all assignments for hits in hit arr
	"""
	count = 0
	for hit in har:
		if (hit == "NextToken"):
			continue
		h = hit['HIT']['HITId']
		assignments = client.list_assignments_for_hit(HITId=h)['Assignments']
		for a in assignments:
			try:
				client.approve_assignment(
					AssignmentId=a['AssignmentId'],
					RequesterFeedback='Thank you!'
				)
				print(str(count) + " AssignmentID: " + a['AssignmentId']  + "HITId: "  + h + " Approved (from approveHitArr")
			except:
				print(str(count) + " approving failed")
			count = count + 1

def approveAssignments(client, aID):
	"""
	 Approve an array of assignments, identified by assignment-id strings stored in aID
	:param client: client which assignments are associated with
	:param aID: string array of assignment ids
	:return: none. approves assignments (or prints approving failed if not)
	"""
	count = 0
	for a in aID:
		response = client.get_assignment(AssignmentId=a)
		if response['Assignment']['AssignmentStatus']  == 'Submitted': # if not yet evaluated
			print('Approving' + str(a))
			client.approve_assignment(
				AssignmentId = a,
				RequesterFeedback='Thank you!'
			)
			count += 1
			print(str(count) + " AssignmentID: " + a  + " approved from approveAssignments")
		else:
			print("AssignmentID " + a + " has already been evaluated.")


def rejectAssignments(client, aID):
	"""
	Reject an array of assignments, identified by assignment-id strings stored in aID
	:param client: client which assignments are associated with
	:param aID: string array of assignment ids
	:return: none. rejects assignemnts (or prints rejection failed if not)
	"""
	count = 0
	for a in aID:
		response = client.get_assignment(AssignmentId=a)
		if response['Assignment']['AssignmentStatus']  == 'Submitted':
			print('Rejecting ' + str(a))
			client.reject_assignment(
				AssignmentId = a,
				RequesterFeedback = 'Sorry, your annotations look incomplete!'
			)
			count += 1
			print(str(count) + " AssignmentID: " + a + " rejected from approveAssignments")
		else:
			print("AssignmentID " + a + " has already been evaluated.")


