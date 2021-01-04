# SF-Greenhouse Gas Emissions DE Pipeline

Tracking greenhouse gas emissions in San Francisco across department, source type, consumption units, and fiscal year. Completly hosted in the AWS ecosystem in cluding a dashboard built with Amazon Quicksight.

**If you would like to replicate this project deploy the CloudFormation template in the cfn directory.**

## Architecture
![](architecture/greenhouse_gas_emissions_architecture_diagram.png)

Data is sourced from San Francisco's Open Data API (https://dev.socrata.com/foundry/data.sfgov.org/pxac-sadh) as JSON documents containing information on greenhouse gas emissions throughout San Francisco. A series of Lambda functions integrated with SQS orchestrate the data movement throughout the pipeline. The presentation layer is created using Amazon QuickSight.
