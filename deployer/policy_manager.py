import json
import boto3
from botocore.exceptions import ClientError

iam=boto3.client("iam")

def generate_s3_readonly_policy(bucket_name):
    read_policy={
    "Version":"2012-10-17",
    "Statement":[
        {
            "Sid":"AllowBucketListing",
            "Effect":"Allow",
            "Action":"s3:ListBucket",
            "Resource":f"arn:aws:s3:::{bucket_name}",
            
        },
        {
            "Sid":"AllowObjectRead",
            "Effect":"Allow",
            "Action":"s3:GetObject",
            "Resource":f"arn:aws:s3:::{bucket_name}/*"
        }
       ]
   }
    return read_policy

def generate_devops_policy():
    devops_policy={
        "Version":"2012-10-17",
        "Statement":[
            {
                "Sid":"AllowIAMReadOnly",
                "Effect":"Allow",
                "Action":["iam:GetUser","iam:GetAccountSummary","iam:ListAccessKeys"],
                "Resource": "*"
            }
        ]
    }
    return devops_policy

def attach_inline_policy(username,policy_name,policy):
    try:
        iam.put_user_policy(UserName=username,PolicyName=policy_name,PolicyDocument=json.dumps(policy))
        print(f"✅ Attached inline policy '{policy_name}' to {username}")
        return True
    except ClientError as e:
        print(f"❌ Failed to attach policy to {username}: {e}")
        return False