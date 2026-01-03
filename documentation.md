# Auto-Tagging EC2 Instances - Complete Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Code Explanation](#code-explanation)
6. [Testing and Verification](#testing-and-verification)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Introduction

### Project Goal
Automate EC2 instance tagging using AWS Lambda and Amazon EventBridge. Whenever a new EC2 instance is launched, it automatically receives tags for tracking, management, and compliance purposes.

### Why Auto-Tagging Matters
- **Resource Management**: Track when and how resources were created
- **Cost Allocation**: Assign costs to projects, teams, or environments
- **Compliance**: Ensure all resources follow organizational tagging policies
- **Automation**: Eliminate manual tagging errors and omissions
- **Governance**: Enforce consistent resource naming and categorization

### Real-World Use Cases
- **Multi-team environments**: Automatically tag resources by team/department
- **Cost tracking**: Tag resources for detailed billing reports
- **Compliance requirements**: Meet regulatory tagging standards
- **DevOps automation**: Differentiate dev/test/prod environments
- **Security policies**: Apply security rules based on tags

### Technologies Used
- **AWS Lambda**: Serverless compute service
- **Amazon EventBridge**: Event bus for event-driven architecture
- **AWS EC2**: Virtual machine instances
- **Boto3**: AWS SDK for Python
- **AWS IAM**: Identity and Access Management
- **CloudWatch Logs**: Logging and monitoring

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                              │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              EC2 Console / API                          │   │
│  │                                                         │   │
│  │  User launches new EC2 instance                         │   │
│  │  (without manual tags)                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           EC2 Instance State Change Event               │   │
│  │                                                         │   │
│  │  Event Details:                                         │   │
│  │  - Source: aws.ec2                                      │   │
│  │  - Detail-Type: EC2 Instance State-change Notification  │   │
│  │  - Instance ID: i-1234567890abcdef0                     │   │
│  │  - State: running                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Amazon EventBridge Rule                    │   │
│  │                                                         │   │
│  │  Rule: EC2-Instance-Launch-Rule                         │   │
│  │  Pattern: Match EC2 state change to "running"           │   │
│  │  Target: Lambda function                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         Lambda Function: EC2-Auto-Tagger                │   │
│  │                                                         │   │
│  │  1. Receive EventBridge event                           │   │
│  │  2. Extract instance ID                                 │   │
│  │  3. Verify instance state is "running"                  │   │
│  │  4. Get current date/time                               │   │
│  │  5. Create tag list:                                    │   │
│  │     - LaunchDate: 2026-01-03                            │   │
│  │     - AutoTagged: Yes                                   │   │
│  │     - Environment: Dev                                  │   │
│  │     - ManagedBy: Lambda                                 │   │
│  │     - Creator: auto-tagger-lambda                       │   │
│  │  6. Apply tags to instance                              │   │
│  │  7. Log success                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              EC2 API - Create Tags                      │   │
│  │                                                         │   │
│  │  Tags applied to instance i-1234567890abcdef0           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  CloudWatch Logs                        │   │
│  │                                                         │   │
│  │  - Event received                                       │   │
│  │  - Instance ID extracted                                │   │
│  │  - Tags applied                                         │   │
│  │  - Success/failure logged                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘

Result: EC2 instance now has automatic tags applied!
```

**Event Flow:**
1. User launches EC2 instance
2. EC2 service emits state-change event to EventBridge
3. EventBridge rule matches the event pattern
4. Lambda function is triggered
5. Function extracts instance ID and applies tags
6. Tags appear on the EC2 instance (1-2 minute delay)
7. All actions logged to CloudWatch

---

## Prerequisites

### AWS Account Requirements
- Active AWS account with console access
- Permissions to create EC2 instances, Lambda functions, EventBridge rules, and IAM roles

### Knowledge Requirements
- Basic understanding of EC2 instances
- Familiarity with AWS Lambda
- Understanding of event-driven architecture
- Python basics
- AWS IAM concepts

### Understanding EventBridge
**Amazon EventBridge** (formerly CloudWatch Events) is a serverless event bus that:
- Routes events from AWS services to targets (like Lambda)
- Filters events based on patterns
- Enables event-driven architectures
- No servers to manage

---

## Step-by-Step Implementation

### Step 1: Create IAM Role for Lambda

#### 1.1 Navigate to IAM Service

1. Log in to [AWS Management Console](https://console.aws.amazon.com)
2. Search for **"IAM"** in the top search bar
3. Click on **"IAM"**

#### 1.2 Create New Role

1. Click **"Roles"** in the left sidebar
2. Click **"Create role"** button

#### 1.3 Select Trusted Entity

1. **Trusted entity type**: Select **"AWS service"**
2. **Use case**: Select **"Lambda"**
3. Click **"Next"**

**📸 Screenshot Point**: Trusted entity selection

#### 1.4 Attach Permissions Policy

1. In the search box, type: `AmazonEC2FullAccess`
2. **Check the checkbox** next to **"AmazonEC2FullAccess"**
3. Click **"Next"**

**📸 Screenshot Point**: Policy attached

**Note**: In production, use a more restrictive policy with only `ec2:CreateTags` and `ec2:DescribeInstances` permissions.

#### 1.5 Name and Create Role

1. **Role name**: `Lambda-EC2-Tagging-Role`
2. **Description**: `Allows Lambda to automatically tag EC2 instances on launch`
3. Click **"Create role"**

**📸 Screenshot Point**: Role created

**✅ Checkpoint**: IAM role created with EC2 permissions

---

### Step 2: Create Lambda Function

#### 2.1 Navigate to Lambda Service

1. Search for **"Lambda"** in AWS Console
2. Click on **"Lambda"**

#### 2.2 Create Function

1. Click **"Create function"** button
2. Select **"Author from scratch"**

**📸 Screenshot Point**: Create function page

#### 2.3 Configure Basic Settings

1. **Function name**: `EC2-Auto-Tagger`
2. **Runtime**: **Python 3.12**
3. **Architecture**: x86_64
4. Expand **"Change default execution role"**
5. Select **"Use an existing role"**
6. **Existing role**: Select `Lambda-EC2-Tagging-Role`
7. Click **"Create function"**

**📸 Screenshot Point**: Function created

**✅ Checkpoint**: Lambda function created

---

### Step 3: Add Lambda Function Code

#### 3.1 Copy the Code

**Copy this entire code:**

```python
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
```

#### 3.2 Paste the Code

1. In the Lambda code editor, select all default code (Ctrl+A or Cmd+A)
2. Delete it
3. Paste the code above
4. Click **"Deploy"**

**📸 Screenshot Point**: Code deployed

**✅ Checkpoint**: Lambda code deployed

---

### Step 4: Create EventBridge Rule

This is the key step that connects EC2 events to your Lambda function.

#### 4.1 Navigate to EventBridge

1. In AWS Console search bar, type **"EventBridge"**
2. Click on **"Amazon EventBridge"**
3. Click **"Rules"** in the left sidebar
4. Make sure you're on the **"default"** event bus

**📸 Screenshot Point**: EventBridge dashboard

#### 4.2 Create Rule

1. Click **"Create rule"** button

#### 4.3 Define Rule Details

1. **Name**: `EC2-Instance-Launch-Rule`
2. **Description**: `Triggers Lambda function when EC2 instance is launched`
3. **Event bus**: default (should be selected)
4. **Rule type**: Select **"Rule with an event pattern"**
5. Click **"Next"**

**📸 Screenshot Point**: Rule details

#### 4.4 Build Event Pattern

1. **Event source**: Select **"AWS events or EventBridge partner events"**

2. **Creation method**: Select **"Custom pattern (JSON editor)"**

3. **Event pattern**: Paste this JSON:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

4. Click **"Next"**

**📸 Screenshot Point**: Event pattern configured

**What this pattern does:**
- **source**: Listens to events from EC2 service
- **detail-type**: Specifically for instance state changes
- **state**: Only triggers when instance enters "running" state

#### 4.5 Select Target

1. **Target types**: Select **"AWS service"**
2. **Select a target**: Choose **"Lambda function"** from dropdown
3. **Function**: Select `EC2-Auto-Tagger` from the dropdown
4. Leave other settings as default
5. Click **"Next"**

**📸 Screenshot Point**: Target configured

#### 4.6 Configure Tags (Optional)

1. Skip this step (click **"Next"**)

#### 4.7 Review and Create

1. Review all settings:
   - Rule name: EC2-Instance-Launch-Rule
   - Event pattern: EC2 state change to "running"
   - Target: Lambda function EC2-Auto-Tagger

2. Click **"Create rule"**

3. You should see: "Successfully created rule EC2-Instance-Launch-Rule"

**📸 Screenshot Point**: Rule created successfully

**✅ Checkpoint**: EventBridge rule created and connected to Lambda

---

### Step 5: Test the Automation

Now we'll test by launching an EC2 instance.

#### 5.1 Launch a Test EC2 Instance

1. Go to **EC2 Console**
2. Click **"Launch Instance"**

3. Configure instance:
   - **Name**: `auto-tag-test` (or leave blank to test)
   - **AMI**: Amazon Linux 2023 (free tier)
   - **Instance type**: t2.micro
   - **Key pair**: Select existing or skip
   - **DO NOT add any tags manually** - we want Lambda to do this

4. Click **"Launch instance"**

5. Note the **Instance ID** (e.g., i-1234567890abcdef0)

**📸 Screenshot Point**: EC2 instance launching

#### 5.2 Wait for Lambda Trigger

- Wait **1-2 minutes** for:
  1. Instance to reach "running" state
  2. EventBridge to detect the event
  3. Lambda to process and apply tags

**Tip**: You can monitor Lambda execution in real-time:
- Go to Lambda Console → EC2-Auto-Tagger → Monitor tab
- Click "View CloudWatch logs"

#### 5.3 Verify Tags Were Applied

1. Go to **EC2 Console** → **Instances**
2. Find your instance (it should be "running" now)
3. Select the instance
4. Click **"Tags"** tab at the bottom
5. **Verify these tags exist**:
   - LaunchDate: (today's date)
   - LaunchDateTime: (current date and time)
   - AutoTagged: Yes
   - Environment: Dev
   - ManagedBy: Lambda
   - Creator: auto-tagger-lambda

**📸 Screenshot Point**: Instance with auto-applied tags

**✅ SUCCESS!** If you see these tags, your automation is working!

#### 5.4 Check CloudWatch Logs

1. Go to **Lambda Console** → **EC2-Auto-Tagger**
2. Click **"Monitor"** tab
3. Click **"View CloudWatch logs"**
4. Click on the latest **log stream**
5. You should see logs like:

```
START RequestId: xxxxx
Processing EC2 instance launch event
Event: {...}
Instance ID: i-1234567890abcdef0
State: running
Applying tags to instance i-1234567890abcdef0
Tags applied successfully to instance i-1234567890abcdef0
Applied tags:
  LaunchDate: 2026-01-03
  LaunchDateTime: 2026-01-03 15:30:45
  AutoTagged: Yes
  Environment: Dev
  ManagedBy: Lambda
  Creator: auto-tagger-lambda
END RequestId: xxxxx
```

**📸 Screenshot Point**: CloudWatch logs showing successful tagging

**✅ Final Checkpoint**:
- ✓ EC2 instance launched
- ✓ Lambda triggered automatically by EventBridge
- ✓ Tags applied to instance
- ✓ Logs show successful execution

---

### Step 6: Test with Manual Lambda Invocation (Optional)

You can also test the Lambda function directly with a test event.

#### 6.1 Create Test Event

1. Go to **Lambda Console** → **EC2-Auto-Tagger**
2. Click **"Test"** tab
3. Click **"Create new event"**
4. **Event name**: `TestEC2Event`
5. **Event JSON**: Paste this (replace with your actual instance ID):

```json
{
  "version": "0",
  "id": "12345678-1234-1234-1234-123456789012",
  "detail-type": "EC2 Instance State-change Notification",
  "source": "aws.ec2",
  "account": "123456789012",
  "time": "2026-01-03T12:00:00Z",
  "region": "us-east-1",
  "resources": [
    "arn:aws:ec2:us-east-1:123456789012:instance/i-REPLACE_WITH_YOUR_INSTANCE_ID"
  ],
  "detail": {
    "instance-id": "i-REPLACE_WITH_YOUR_INSTANCE_ID",
    "state": "running"
  }
}
```

**Important**: Replace `i-REPLACE_WITH_YOUR_INSTANCE_ID` with an actual running instance ID from your account.

6. Click **"Save"**
7. Click **"Test"**

**📸 Screenshot Point**: Test execution results

---

## Code Explanation

### EventBridge Event Structure

```python
{
  "version": "0",
  "id": "event-id",
  "detail-type": "EC2 Instance State-change Notification",
  "source": "aws.ec2",
  "detail": {
    "instance-id": "i-1234567890abcdef0",
    "state": "running"
  }
}
```

- **source**: Always "aws.ec2" for EC2 events
- **detail-type**: Type of notification
- **detail**: Contains the actual event data
  - **instance-id**: The ID of the instance
  - **state**: Current state (pending, running, stopping, stopped, etc.)

### Extracting Instance ID

```python
if 'detail' not in event or 'instance-id' not in event['detail']:
    # Error handling
    return error_response

instance_id = event['detail']['instance-id']
instance_state = event['detail'].get('state', 'unknown')
```

- Validates event structure
- Extracts instance ID from the event
- Gets the current state

### State Validation

```python
if instance_state != 'running':
    print(f"Instance is not in running state, skipping tagging")
    return success_response  # Not an error, just skipping
```

- Only tags instances in "running" state
- Prevents tagging instances that are stopping/stopped
- Returns success (not error) if state doesn't match

### Date and Time Formatting

```python
current_date = datetime.now().strftime('%Y-%m-%d')
current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
```

- **%Y**: 4-digit year (2026)
- **%m**: 2-digit month (01-12)
- **%d**: 2-digit day (01-31)
- **%H**: Hour in 24-hour format (00-23)
- **%M**: Minute (00-59)
- **%S**: Second (00-59)

### Tag Structure

```python
tags = [
    {'Key': 'LaunchDate', 'Value': current_date},
    {'Key': 'AutoTagged', 'Value': 'Yes'},
    # ... more tags
]
```

- Each tag is a dictionary with 'Key' and 'Value'
- Tags are applied as a list
- You can modify these to match your organization's needs

### Applying Tags

```python
ec2_client.create_tags(
    Resources=[instance_id],
    Tags=tags
)
```

- **create_tags()**: EC2 API to add tags
- **Resources**: List of resource IDs (instances, volumes, etc.)
- **Tags**: List of tag dictionaries
- Can tag multiple resources at once

---

## Testing and Verification

### Test Checklist

- [ ] IAM role created with EC2 permissions
- [ ] Lambda function created and deployed
- [ ] EventBridge rule created and active
- [ ] Rule connected to Lambda function
- [ ] EC2 instance launched
- [ ] Instance reached "running" state
- [ ] Lambda executed (check CloudWatch logs)
- [ ] Tags applied to instance
- [ ] Tags visible in EC2 console

### Verification Steps

1. **Check EventBridge Rule Status**:
   - Go to EventBridge → Rules
   - Rule should be "Enabled"

2. **Check Lambda Permissions**:
   - Lambda → Configuration → Permissions
   - Should have resource-based policy allowing EventBridge to invoke

3. **Check CloudWatch Logs**:
   - Lambda → Monitor → View logs
   - Should see execution logs when instance launches

---

## Troubleshooting

### Issue 1: Tags Not Applied

**Symptoms**: EC2 instance launches but no tags appear

**Solutions**:
1. Check EventBridge rule is **Enabled**
2. Verify rule event pattern matches EC2 state changes
3. Check Lambda has EC2 permissions (IAM role)
4. Review CloudWatch logs for errors
5. Wait 2-3 minutes (there can be a delay)

### Issue 2: Lambda Not Triggered

**Symptoms**: No logs in CloudWatch when instance launches

**Solutions**:
1. Verify EventBridge rule exists
2. Check rule target is set to correct Lambda function
3. Ensure Lambda has resource-based policy for EventBridge
4. Test with manual Lambda invocation first

### Issue 3: Permission Errors

**Symptoms**: Error in logs about permissions

**Solutions**:
1. Verify IAM role has `ec2:CreateTags` permission
2. Check Lambda execution role is attached
3. Ensure role trust relationship includes lambda.amazonaws.com

### Issue 4: Wrong Instance Tagged

**Symptoms**: Tags applied to wrong instance

**Solutions**:
1. Check event pattern in EventBridge rule
2. Verify instance ID extraction logic
3. Review CloudWatch logs for instance ID

---

## Best Practices

### Tag Naming Conventions

1. **Use PascalCase for keys**: `LaunchDate`, `Environment`
2. **Be descriptive**: `CreatedBy` not just `By`
3. **Use namespaces**: `Project:Name`, `Cost:Center`
4. **Limit tag count**: 10-15 essential tags per resource

### Production Enhancements

1. **Extract user information**:
```python
# Get IAM user who launched instance
user_arn = event['detail']['userIdentity']['arn']
user_name = user_arn.split('/')[-1]
tags.append({'Key': 'LaunchedBy', 'Value': user_name})
```

2. **Environment-based tagging**:
```python
# Determine environment from VPC or subnet
vpc_id = instance_details['VpcId']
if vpc_id == 'vpc-prod123':
    environment = 'Production'
elif vpc_id == 'vpc-dev456':
    environment = 'Development'
```

3. **Add SNS notifications**:
```python
# Notify when instance is tagged
sns_client.publish(
    TopicArn='arn:aws:sns:region:account:ec2-tags',
    Subject=f'EC2 Instance Tagged: {instance_id}',
    Message=f'Instance {instance_id} was automatically tagged'
)
```

4. **Cost allocation tags**:
```python
tags.extend([
    {'Key': 'CostCenter', 'Value': '12345'},
    {'Key': 'Project', 'Value': 'WebApp'},
    {'Key': 'Owner', 'Value': 'team@company.com'}
])
```

---

## Summary

### What We Built
- ✅ Event-driven auto-tagging system
- ✅ EventBridge rule for EC2 state changes
- ✅ Lambda function to apply tags automatically
- ✅ Comprehensive logging for audit trail

### Skills Learned
- Event-driven architecture with EventBridge
- EC2 instance lifecycle events
- Lambda event processing
- Automated resource tagging
- Tag-based resource management

### Real-World Value
- Automated compliance with tagging policies
- Consistent resource tracking
- Reduced manual errors
- Better cost allocation
- Improved resource governance

---

**Congratulations!** You've completed the project. This event-driven automation pattern is foundational for modern cloud architectures!
