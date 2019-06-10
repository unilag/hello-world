import json
import datetime
import sys
import boto3
import time
import logging

#client = boto3.client('iam')

name='fake-user'
username='fake-user'
iam = boto3.resource('iam')
user = iam.User('name')


def lambda_handler(event, context):
	
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	
	
	
	

	
	print(username)
	
	#get_available_subresources()
	
	user_access_keys()
	#delete_login_profile(username)
	#delete_user(username)
	
	#get_user(username)
	

#def delete_user(username):
	
#	delete_response = client.delete_user(
#    UserName=username)
    
#def delete_login_profile(username):
#	response_delete_login_profile = client.delete_login_profile(
#    	UserName=username
#    )
    
#	print(response_delete_login_profile)
	
	
	#delete_response = user.delete(username= attribute-tes)
	
	#print(delete_response)
	
	
#def get_user(username):
#	get_user_response = client.get_user(
#    	UserName=username
#	)
	
#	print(get_user_response)
	
#def get_available_subresources():
#	user_sub_resources = user.get_available_subresources( )

#	print (user_sub_resources)

def user_access_keys():
	access_key_iterator = user.access_keys.all()
	
	print(access_key_iterator)
