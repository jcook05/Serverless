import urllib3
import json
import time
import boto3
from boto3.dynamodb.conditions import Key
import os

MAX_WAIT_SECONDS = 260  
POLL_INTERVAL = 10       

def putEvent(status, detail):
    client = boto3.client("events")
    
    print("Putting Event for: ", detail['environment'], detail['deployment'], status)

    detail['state'] = status
   
    client.put_events(
        Entries=[
            {
                "DetailType": "Deployment State Notification",
                "Source": "eks.deploy",
                "Detail": json.dumps(detail),
                "EventBusName": "devops"
            }
        ]
    )

class PodVerifier:
    def __init__(self, endpoint, pod_name):
        self.endpoint = endpoint
        self.pod_name = pod_name
        self.http = urllib3.PoolManager()

    def get_pod_data(self):
        for attempt in range(3):
            try:
                r = self.http.request("GET", self.endpoint)
                decoded = r.data.decode("utf-8")
                if not decoded:
                    raise ValueError("Empty response")
                return json.loads(decoded)
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(POLL_INTERVAL)
        raise RuntimeError("Failed to fetch pod data after retries")

    def get_pods(self):
        data = self.get_pod_data()
        print("pod data", data)
        pods = [
            x for x in data.get("podStatusByNamespace", [])
            if self.pod_name in x["Name"] and 'h' not in x["Age"] and 'd' not in x["Age"]
        ]
        return pods

    def is_ready(self, pod):
        return pod.get("Status") == "Running" and pod.get("Ready") == "1/1"

    def verify_age(self, pod):
        age = pod.get("Age", "")
        print("Pod Age: ", age)
        if "h" in age:
            return False
        if "m" in age:
            try:
                mins = int(age.split("m")[0].replace("(", "").strip() or 99)
                return mins <= 6
            except ValueError:
                return False
        if "s" in age:
            return True
        return False

    def has_crashloop(self, pods):
        return any(p.get("Status") == "CrashLoopBackOff" for p in pods)

    def verify(self):
        print(f"Verifying pod status for {self.pod_name}")
        start = time.time()

        while time.time() - start < MAX_WAIT_SECONDS:
            pods = self.get_pods()
            if not pods:
                print("No pods found; retrying...")
                time.sleep(POLL_INTERVAL)
                continue

            ## if multiple pods, check age 
            ## by design k8s will not terminate the previous pod until the new pod is ready
            if len(pods) > 1:
                for checkpod in pods:
                    print(checkpod)
                    if self.verify_age(checkpod):
                        print("using pod", checkpod)
                        pod = checkpod 
            else:
                pod = pods[0]
            if self.has_crashloop(pods):
                print("CrashLoopBackOff detected.")
                return "Unsuccessful"
            
            if self.verify_age(pod):
                if self.is_ready(pod):
                    return "Successful"
                print("Pod not ready yet, waiting...")
                time.sleep(POLL_INTERVAL)
                continue
            else: 
                return "Unsuccessful"                
           
        print("Timeout reached before pod became ready.")
        return "Unsuccessful"

class DepVerify:
    
    def getAppConfig(self, app):
        dynamodb = boto3.resource("dynamodb", "us-west-2")
        table = dynamodb.Table("managed-projects")
        response = table.query(KeyConditionExpression=Key("App").eq(app))
        return response["Items"][0]["Config"]

    def run_deploy_verification(self, env, app, detail):
        print(f"Starting verification for {app} in {env}")
        endpoint = os.environ['BASEURL'] + env
        print("Endpoint: ", endpoint)
        status = PodVerifier(endpoint, app).verify()
        putEvent(status, detail)
        return status

def depVerify(event, context):
    
    print(event)
    app = event["APP"]
    env = event["ENV"]

    detail = {
        "state": "",
        "timestamp": int(time.time()),
        "deployment": app,
        "environment": env,
        "buildlink": event.get("BUILDLINK"),
        "branch": event.get("BRANCH"),
        "release": event.get("RELEASE"),
        "commit": event.get("COMMIT"),
        "image": event.get("IMAGE"),
        "buildname": event.get("BUILDNAME"),
        "author": event.get("AUTHOR"),
    }
    try:
        verifier = DepVerify()
        status = verifier.run_deploy_verification(env, app, detail)
        print(f"Verification {status} for {app}")
        return {"app": app, "env": env, "status": status}
    except Exception as e:
        print(f"Verification failed: {e}")
        putEvent("Unsuccessful", detail)
        raise

def depVerifyRequest(event, context):
    print(event)
    try:
   
        data = event.get("detail")
    
        message = {
        "APP": data['deployment'],
        "ENV": data['environment'],
        "IMAGE": data['image'],
        "BUILDLINK": data['buildlink'],
        "BRANCH": data['branch'],
        "RELEASE": data['release'],
        "COMMIT": data['commit'],
        "BUILDNAME": data['buildname'],
        "AUTHOR": data['author'],
       }
       
        # Invoke Lambda function
        client = boto3.client('lambda', region_name='us-west-2')
        response = client.invoke(
            FunctionName=f'arn:aws:lambda:us-west-2:ACCOUNTID:function:eks-deployment-{os.environ["STAGE"]}-verify',
            InvocationType='Event',
            Payload=json.dumps(message)
        )
        print("Function Response: ", response)

        body = {"message": f"Verification Request Received"}
        return {"statusCode": 200, "body": json.dumps(body)}

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Missing key: {str(e)}",
                "function": context.function_name
            })
        }
    except json.JSONDecodeError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Invalid JSON format: {str(e)}",
                "function": context.function_name
            })
        }
    except boto3.exceptions.Boto3Error as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"AWS Error: {str(e)}",
                "function": context.function_name
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Unexpected error occurred: {str(e)}",
                "function": context.function_name
            })
        }