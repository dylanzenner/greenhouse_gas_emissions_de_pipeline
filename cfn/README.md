## If you would like to replicate this project please follow these instructions in order
- Make the necessary changes in the greenhouse_gas_emissions_s3_bucket_iac.yml file (i.e.: BucketName on line 7)
- Deploy the greenhouse_gas_emissions_s3_bucket_iac.yml file
- Upload the code for the lambda functions (zipped with their necessary dependencies) to the S3 bucket


- Create an IAM Role for the lambda function "pull_data.py" with the following permissions:
  
  - AWSLambdaBasicExecutionRole (Managed Policy)
  - AWSLambdaVPCAccessExecutionRole (Managed Policy)
  - Write access to SQS (Customer Policy)
  
- Create an IAM Role for the lambda function "send_to_dynamodb.py" with the following permissions:
  
  - AWSLambdaBasicExecutionRole (Managed Policy)
  - AWSLambdaSQSQueueExecutionRole (Managed Policy)
  - Write access to DynamoDB (Customer Policy)
  
- Create an IAM Role for the lambda function "export_to_s3.py" with the following permissions:
  
  - AWSLambdaBasicExecutionRole (Managed Policy)
  - DynamoDB write access for ExportTableToPointInTime (Customer Policy) 
  - Write access to S3 (Customer Policy)
  
- Make the necessary changes in the greenhouse_gas_emissions_iac.yml file (i.e.: Put the arn of the IAM Roles you created in the previous step here):
  - line 7
  - line 141
  - line 162
  - line 183
  
- Deploy the greenhouse_gas_emissions_iac.yml file

- Go to the AWS SQS dashboard
  - Click on the greenhouse_gas_emissions queue
  - Copy the queue URL
  - Go to the AWS Secrets Manager dashboard
  - Store the queue URL which you just copied in the previous step as a new secret and give it the name sqs_queue
  
- After you run the project and have your data in an S3 bucket do not forget to upload the s3_manifest file to the bucket with the correct URL paths to your exported data.
  
- With that, the project should be deployed successfully then you can head over to QuickSight to make your dashboard.


# !!Warning!!

The reason why I did not include the Lambda roles in the CF Template is because there is a known issue when deleting the CF template if it contains IAM Roles/IAM Policies which allow a Lambda function access to the VPC. When you delete the CF Template the lambda functions will be deleted before the network interfaces. The network interfaces which were allocated to those functions will then be unable to be deleted by CF during the deletion process. You will also be unable to detach or delete these interfaces because only the lambda function (which was deleted by CF) can delete them. This will result in the inability to delete the security groups, subnets, network interfaces, or VPC. You will have to contact AWS support to have them fix this issue if the article below is not able to help you.


https://aws.amazon.com/premiumsupport/knowledge-center/lambda-eni-find-delete/#:~:text=Network%20interfaces%20that%20Lambda%20creates%20can%20be%20deleted%20only%20by%20Lambda.&text=Lambda%20doesn't%20delete%20network,that%20created%20the%20network%20interfaces.
