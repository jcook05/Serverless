import json
from random import randint
from urlparse import urlsplit


def generator(min, max):
    return randint(min,max)

def RandomWeather(days):
    
    forecast = []
    conditions = ["Sunny","Mostly Sunny","Partly Sunny","Partly Cloudy","Mostly Cloudy","Rain"];

    for x in range(1,days):
        HiTemperature = generator(40, 100);
        LoTemperature = generator(0, HiTemperature);
        AverageWindSpeed = generator(0, 45);
        Conditions = conditions[generator(0, (len(conditions) - 1))];

        weatherreport = {'HiTemperature':HiTemperature, 'LoTemperature':LoTemperature, 'AverageWindSpeed':AverageWindSpeed, 'Conditions':Conditions}

        forecast.append(weatherreport)
 
    print(json.dumps(forecast))

    return forecast

    

def weather(event, context):
    

   
    print(event)
    latitude = event["queryStringParameters"]['lat']
    longitude = event["queryStringParameters"]['long']

    
    response = {
        "statusCode": 200,
        "body": json.dumps(RandomWeather(6), indent=4)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
