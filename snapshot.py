import boto3
import pprint

def lambda_handler(event, context):
    pp = pprint
    ec2 = boto3.client('ec2')
	#ec2 = boto3.resource('ec2')
    #image = ec2.Image('id')
	
	#deregister image
    
    
    
    #image = ec2.image(revert_log['image_id'])
    
    
    #deregister_image= image.deregister('image')
    
    #list snapshots for specified volume
    snapshot_response = ec2.describe_snapshots(
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [
                'vol-0db84e7443b3b0425'
            ]
        }
    ]
    
	)
	
    print(snapshot_response)
	
	#remove snapshot(s)
    for snap in snapshot_response['Snapshots']:
        print ('Deleting snapshot ' + snap['SnapshotId'])
        ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])

   

