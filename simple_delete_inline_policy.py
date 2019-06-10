import json
import datetime
import sys
import boto3
import time
import logging
import os

iam = boto3.client('iam')

def lambda_handler(event, context):
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    username=event['keys'][0]['username']
    print(username)
    #print(type(username))
    #logs_bucket = os.environ['LOGS_BUCKET']
    
    #delete_inline_policy_log=""
    
    #delete_inline_policy_log=delete_inline_policy_log + delete_all_inline_policies(username)

    #logic that constructs revert_log
    
    delete_all_inline_policies(username)
    
   # revert_log="{\n \"revert_metadata\": [\n" + delete_inline_policy_log[:-2] + " \n     ]\n }\n"

    #log Revert Log
   # logger.info("Inline user policy " + policyname + " for user " + username + " was deleted by the IR team: \n" + revert_log)

    #Save revert_log to file
   # revert_log_file=save_revert_log_file(revert_log)

    #Save revert_log to S3
   # upload_to_s3(revert_log_file,logs_bucket)

   # return


#def delete_inline_policy(username,policy):
    


    #delete_inline_policy_log="{\n        \"type\": \"delete_inline_policy\",\n      \"username\": \"" + username + "\",\n       \"policyname\": \"" + policyname + "\"\n      },\n"
    #return delete_inline_policy_log

def delete_all_inline_policies(username):

    print("Delete all inline polices for " + username)

    #list inline policies for user
    response = iam.list_user_policies(
        UserName=username
    )
    print(response)

    #delete policy
    delete_inline_policy_log=""
    for PolicyNames in response:
        for policyname in response['PolicyNames']:
            #delete_inline_policy_log= delete_inline_policy_log + delete_inline_policy(username,str(response['PolicyNames']))
            print(policyname)
            
            
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
    
            print("Delete " + policyname + " for user " + username)
  
            delete_policy_response = iam.delete_user_policy(
                UserName=username,
                PolicyName=policyname
            )
            #return delete_inline_policy_log

def upload_to_s3(file_name,logs_bucket):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file("/tmp/" + file_name,logs_bucket,"socir_disable_access_PolicyNames_logs/"+ file_name)

def save_revert_log_file(revert_log):
    revert_log_file="revert_log" + '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()) + ".json"
    with open("/tmp/" + revert_log_file, mode='w+') as file:
        file.write(revert_log)
        file.closed
    return revert_log_file
    
