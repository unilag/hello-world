import json
import datetime
import sys
import boto3
import time
import logging
import os


def lambda_handler(event, context):
	
	print(event)
	
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
    
	logs_bucket=os.environ['logs_bucket']
	
    disable_key_log=""
	
    if (username == event['username']):
        disable_key_log=disable_key_log + disable_all_keys(username)
        log_status(username)
    else:    
        
        for key in event['keys']:
		    keyid=key['KeyID']
		    username=key['username']
	
		
		    #check for wildcard
		    if keyid == "*":
			    disable_key_log=disable_key_log + disable_all_keys(username)
			    log_status(username)
		    else:
			    #create a function that obtains the username associated with a given keyid
			
			    disable_key_log=disable_key_log + disable_key(username,keyid)
			    log_status(username)
	
	#logic that constructs revert_log
	
	#remove the last charachter (,)
	
	revert_log="{\n \"revert_metadata\": [\n" + disable_key_log[:-2] + " \n 	]\n }\n"

	#Print Revert Log
	#print(revert_log)
	
	#log Revert Log
	logger.info("Access Key ID: " + keyid + " was disabled by IR team: \n" + revert_log)

    #Save revert_log to file
	revert_log_file=save_revert_log_file(revert_log)

    #Save revert_log to S3
	upload_to_s3(revert_log_file,logs_bucket)

	return

#def obtain_user(key):


#	return username

def disable_key(username,keyid):
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	
	print("Disable " + keyid + " owned by " + username)
	
	iam = boto3.client('iam')
	response = iam.update_access_key(
		UserName= username,
		AccessKeyId=keyid,
		Status='Inactive'
	)
	
	disable_key_log="{\n 		\"type\": \"disable_accesskey\",\n		\"username\": \"" + username + "\",\n		\"keyid\": \"" + keyid + "\"\n		},\n"
	return disable_key_log
	
def disable_all_keys(username):

	print("Disable all keys for " + username)
	
	iam = boto3.client('iam')
	response = iam.list_access_keys(UserName= username)
	#disable keys
	disable_key_log=""
	for key in response['AccessKeyMetadata']:
		disable_key_log= disablekey_log + disable_key(username,key['AccessKeyId'])
	
	return disable_key_log

def log_status(username):
	iam = boto3.client('iam')
	response = iam.list_access_keys(UserName= username)
	print("Status: \n" + str(response))
	
	
	return response

def upload_to_s3(file_name,logs_bucket):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file("/tmp/" + file_name,logs_bucket,"socir_disable_access_key_logs/"+ file_name)

def save_revert_log_file(revert_log):
    revert_log_file="revert_log" + '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()) + ".json"
    with open("/tmp/" + revert_log_file, mode='w+') as file:
        file.write(revert_log)
        file.closed
    return revert_log_file
	
