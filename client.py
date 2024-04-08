import requests

# # Запрос маршрутов
# response = requests.get(
#     'http://127.0.0.1:8000/api/v1/routes/',
# )
# print(response.status_code)
# print(response.text)

# # Запрос обновления маршрутов по категории "река"
# response = requests.get(
#     'http://127.0.0.1:8000/api/v1/routes/update/?filter=река'
# )
# print(response.status_code)
# print(response.text)

# Запрос стандартных маршрутов по категории "река"
response = requests.get(
    'http://127.0.0.1:8000/api/v1/bearroute/?filter=река'
)
print(response.status_code)
print(response.text)