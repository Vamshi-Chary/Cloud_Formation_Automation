import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    codecommit = boto3.client('codecommit')
    codecommit_client = boto3.client('codecommit')

    # Retrieve S3 object details from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Download the object content from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read()

    

    # Push changes to CodeCommit
    repo_name = 'CloudFormation-Pipeline-Repo'
    branch_name = 'main'  # Change as needed
    putFilesList = [{'filePath': file_key, 'fileContent': file_content}]
    
    
    try:
        response = codecommit_client.get_branch(
            repositoryName=repo_name,
            branchName=branch_name
        )
        parent_commit_id = response['branch']['commitId']
    except ClientError as error:
        print(f"Error getting parent commit ID: {error.response['Error']['Message']}")
        return
    

    try:
        response = codecommit.create_commit(
            repositoryName=repo_name,
            branchName=branch_name,
            putFiles=putFilesList,
            parentCommitId=parent_commit_id,
            commitMessage='Syncing changes from S3',
            authorName='OC001',
            email='OC001@oneclick.com'
        )
        print(f"Commit ID: {response['commitId']}")
    except ClientError as error:
        print(f"Error creating commit: {error.response['Error']['Message']}")

    return "Code pushed to CodeCommit successfully!"

# Note: Adjust the error handling and authentication as needed.
