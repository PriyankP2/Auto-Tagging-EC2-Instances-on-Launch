import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function to automatically tag EC2 instances when they are launched.
    
    This function is triggered by EventBridge (CloudWatch Events) when an EC2
    instance state changes to 'running'. It automatically applies tags including
    launch date, environment, and management information.
    
    Args:
        event (dict): EventBridge event containing EC2 instance information
        context (object): Lambda context object
    
    Returns:
        dict: Response containing status code and tagging results
    
    Example EventBridge event structure:
    {
        "version": "0",
        "id": "...",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "detail": {
            "instance-id": "i-1234567890abcdef0",
            "state": "running"
        }
    }
    """
    
    # Initialize EC2 client
    ec2_client = boto3.client('ec2')
    
    try:
        # Log the incoming event for debugging
        print("Processing EC2 instance launch event")
        print(f"Event: {json.dumps(event)}")
        
        # Extract instance ID from the event
        if 'detail' not in event or 'instance-id' not in event['detail']:
            print("Error: No instance-id found in event")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Invalid event structure',
                    'error': 'Missing instance-id in event detail'
                })
            }
        
        instance_id = event['detail']['instance-id']
        instance_state = event['detail'].get('state', 'unknown')
        
        print(f"Instance ID: {instance_id}")
        print(f"State: {instance_state}")
        
        # Only tag instances that are in 'running' state
        if instance_state != 'running':
            print(f"Instance is not in running state (current: {instance_state}), skipping tagging")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Instance not in running state, skipping tagging',
                    'instance_id': instance_id,
                    'state': instance_state
                })
            }
        
        # Get current date and time
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Define tags to apply
        tags = [
            {
                'Key': 'LaunchDate',
                'Value': current_date
            },
            {
                'Key': 'LaunchDateTime',
                'Value': current_datetime
            },
            {
                'Key': 'AutoTagged',
                'Value': 'Yes'
            },
            {
                'Key': 'Environment',
                'Value': 'Dev'  # You can modify this based on your needs
            },
            {
                'Key': 'ManagedBy',
                'Value': 'Lambda'
            },
            {
                'Key': 'Creator',
                'Value': 'auto-tagger-lambda'
            }
        ]
        
        # Apply tags to the instance
        print(f"Applying tags to instance {instance_id}")
        ec2_client.create_tags(
            Resources=[instance_id],
            Tags=tags
        )
        
        # Log success
        print(f"Tags applied successfully to instance {instance_id}")
        print("Applied tags:")
        for tag in tags:
            print(f"  {tag['Key']}: {tag['Value']}")
        
        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Instance tagged successfully',
                'instance_id': instance_id,
                'tags_applied': tags
            })
        }
        
    except Exception as e:
        # Log and return error
        print(f"Error tagging instance: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error tagging instance',
                'error': str(e)
            })
        }
