import requests
from typing  import Dict,Any,Optional
from config import settings
import os
import time
"""Класс описывающий методы и парметры для нашего апи запроса, так как у нас доступен только post запрос, только он и реализован
в дальнейшем можно масштабировать и добавлять новые методы если потребуеются"""

class SberClient:
	def __init__(self):
		self.secret_data = settings
		self.token = self._get_token()
	
	def _get_token(self):
		if os.path.exists(self.secret_data.token_file):
    			with open(self.secret_data.token_file, 'r') as f:
        			token_data = f.read().strip().split('|')
        			if len(token_data) == 2 and float(token_data[1]) > time.time():
            				return token_data[0]
		return self._refresh_token()


	def _refresh_token(self):
		payload={
  			'scope': 'GIGACHAT_API_PERS'
		}
		headers = {
  			'Content-Type': 'application/x-www-form-urlencoded',
  			'Accept': 'application/json',
  			'RqUID': '2cfa6b00-c202-40c0-8229-8db164e1b151',
  			'Authorization': f'Basic {self.secret_data.auth_key}'
		}

		response = requests.request("POST",self.secret_data.oauth_url , headers=headers, data=payload,verify=self.secret_data.cert)
        	
		if response.status_code == 200:
			token_data = response.json()
			access_token = token_data['access_token']
			expires_in = token_data.get('expires_in', 1800)
			expiry_time = time.time() + expires_in
			with open(self.secret_data.token_file, 'w') as f:
				f.write(f"{access_token}|{expiry_time}") 
			return access_token
		else:
			raise Exception(f"Token request failed: {response.status_code}")
    



	def post(self,message,headers: Optional[Dict] = None):
		self._get_token()
		default_headers = {"Content-Type":"application/json","Accept":"application/json","Authorization":f"Bearer {self.token}"}
		if headers:
			default_headers.update(header)
		print(f'Send {self.secret_data.chat_url} \n {default_headers}\n {message}')
		response = requests.request("POST",url=self.secret_data.chat_url,headers = default_headers,data=message,verify=self.secret_data.cert)
		return response
