Example of an AWS Serverless Project for nodejs6.10

This project is loosely based on the Microsoft Microservices on Docker project: https://docs.microsoft.com/en-us/dotnet/articles/csharp/tutorials/microservices where Docker containers are used.    While containerization definitely has a role to play in modern IT infrastructures containers may not be the best model to use for true RESTful Microservices.   The Serverless model allows the implementation of RESTful Microservices while minimizing infrastructure requirements.   Depending upon the cloud platform leveraged, costs are significantly reduced as well.   This project leverages AWS Lambda and APIGateway which both provide 1 million free uses.  The cost of the services after the 1 million free uses is minimal as well.  


This service represents a simplified service for demo purposes and does not include a hosted zone, IAM policies or authentication which could easily be added.  



## Technologies used

Serverless Framework
AWS
 Lambda
 APIGateway
 S3
nodejs6.10


nodejs source

The Handler.cs file is the C# source.   This file contains 3 functions
generate - generates a rounded random whole number
RandomWeather  -   Generates a random weather forecast 

APIGatewayProxyResponse  -  Gets a WeatherReport based on the lat and long within the query string and returns a serialized json report. 



Install the Serverless Framework:

https://serverless.com/framework/docs/getting-started/

npm install serverless -g


Configure AWS Credentials

AWS Credentials can be configured in a number of ways.   Choose the option that works best for you. 

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

Additional Options:
https://serverless.com/framework/docs/providers/aws/guide/credentials/




Build:

nodejs does not require a build step.  

Deploy

   Run:  sls deploy or serverless deploy
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


Tear Down:

sls remove or serverless remove