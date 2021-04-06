import os
import requests


path = os.getcwd() + "/tests/test_image.jpg"
print(path)

resp = requests.post("http://ziyiewe.aiap.okdapp.tekong.aisingapore.net/predict",
                     files={"image_path": path})
print(resp.json())

resp = requests.get("http://ziyiewe.aiap.okdapp.tekong.aisingapore.netinfo")

#resp = requests.get('http://localhost:5000/')

print(resp)
