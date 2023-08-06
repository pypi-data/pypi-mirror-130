# rida-dynamic-pricing

run this command in the root of the directory:

bash run.sh

See the ip address of the docker container:

dynamic_pricing_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dynamic_pricing)

Test it with 

bash tests.sh

Call the api with a post request at http://[ip]:2000/multi_stop_penalisation=true, posting a json string such as: 

{
  "timeWindows": {
    "10:00-11:00": {
      "lalamove": "15",
      "gogox": "20"
    }, 
    "11:30-12:00": {
      "lalamove": "16",
      "gogox": "22"
    }
  },
  "waypoints": [
    {
      "type": "PICKUP",
      "location": {
        "lat": 1.3068056000000001,
        "lng": 103.81013890000001
      },
      "items": [
        {
          "size": 5
        }
      ]
    },
    {
      "type": "PICKUP",
      "location": {
        "lat": 1.3493056,
        "lng": 103.8481944
      },
      "items": [
        {
          "size": 2
        }
      ]
    },
    {
      "type": "PICKUP",
      "location": {
        "lat": 1.3551388999999998,
        "lng": 103.8231944
      },
      "items": [
        {
          "size": 2
        }
      ]
    },
    {
      "type": "DROPOFF",
      "location": {
        "lat": 1.3565278,
        "lng": 103.9384722
      },
      "items": [
        {
          "size": 5
        }
      ]
    }
  ],
  "serviceType": "MINIVAN"
}

It will return the price:

{
        "10:00-11:00": 14.19,
        "11:30-12:00": 15.14
    }

