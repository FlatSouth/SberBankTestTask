import pytest
import allure
import json
import requests
from requests.exceptions import HTTPError
from unittest.mock import patch
from config import settings
from src import SberClient

@allure.epic("Прорвека функциональность с разными данными")
@allure.feature("Проверка двух тестов с ожидаемыми результами 200 и 400")
class TestCompletionsAPI:
	@pytest.mark.negative
	@allure.story("Ожидаемый ответ от сервера 400")
	def test_expected_400(self,sber_api_client,corupted_body_payload):
		with allure.step("Передача серверу неправильно сформиранного запроса"):
			response = sber_api_client.post(corupted_body_payload)
		with allure.step("Получение ответа от сервера с ожидаемым результатом 400"):
			assert response.status_code  == 400
	@pytest.mark.smoke
	@allure.story("Ожидаемый ответ от сервера 200")
	def test_expected_200(self,sber_api_client,correct_body_payload):
		with allure.step("Передача серверу правильно сформиранного запроса"):
			response = sber_api_client.post(correct_body_payload)
		with allure.step("Получение ответа от сервера с ожидаемым результатом 200"):
			assert response.status_code  == 200

	
	@pytest.mark.parametrize("input_data,expected",[ (0.2,200)
							,(0.7,200)
							,(-1,422)
							,(33,422)
	])
	@allure.story("Передаем различные параметры для поля top_p для проверки функционала сервиса, первые 2 значения валидные, остальные 2 проверяют значения превышающие границы")
	def test_change_top_p_value(self,sber_api_client,input_data,expected):
		with allure.step(f"Подготавливаем тело запроса с учетом данных которые приходят top_p = {input_data}"):
			data = {'model': 'GigaChat','messages': [{'role': 'system','content': 'Ты лучший гонщик в мире.'},{'role': 'user','content': 'Расскажи про самый классный автомобиль.'}],'top_p': input_data,'update_interval': 0} 
		response = sber_api_client.post(json.dumps(data,ensure_ascii=False,indent=2))
		with allure.step(f"Проверка ответа запроса и сравнение его с ожидаемым результатом top_p {input_data} expected {expected}"):
			assert response.status_code  == expected

	@allure.story("Мок тест для получения 429 ошибки")
	def test_mock_expected_429(self,sber_api_client,correct_body_payload):
		with allure.step("Подготовка мока"):
			mock_response = requests.Response()
			mock_response.status_code = 429
			mock_response.reason = "Too many Requests"
			mock_response.headers = {
				"Retry-After":"60",
				"X-RateLimit-Limit":"100",
				"X-RateLimit-Remaining":"0"
			}
		
		with patch('requests.request') as mock_post:
			mock_post.return_value = mock_response
			with pytest.raises(HTTPError) as info:
				with allure.step("Отправка серверу корректного запроса и обратка ошибки"):
					response = sber_api_client.post(correct_body_payload)
					response.raise_for_status()
		
		with allure.step("Сравнения ошибки и ожидаемого результата и выход из теста"):
			assert info.value.response.status_code == 429
		
