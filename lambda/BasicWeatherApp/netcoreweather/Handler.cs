using Amazon.Lambda.Core;
using Amazon.Lambda.APIGatewayEvents;
using System;
using System.Net;
using System.Collections.Generic;
using Newtonsoft.Json;

[assembly:LambdaSerializer(typeof(Amazon.Lambda.Serialization.Json.JsonSerializer))]

namespace WeatherService
{

    public class WeatherReport
    {
        private static readonly string[] PossibleConditions = new string[]
        {
            "Sunny",
            "Mostly Sunny",
            "Partly Sunny",
            "Partly Cloudy",
            "Mostly Cloudy",
            "Rain"
        };

        public WeatherReport(double latitude, double longitude, int daysInFuture)
        {
            var generator = new Random((int)(latitude + longitude) + daysInFuture);

            HiTemperature = generator.Next(40, 100);
            LoTemperature = generator.Next(0, HiTemperature);
            AverageWindSpeed = generator.Next(0, 45);
            Conditions = PossibleConditions[generator.Next(0, PossibleConditions.Length - 1)];
        }

         public int HiTemperature { get; }
         public int LoTemperature { get; }
         public int AverageWindSpeed { get; }
         public string Conditions { get; }
    }

    
    
    public class Handler
    {
      public APIGatewayProxyResponse Hello(APIGatewayProxyRequest request, ILambdaContext context)
        {

        string GetParms(IDictionary<string, string> qsParms, string parmName)
        {
            var result = string.Empty;
            if (qsParms != null)
            {
                if (qsParms.ContainsKey(parmName))
                {
                    result = qsParms[parmName];
                }
            }
            return result;

        }
          
          // Log entries show up in CloudWatch
          context.Logger.LogLine("Example log entry\n");

          double latitude = Convert.ToDouble(GetParms(request.QueryStringParameters, "lat"));
          double longitude = Convert.ToDouble(GetParms(request.QueryStringParameters, "long"));

           
            
          // Generating random weather forecast.   This could easily be a call to a national weather service API
          var forecast = new List<WeatherReport>();
          for (var days = 1; days < 6; days++)
            {
                forecast.Add(new WeatherReport(latitude, longitude, days));
            }
          var jsonresponse = JsonConvert.SerializeObject(forecast, Formatting.Indented);
                
         
          var response = new APIGatewayProxyResponse
            {
              StatusCode = (int)HttpStatusCode.OK,
              Body = jsonresponse,
              Headers = new Dictionary<string, string> {{ "Content-Type", "application/json" }}
            };

        return response;
        }
    }
    
}
