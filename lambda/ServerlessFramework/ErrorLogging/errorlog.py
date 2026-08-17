import base64
import boto3
import gzip
import json
import logging
import os
import os
import urllib3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logpayload(event):
    logger.setLevel(logging.DEBUG)
    logger.debug(event['awslogs']['data'])
    compressed_payload = base64.b64decode(event['awslogs']['data'])
    uncompressed_payload = gzip.decompress(compressed_payload)
    log_payload = json.loads(uncompressed_payload)
    return log_payload

def error_details(payload):
    error_msg = ""
    log_events = payload['logEvents']
    logger.debug(payload)
    loggroup = payload['logGroup']
    logstream = payload['logStream']
    lambda_func_name = loggroup.split('/')
    logger.debug(f'LogGroup: {loggroup}')
    logger.debug(f'Logstream: {logstream}')
    logger.debug(f'Function name: {lambda_func_name[3]}')
    logger.debug(log_events)
    for log_event in log_events:
        error_msg += log_event['message']
    logger.debug('Message: %s' % error_msg.split("\n"))
    return loggroup, logstream, error_msg, lambda_func_name

def slackNotify(lgroup, lstream, errmessage, lambdaname, source):
    a = ""
    if source == "lambda":
        a = "*Lambda Function*: " + str(lambdaname[3])
    if source == "codebuild":
         a = "*CodeBuild*: " + str(lambdaname[3])
    b = "*Log Group*: " + str(lgroup)
    e = "*Log Stream*: " + str(lstream)
    s = "*Error Message*: " + str(errmessage.split("\n"))
    payload = {'text': a + "\n" + b + "\n" + e + "\n" + s}
    print(payload)
    encoded_data = json.dumps(payload).encode('utf-8')
    # urllib3
    endpoint = os.environ["slack_channel"]
    http = urllib3.PoolManager()
    r = http.request("POST", endpoint, body=encoded_data)

def logError(event, context):
    pload = logpayload(event)
    lgroup, lstream, errmessage, lambdaname = error_details(pload)
    slackNotify(lgroup, lstream, errmessage, lambdaname, "lambda")

def cbLogError(event, context):
    pload = logpayload(event)
    lgroup, lstream, errmessage, cbname = error_details(pload)
    slackNotify(lgroup, lstream, errmessage, cbname, "codebuild")