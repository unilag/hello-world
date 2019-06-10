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
    
    #detach_managed_policy_log=""
    
    #detach_managed_policy_log=detach_managed_policy_log + detach_all_managed_policies(username)

    #logic that constructs revert_log
    
    detach_all_managed_policies(username)
    
   # revert_log="{\n \"revert_metadata\": [\n" + detach_managed_policy_log[:-2] + " \n     ]\n }\n"

    #log Revert Log
   # logger.info("managed user policy " + policyarn + " for user " + username + " was detachd by the IR team: \n" + revert_log)

    #Save revert_log to file
   # revert_log_file=save_revert_log_file(revert_log)

    #Save revert_log to S3
   # upload_to_s3(revert_log_file,logs_bucket)

   # return


#def detach_managed_policy(username,policy):
    


    #detach_managed_policy_log="{\n        \"type\": \"detach_managed_policy\",\n      \"username\": \"" + username + "\",\n       \"policyarn\": \"" + policyarn + "\"\n      },\n"
    #return detach_managed_policy_log

def detach_all_managed_policies(username):

    #print("detach all managed polices for " + username)

    #list managed policies for user
    #response = iam.list_user_policies(
    #    UserName=username
    #)
    

    #List all managed policies that are attached to the specified IAM user
    response = iam.list_attached_user_policies(
        UserName=username
    )
    print(response)

    #detach policy
    detach_managed_policy_log=""
    for policies in response['AttachedPolicies']:
        policyarn=policies['PolicyArn']
            
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    
        print("detach " + policyarn + " for user " + username)
  
        detach_policy_response = iam.detach_user_policy(
            UserName=username,
            PolicyArn=policyarn
        )
            #return detach_managed_policy_log

def upload_to_s3(file_name,logs_bucket):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file("/tmp/" + file_name,logs_bucket,"socir_disable_access_policyarns_logs/"+ file_name)

def save_revert_log_file(revert_log):
    revert_log_file="revert_log" + '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()) + ".json"
    with open("/tmp/" + revert_log_file, mode='w+') as file:
        file.write(revert_log)
        file.closed
    return revert_log_file
    
