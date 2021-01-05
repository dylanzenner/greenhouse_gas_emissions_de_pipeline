![GitHub last commit](https://img.shields.io/github/last-commit/dylanzenner/greenhouse_gas_emissions_de_pipeline)
![GitHub repo size](https://img.shields.io/github/repo-size/dylanzenner/greenhouse_gas_emissions_de_pipeline)
# SF-Greenhouse Gas Emissions DE Pipeline

Tracking greenhouse gas emissions in San Francisco across department, source type, consumption units, and fiscal year. Completly hosted in the AWS ecosystem in cluding a dashboard built with Amazon Quicksight.

**If you would like to replicate this project deploy the CloudFormation templates in the cfn directory.**

## Architecture
![](architecture/greenhouse_gas_emissions_architecture_diagram.png)

Data is sourced from San Francisco's Open Data API (https://dev.socrata.com/foundry/data.sfgov.org/pxac-sadh) as JSON documents containing information on greenhouse gas emissions throughout San Francisco. A series of Lambda functions integrated with SQS orchestrate the data movement and transformation throughout the pipeline. The presentation layer is created using Amazon QuickSight.

## Infrastructure
The project is housed in the AWS ecosystem and utilizes the following resources:

**VPC:**
-   Custom built VPC with two subnets (1 private, 1 public)
-   IGW, NATGW and Route Tables
-   Security Groups

**DynamoDB:**

-   On-Demand Capacity
- Partition key on the uuid field

**2 Lambda Functions:**
-   1 for pulling data from the API and sending it in batches to an SQS Queue
-   1 for transforming the data from the SQS Queue and sending it to DynamoDB

**Secrets Manager:**
-   For storing connection variables and API tokens

**S3 Bucket with versioning enabled:**
-   For storing the transformed data in JSON format

**SQS with a deadletter queue:**
-   For receiving data in batches from the API
-   Deadletter queue for automatic retry of failed messages

**SNS**
-   For sending failure messages to a Slack Channel

**CloudWatch Time-Based Events:**
-   For invoking the first lambda function and triggering the pipeline

**Amazon Quicksight:**
-   For the visualization layer

## Dashboard
![]()
![]()
![]()
![]()
![]()

## Points moving forward
