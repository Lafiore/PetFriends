import requests
import json
class Petfrfiends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key' : auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет на сервер с информацией о новом питомце без фото и возвращает статус запроса на сервер
        и результат в формате JSON"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """Метод отправляет на сервер с информацией о новом питомце с фото и возвращает статус запроса на сервер
        и результат в формате JSON"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers, data=data, files=file)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер и возвращает статус
        и результат в формате JSON с обновленной информацией о питомце"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.put(self.base_url+'api/pets/'+pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет запрос на сервер на удаление питомца по указанному ID и возвращает статус запроса
        и результат в формате JSON"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url+'api/pets/'+pet_id, headers=headers)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


