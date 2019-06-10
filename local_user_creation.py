import boto3
import json
import os
import logging
import botocore.session
from botocore.exceptions import ClientError
from datetime import datetime
import pprint


# Defines Lambda function for automatically enabling AWS CloudTrail logs when it gets disabled
# and publish notification to SNS Topic on any changes to the AWS CloudTrail.

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#pp = pprint.PrettyPrinter(indent=4)


def lambda_handler(event, context):
    eventName = event['detail']['eventName']
    requestParameters = event['detail']['requestParameters']



# When an IAM user is created, the user attributes such as user policy,
# access key and eventually the user will be deleted.

    try:
        if (requestParameters == None):
            errorCode = event['detail']['errorCode']
            remediation_action = "Notification Only"
        else:
            if (eventName == 'CreateUser'):
                username = event['detail']['requestParameters']['userName']
                
             # invoke lambda for remediation action
                msg = { "keys": [ {"username": username , "KeyID":"*"}]}
                
                FunctionName='delete_access_key'
                InvocationType='Event'
                Payload=json.dumps(msg)
                  
                remediation_action = invoke_lambda(event,FunctionName,InvocationType, Payload)
               

                errorCode = "New user created"
               
                # For Other IAM user events such as deletion/update operations, updating
                #IAM user passwords or Access Keys, as well as attaching/detaching
                #policies from IAM users or groups, an SNS notification will be sent
                # to the Amazon SNS topic subscribers.
            else:
                errorCode = "IAM user was modified."
                remediation_action = "Notification sent to cloud IR team for Action"
        
        logger_info(eventName, errorCode, remediation_action, event)
        sns_publish(eventName, errorCode, remediation_action, event)
        
    except ClientError as e:
        errorCode = ("%s" % e)
        logger_info(eventName, errorCode, "N/A", event)
        sns_publish(eventName, errorCode, "N/A", event)


def sns_publish(eventName, errorCode, remediation_action, event):
    snsARN = os.environ['SNSARN']
    snsclient = boto3.client('sns')

    subject = f"Alert: Clodutrail Event- \"{eventName}\" received at {event['account']}"

    message = f"""
    Event: {subject}
    Event Result: {errorCode}
    Remediation Action:  {remediation_action}
    
    Raw Event: {event}
    """

    snspublish = snsclient.publish(
        TargetArn=snsARN,
        Subject=("%s" % subject),
        Message=("%s" % message))
    logger.info("SNS Publish Response- %s" % snspublish)
    logger.info("SNSARN: %s" % snsARN)

def logger_info(eventName, errorCode, remediation_action, event):

    subject = "iam_user_changes() was invoked by IR team: "

    message = f"""
    Event: {subject}
    Event Result: {errorCode}
    Remediation Action:  {remediation_action}
    
    Raw Event: {event}
    """
    logger.info(message)

def invoke_lambda(event,FunctionName,InvocationType,Payload):
    username = event['detail']['requestParameters']['userName']
    lambda_client = boto3.client('lambda')
    #message for access key lambda functions
    msg_access_key = { "keys": [ {"username": username , "KeyID":"*"}]}
    
    #message for delete_user and delete_policy functions
    msg_user_and_policy = { "keys": [ {"username": username }]}
    
    #call disable access key lambda function
    print("Calling disable access key lambda function...")
    invoke_disable_access_key=lambda_client.invoke(FunctionName="Disable_Access_key",
                                        InvocationType='RequestResponse',
                                        Payload=json.dumps(msg_access_key)
                                        )
    
    #call delete access key lambda function
    print("Calling delete access key lambda function...")                                    
    invoke_delete_access_key=lambda_client.invoke(FunctionName="delete_access_key",
                                        InvocationType='RequestResponse',
                                        Payload=json.dumps(msg_access_key)
                                        )
    
    #call delete inline policy lambda function
    print("Calling delete inline policy lambda function...")  
    invoke_delete_inline_policy=lambda_client.invoke(FunctionName="delete_inline_policy",
                                        InvocationType='RequestResponse',
                                        Payload=json.dumps(msg_user_and_policy)
                                        )
    
     #call detach managed policy lambda function
    print("Calling detach managed policy lambda function...")  
    invoke_detach_managed_policy=lambda_client.invoke(FunctionName="detach_managed_policy",
                                        InvocationType='RequestResponse',
                                        Payload=json.dumps(msg_user_and_policy)
                                        )
    
    #call delete user lambda function
    print("Calling delete user lambda function...")                                     
    invoke_delete_user=lambda_client.invoke(FunctionName="delete_user",
                                        InvocationType='RequestResponse',
                                        Payload=json.dumps(msg_user_and_policy)
                                        )