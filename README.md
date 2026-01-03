# Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## 📋 Project Overview

This project demonstrates automated resource tagging using AWS Lambda, Boto3, and Amazon EventBridge (CloudWatch Events). Whenever a new EC2 instance is launched, the Lambda function automatically tags it with the current date, creator information, and custom tags for better resource management and tracking.

## 🎯 Objectives

- Automate EC2 instance tagging on launch
- Utilize EventBridge for event-driven automation
- Implement resource tracking and management
- Practice AWS event-driven architecture
- Ensure consistent tagging policies

## 🏗️ Architecture

```
EC2 Instance Launch Event → EventBridge Rule → Lambda Function → EC2 API
                                                       ↓
                                              Auto-apply Tags
                                                       ↓
                                                CloudWatch Logs
```

## 📦 Prerequisites

- AWS Account (Free Tier eligible)
- Basic understanding of AWS EC2
- Python 3.x knowledge
- Understanding of AWS EventBridge
- AWS IAM permissions

## 🚀 Features

- **Automatic tagging**: Tags instances immediately upon launch
- **Event-driven**: Triggered by EC2 state change events
- **Customizable tags**: Easily modify tags to suit your needs
- **Launch date tracking**: Records when instance was created
- **Environment classification**: Adds environment tags (dev/prod/test)
- **No manual intervention**: Completely automated workflow

## 📁 Repository Structure

```
assignment5-ec2-auto-tagging/
├── README.md                          # This file
├── lambda_function.py                 # Lambda function code
├── documentation.md                   # Detailed step-by-step guide
└── screenshots/                       # Project screenshots
    ├── 01-iam-role-created.png
    ├── 02-lambda-function-created.png
    ├── 03-lambda-code-deployed.png
    ├── 04-eventbridge-rule-created.png
    ├── 05-ec2-instance-launched.png
    ├── 06-auto-tags-applied.png
    ├── 07-cloudwatch-logs.png
    └── 08-test-execution-results.png
```

## 🔧 Setup Instructions

### Step 1: Create IAM Role

1. Create IAM role: `Lambda-EC2-Tagging-Role`
2. Attach policy: `AmazonEC2FullAccess`
3. Trust entity: Lambda service

### Step 2: Create Lambda Function

1. Function name: `EC2-Auto-Tagger`
2. Runtime: Python 3.12
3. Execution role: `Lambda-EC2-Tagging-Role`
4. Deploy the code from `lambda_function.py`

### Step 3: Create EventBridge Rule

1. Rule name: `EC2-Instance-Launch-Rule`
2. Event pattern: EC2 Instance State-change Notification
3. Target: Lambda function `EC2-Auto-Tagger`

### Step 4: Test

1. Launch a new EC2 instance
2. Wait 1-2 minutes for Lambda to trigger
3. Check instance tags to verify automation

## 💻 Lambda Function Code

The Lambda function performs the following operations:

1. Extracts instance ID from EventBridge event
2. Gets current date and time
3. Applies multiple tags to the instance:
   - LaunchDate: Current date
   - AutoTagged: "Yes"
   - Environment: "Dev" (customizable)
   - ManagedBy: "Lambda"
4. Logs all actions to CloudWatch

See `lambda_function.py` for complete implementation.

## 📊 Expected Results

### Before Launch:
- New EC2 instance has no custom tags (only default Name tag if specified)

### After Launch (1-2 minutes):
- Instance automatically receives these tags:
  ```
  LaunchDate: 2026-01-03
  AutoTagged: Yes
  Environment: Dev
  ManagedBy: Lambda
  Creator: auto-tagger-lambda
  ```

## 📸 Screenshots

All screenshots documenting the implementation process are available in the `screenshots/` directory.

## 🔍 Testing

### Manual Test

1. **Launch EC2 Instance:**
   ```
   - Go to EC2 Console
   - Click "Launch Instance"
   - Select any AMI and t2.micro instance type
   - Launch without manually adding tags
   ```

2. **Wait 1-2 minutes** for Lambda to process the event

3. **Verify Tags:**
   ```
   - Go to EC2 Console
   - Select your instance
   - Click "Tags" tab
   - Verify auto-applied tags are present
   ```

### Lambda Test Event

You can also test the Lambda function directly with this event:

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
    "arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0"
  ],
  "detail": {
    "instance-id": "i-1234567890abcdef0",
    "state": "running"
  }
}
```

**Note:** Replace the instance ID with an actual running instance ID in your account.

## 📝 CloudWatch Logs Sample

```
START RequestId: xxxxx
Processing EC2 instance launch event
Instance ID: i-1234567890abcdef0
State: running
Applying tags to instance i-1234567890abcdef0
Tags applied successfully:
  LaunchDate: 2026-01-03
  AutoTagged: Yes
  Environment: Dev
  ManagedBy: Lambda
  Creator: auto-tagger-lambda
END RequestId: xxxxx
```

## 🔐 Security Considerations

### Current Implementation
- Uses `AmazonEC2FullAccess` for simplicity

### Production Recommendations
- Use least privilege IAM policies
- Restrict to specific EC2 actions
- Add resource-level permissions
- Enable CloudTrail for audit

### Recommended IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:CreateTags",
        "ec2:DescribeTags"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

## 🎓 Learning Outcomes

- Event-driven architecture with AWS
- EventBridge (CloudWatch Events) usage
- EC2 instance lifecycle events
- Automated resource management
- Tag-based resource organization
- Lambda event processing
- Infrastructure automation patterns

## 💡 Use Cases

- **Cost allocation**: Tag resources by project/department for billing
- **Compliance**: Ensure all resources follow tagging policies
- **Resource tracking**: Know when and who created resources
- **Automated governance**: Enforce organizational standards
- **Environment management**: Differentiate dev/test/prod resources
- **Security**: Tag resources for security group policies

## 🔄 Future Enhancements

- [ ] Add SNS notifications when instances are tagged
- [ ] Tag based on IAM user who launched the instance
- [ ] Different tags for different instance types
- [ ] Store tagging history in DynamoDB
- [ ] Add tag validation and compliance checks
- [ ] Auto-tag other AWS resources (EBS volumes, security groups)
- [ ] Create dashboard showing tagged resources
- [ ] Implement tag-based automation rules

## 🧹 Cleanup

To avoid unnecessary AWS charges:

```bash
# Terminate test EC2 instances
# Delete Lambda function
# Delete EventBridge rule
# Delete IAM role
# Remove CloudWatch log groups
```

## ⚠️ Important Notes

### EventBridge Trigger Delay
- Lambda triggers within 1-2 minutes of instance launch
- Not instantaneous - slight delay is normal
- Event is triggered when instance state changes to "running"

### Tag Limitations
- Maximum 50 tags per resource
- Tag keys and values are case-sensitive
- Tag keys can be up to 128 characters
- Tag values can be up to 256 characters

### Cost Considerations
- Lambda invocations: FREE (within free tier)
- EventBridge events: FREE (within free tier)
- This assignment: $0.00 expected cost

## 📚 References

- [Amazon EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)
- [EC2 Instance State Change Events](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-state-change-events.html)
- [Boto3 EC2 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
- [AWS Tagging Best Practices](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html)

## 👤 Author

**Your Name**
- GitHub: [@PriyankP2](https://github.com/PriyankP2)

## 📄 License

This project is created for educational purposes as part of AWS Lambda automation assignment.

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

---

**Note**: This project demonstrates event-driven automation - a key pattern in modern cloud architecture!
