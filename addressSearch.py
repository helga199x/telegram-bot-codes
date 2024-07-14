from opencage.geocoder import OpenCageGeocode
import requests

class OpenCageAPIWrapper:
    def __init__(self):
        api_key = 'API_KEY'
        self.api_key = api_key
        self.geocoder = OpenCageGeocode(api_key)

    def get_possible_addresses(self, input_string, limit=5):
        results = self.geocoder.geocode(input_string, no_annotations='1', limit=limit)
        if results:
            addresses = []
            print(results)
            for result in results:
              city = result.get('components').get('village')
              if not city:
                city = result.get('components').get('city')
              road = result.get('components').get('road')
              if city and road:
                addresses.append(f'{city}, {road}')
            
            if len(addresses) == 0:
               return "Не удалось найти адрес. Попробуйте другой вариант или уточните запрос."
            else:
               return addresses
        else:
            return "Не удалось найти адрес. Попробуйте другой вариант или уточните запрос."