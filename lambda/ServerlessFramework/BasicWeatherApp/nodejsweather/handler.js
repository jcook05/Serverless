'use strict'
const querystring = require('querystring')


function generator(min, max) {

  // return whole number Math.floor rounds
  return Math.floor(Math.random() * (max - min) + min);
}


function RandomWeather(lat, long, days) {

  // Conditions Array

  var conditions = ["Sunny","Mostly Sunny","Partly Sunny","Partly Cloudy","Mostly Cloudy","Rain"];
  
  // Forecast Array
  var forecast = new Array()

  console.log("Modal to review questions and edit or submit")
  console.log(lat)
  console.log(long)
  
  var obj = new Object();

  
  var test = generator(0, (conditions.length - 1))
  console.log(test)

  for (var i = 1; i < days; i++) {

    obj.HiTemperature = generator(40, 100);
    obj.LoTemperature = generator(0, obj.HiTemperature);
    obj.AverageWindSpeed = generator(0, 45);
    obj.Conditions = conditions[generator(0, (conditions.length - 1))];
   
  var jsonString = JSON.stringify(obj);    

  forecast.push(obj)



  }
  

  console.log(forecast.length)
  console.log(forecast[0].HiTemperature)
  console.log(forecast[0].LoTemperature)
  console.log(forecast[0].AverageWindSpeed)
  console.log(forecast[0].Conditions)
  console.log(jsonString)
 
  var newstring = JSON.stringify(forecast)

  console.log(newstring)


  return forecast;
  
  
}

var NewWeather = RandomWeather(35.5, 40.75, 6)

module.exports.weather = (event, context, callback) => {

  var latitude = querystring.parse(event.body).lat
  var longitude = querystring.parse(event.body).long

  var WeatherReport = RandomWeather(latitude, longitude, 6)

  var jsonString = JSON.stringify(WeatherReport, null, 4);   

  const response = {
    statusCode: 200,
    body: jsonString,
  };

  callback(null, response);

  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // callback(null, { message: 'Go Serverless v1.0! Your function executed successfully!', event });
};
