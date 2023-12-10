import pytest

from api import Petfrfiends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password
import os

pf = Petfrfiends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):

    """ Проверяем что запрос всех питомцев возвращает не пустой список."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_without_photo(name='Пушок', animal_type='Кролик',
                                     age=1):

    """Проверяем, что можно добавить питомца с корректными данными без фото"""


    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_valid_data(name='Лапа', animal_type='Кролик',
                                     age=1, pet_photo='images/112af7570ccf23890d9fa3876eeee53e.jpeg'):

    """Проверяем, что можно добавить питомца с корректными данными с фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_update_pet_info_with_valid_data(name='Кроль', animal_type='Кролик', age=1):

    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter= 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Список питомцев пуст.')


def test_successful_delete_pet():

    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key,  filter="my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, name="Дог", animal_type="Собака", age=3)
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, filter= "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):

    """Проверяем возможноть получения API-ключа неавторизованным пользователем"""

    status, result = pf.get_api_key(email, password)
    with pytest.raises(AssertionError):
        assert status == 200

def test_get_api_key_with_blank_email(email=None, password=valid_password):

    """Проверяем возможноть получения API-ключа с пустым полем email"""

    status, result = pf.get_api_key(email, password)
    with pytest.raises(AssertionError):
        assert status == 200

def test_get_api_key_with_blank_password(email=valid_email, password=None):

    """Проверяем возможноть получения API-ключа с пустым полем password"""

    status, result = pf.get_api_key(email, password)
    with pytest.raises(AssertionError):
        assert status == 200

def test_add_new_pet_with_incorrect_data(name=215, animal_type=1111,
                                     age=1):
    """Проверяем возможность добавитоь питомца с некорректными данными (В поля "Имя" и "Порода"
    введен числовой формат, вместо строки"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    with pytest.raises(AssertionError):
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_with_blank_name(name=None, animal_type="Кот",
                                     age=1):
    """Проверяем возможность добавитоь питомца с пустым значениеум имени"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    with pytest.raises(AssertionError):
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_with_blank_animal_type(name="Яма", animal_type=None,
                                     age=1):
    """Проверяем возможность добавитоь питомца с пустым значениеум породы питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    with pytest.raises(AssertionError):
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_with_blank_age(name="Яма", animal_type="Черепаха",
                                     age=None):
    """Проверяем возможность добавитоь питомца с пустым значениеум возраста"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    with pytest.raises(AssertionError):
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_with_negative_value(name="Китя", animal_type="Кошка", age= -2):

    """Проверяем возможность создания питомца с отрицательным значнеием возраста"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    """В API баг, тест проходить не должен"""

def test_add_new_pet_with_negative_value(name="Китя", animal_type="Кошка", age= "abc"):

    """Проверяем возможность создания питомца со строковым форматом в значении возраста, вместо числового"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    """В API баг, тест проходить не должен"""

def test_update_pet_info_with_valid_data(name=1111, animal_type='крокодил', age=1):

    """Проверяем возможность обновления информации о питомце с некорректным значением имени"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter= 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        with pytest.raises(AssertionError):
            assert status == 200
            assert result['name'] == name
    else:
        raise Exception('Список питомцев пуст.')
