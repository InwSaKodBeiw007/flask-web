import requests, os

filename = "storages/ผงแห่งจินตนาการ.png"
filePath = os.path.join("storages","ผงแห่งจินตนาการ.png")

# ส่ง POST ไปยัง Flask API

url = "http://localhost:8000/uploads"

with open(filePath,"rb") as photo:
    files = {"file":photo}
    response = requests.post(url=url,files=files)
    
try:
    print("Posted ", response.json())
except:
    print("no response",response.text)