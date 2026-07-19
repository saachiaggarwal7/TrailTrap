import boto3
from botocore.exceptions import ClientError
from config import HONEY_USERS
from deployer.policy_manager import (generate_devops_policy,generate_s3_readonly_policy,attach_inline_policy)
iam=boto3.client("iam")

session=boto3.session.Session()
REGION=session.region_name
s3_client=boto3.client("s3")

#creates honey users
def create_honey_user(username):
    try:
        iam.create_user(UserName=username)
        print(f"✅ Created IAM user: {username}")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"]=="EntityAlreadyExists":
            print(f"⚠️ IAM user already exists: {username}")
            return True
        else:
            print(f"Unexpected error: {e}")
    return False



#creates access keys
def create_access_key(username):
    try:
        response=iam.create_access_key(UserName=username)
        access_key=response["AccessKey"]
        print(f"✅ Created Access Key for {username}")
        return {
            "access_key_id":access_key['AccessKeyId'],
            "secret_access_key":access_key['SecretAccessKey']
        }
    except ClientError as e:
        if e.response["Error"]["Code"]=="LimitExceeded":
            print(f"⚠️ {username} already has the maximum number of access keys.")      
            return True  
        else:
            print(f"❌ Failed to create access key for {username}: {e}")
    return {}

#creates honey S3 buckets
def create_honey_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={
                                    "LocationConstraint":REGION
                                })
        print("✅ Bucket created successfully.")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"]=="BucketAlreadyExists":
            print(f"⚠️ Bucket with name {bucket_name} already exists.")
        elif e.response["Error"]["Code"]=="BucketAlreadyOwnedByYou":
            print(f"⚠️ Bucket with name {bucket_name} is already owned by you.")
            return True
        else:
             print(f"❌ Failed to create bucket: {bucket_name}:{e}")
    return False

#uploads decoy files
def upload_decoy_files(bucket_name,files):
    all_uploaded=True
    for file in files:
        try:
            with open(file["template"],"r") as f:
                content=f.read()
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=file["key"],
                    Body=content
                )
                print(f"✅ Uploaded {file['key']} to {bucket_name}")
        except FileNotFoundError as e:
            print(f"⚠️ file {file['key']} not found.")
            all_uploaded=False
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"❌ AWS Error [{error_code}]: {error_message}")
            all_uploaded=False
        except Exception as e:
            print(f"❌ Error while uploading file: {e}")
            all_uploaded=False
    return all_uploaded

#deploys honey user
def deploy_honey_users():
    for username in HONEY_USERS:
        if create_honey_user(username["username"]):
            if username['bucket'] is not None:
                if create_honey_bucket(username["bucket"]):
                   if upload_decoy_files(username["bucket"],username["files"]):
                        policy= generate_s3_readonly_policy(username['bucket'])
                        if policy:
                            attach_inline_policy(username['username'],username["policy_name"],policy)
                            create_access_key(username['username'])

            else:
                policy=generate_devops_policy()
                if policy:
                    attach_inline_policy(username['username'],username["policy_name"],policy)
                    create_access_key(username['username'])


