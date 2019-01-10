Example of an AWS Serverless Project for .Net Core 2.0, NodeJS and Python.  

This projects contained in this repo are loosely based on the Microsoft Microservices on Docker project: https://docs.microsoft.com/en-us/dotnet/articles/csharp/tutorials/microservices where Docker containers are used.    While containerization definitely has a role to play in modern IT infrastructures containers may not be the best model to use for true RESTful Microservices.   The Serverless model allows the implementation of RESTful Microservices while minimizing infrastructure requirements.   Depending upon the cloud platform leveraged, costs are significantly reduced as well.   This project leverages AWS Lambda and APIGateway which both provide 1 million free uses.  The cost of the services after the 1 million free uses is minimal as well.  

This repo illustrates how teams can use the Serverless Framework to develop services in a variety of languages.   The projects contained within implement the same weather service in numerous languages to include .netcore, nodejs and python.  The projects are currently configured for AWS however they can be configured for several other cloud providers. 


This service represents a simplified service for demo purposes and does not include a hosted zone, IAM policies or authentication which could easily be added.  



## Technologies used

 1. **Serverless Framework**
 2. **AWS** 
      - Lambda
      - APIGateway
      - S3
 3. **dotnetcore2.0**
 4. **C# Libraries** 
     - Amazon.Lambda.Core;
     - Amazon.Lambda.APIGatewayEvents;
     - System;
     - System.Net;
     - System.Collections.Generic;
     - Newtonsoft.Json;
 5. **Python Modules** 
     - random
     - urlparse
 6. **NodeJS Libraries**
     - querystring


## Prepare your environment


**Install the Serverless Framework**

https://serverless.com/framework/docs/getting-started/

npm install serverless -g


**Configure AWS Credentials**

AWS Credentials can be configured in a number of ways.   Choose the option that works best for you. 

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

Additional Options:
https://serverless.com/framework/docs/providers/aws/guide/credentials/


###### netcoreweather

**C# Source** 

1. Handler.cs: This file contains 2 classes within the WeatherService namespace. 

  - WeatherReport  -   Generates a random weather forecast 

  - APIGatewayProxyResponse  -  Gets a WeatherReport based on the lat and long within the query string and returns a serialized json report. 

2. Build:

Run the included build.sh or build.cmd scripts.

This will compile the code create a .zip ready for deployment


###### nodejsweather

1.  handler.js  

2. Build:    No build steps are necessary for this project


###### pythonweather

1.  handler.py  

2. Build:    No build steps are necessary for this project






## Deploy

The Deploy step is the same for all languages.   This maximizes reusability as numerous teams leveraging several languages can deploy code in a consistent manner.   You will not have retrain your DevOps or Build teams to deploy and maintain your code for different teams. 

   From the directory containing the serverless.yml file for your project sls deploy or serverless deploy commands
   
   The deployment creates a CloudFormation template that is used to manage the resulting stack. 

Once your deploy is complete you will see an output similar to below:

Serverless: Stack update finished...
Service Information
service: weather
stage: dev
region: us-west-2
stack: weather-dev
api keys:
  None
endpoints:
  GET - https://v24ewjbow1.execute-api.us-west-2.amazonaws.com/dev/
functions:
  weather: weather-dev-weather


A Lambda Service and APIGateway Endpoint will have been created in the AWS us-west-2 (Oregon) region.  

Access your new endpoint via:  

https://v24ewjbow1.execute-api.us-west-2.amazonaws.com/dev/?lat=35.5&long=40.75
