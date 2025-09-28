from dotenv import dotenv_values

class Settings():
	values = dotenv_values()	
	chat_url = values["CHAT_URL"]
	auth_key = values["AUTH_KEY"]
	oauth_url = values["OAUTH_URL"]
	token_file = values["TOKEN_FILE"]
	cert = values["CERT_FILE"]

settings = Settings()
