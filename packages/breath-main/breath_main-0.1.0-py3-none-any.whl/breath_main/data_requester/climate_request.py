import requests, json, pdb, datetime

def get_clima(city_name, print_in_terminal=True):

	url = "https://community-open-weather-map.p.rapidapi.com/climate/month"

	city = city_name

	querystring = {"q":city}

	headers = {
	    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
	    'x-rapidapi-key': "24117470c7msh69c4f7f119cb290p144f8djsnfa7d413f68a3"
	    }

	response = requests.request("GET", url, headers=headers, params=querystring)

	result = None

	clima_data = None
	if response.status_code == 200:
		clima_data = response.json()

	for item in clima_data['list']:
		prev = datetime.datetime.fromtimestamp(int(item['dt']))
		now = datetime.datetime.now()

		if prev > now:
			if(print_in_terminal):

				print(f"Para {city}, na hora:", prev)
				print("Umidade",round(item['humidity']),"%")
				print("Pressão",round(item['pressure']),"Pa")
				print("Máxima",round(item['temp']['average_max']-273,1),"ºC")
				print("Mínima",round(item['temp']['average_min']-273,1),"ºC")

			result = {}
			result["Umidade"] = item['humidity']
			result["Temp_max"] = item['temp']['average_max']-273
			result["Temp_min"] = item['temp']['average_min']-273
			result["Pressao_at_max"] = item["pressure"]
			result["Pressao_at_min"] = item["pressure"]
			result["Velocidade_vent"] = item["wind_speed"]
			break

	if clima_data is not None:
		# Airmine AQI endpoint
		endpoint = "https://pm251.p.rapidapi.com/aqi"
		# Coordinates of Berlin
		coordinates = {
			"lat": clima_data['city']['coord']['lat'],
			"lon": clima_data['city']['coord']['lon']
		}
		# Custom headers
		headers = {
			'x-rapidapi-host': "pm251.p.rapidapi.com/aqi",
			'x-rapidapi-key': "24117470c7msh69c4f7f119cb290p144f8djsnfa7d413f68a3"
		}

		# Execute a GET request
		response = requests.request(
			  "GET", endpoint,
			  headers = headers, params = coordinates
		)

		air_data = None
		if response.status_code == 200:
			air_data = response.json()

		if air_data is not None:
			n = len(air_data['forecasts'])	
			for item in air_data['forecasts']:
				date = item['date']
				d1 = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
				d2 = datetime.datetime.now()
				pm25 = item['values'][0]['value']
				if (d1 > d2):
					print("%s | %d pm25" % (date, pm25))
					break
				else:
					print(date, 'futuro')	
			#remaining = int(response.headers['x-ratelimit-requests-remaining'])
	 		#print("You have %d requests left" % remaining)
		else:
			if(print_in_terminal):
				print("Nao pudemos achar os dados de qualidade do ar para sua cidade")
	else:
		if(print_in_terminal):
			print("Nao possuimos informacoes da sua cidade")

	return result
