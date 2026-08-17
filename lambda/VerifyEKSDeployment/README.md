# Deployment Verify
Serverless Framework Lambda Functions to verify EKS pod deployments.  

# Functions

to obtain a list of functions run `sls info`

## Serverless Framework: 
Installation:
https://www.serverless.com/framework/docs/getting-started/

AWS Docs:
https://www.serverless.com/framework/docs/providers/aws/


## Deploy All Functions 
Setup: Install Serverless Framework
1. run ```sls package --stage <stage>```
2. review generated CloudFormation templates in the .serverless folder
3. run ```sls deploy --stage <stage>```

## Deploy a Single Function 
steps 1 and 2 above 
3. run: ```sls deploy --stage <stage> function -f auto-release```

## Test Locally

To test locally use a test event json file.  Tests have been provided in the test directory.

verify
`serverless invoke local --function verify --path test/dev-app.json`

