import pytest
import requests
import os
import json
from src import SberClient
from config import settings

@pytest.fixture
def corupted_body_payload():
  """Делаем фикстуру с некорректным Body  для функционального теста"""
  return {
    "model":"GigaChat-2",
    "message":[{"role":"user","content":"Привет ГигаЧэд), что ты думаешь про Сбербанк?"}],
    "temperature":0.6,
    "max_tokens":23
  }

@pytest.fixture
def correct_body_payload():
  return json.dumps({
  'model': 'GigaChat',
  'messages': [
    {
      'role': 'system',
      'content': 'Ты — профессиональный переводчик на английский язык. Переведи точно сообщение пользователя.'
    },
    {
      'role': 'user',
      'content': 'GigaChat — это сервис, который умеет взаимодействовать с пользователем в формате диалога, писать код, создавать тексты и картинки по запросу пользователя.'
    }
  ],
  'update_interval': 0
},ensure_ascii=False,indent=2)


@pytest.fixture
def change_top_p():
        return json.dumps({
  'model': 'GigaChat',
  'messages': [
    {
      'role': 'system',
      'content': 'Ты — профессиональный переводчик на английский язык. Переведи точно сообщение пользователя.'
    },
    {
      'role': 'user',
      'content': 'GigaChat — это сервис, который умеет взаимодействовать с пользователем в формате диалога, писать код, создавать тексты и картинки по запросу пользователя.'
    }
  ],
  'top_p': {input_data},
  'update_interval': 0
},ensure_ascii=False,indent=2)



@pytest.fixture
def sber_api_client():
  return  SberClient()
