from flask import Flask,render_template,send_from_directory,request,jsonify
import os,requests
from datetime import datetime

app = Flask(__name__) 

uploadPath = "uploads"
# n8n Webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/new-image"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/<name>/images/')
def user(name):
    return 'Hello {} my master'.format(name)




@app.route('/uploads/<path:filename>',methods=["GET"])
def upanddown(filename):
    return send_from_directory(uploadPath,filename)

@app.route('/uploads',methods=["POST"])
def uploadgimmic():
## เช็ค 'file' ได้จาก request.files ได้เพราะเราต้องเข้าถึง url= http://host.docker.internal:8000/uploads ก่อน request ถึงจะมี requset.files ได้, ซึ่ง มันรอจนกว่าจะมีคนเข้าถึง def(function) นี้ถึงทำงาน
    if 'file' not in request.files:
        return jsonify({'error':"NO detect file"}),400
    
    file = request.files['file']

    filePath = os.path.join("uploads",file.filename)
    file.save(filePath)

    # สร้าง URL สำหรับดาวน์โหลด
    get_url_path = f"http://host.docker.internal:8000/uploads/{file.filename}"

    ## แจ้ง n8n ว่ามีไฟล์ใหม่ (ส่ง metadata ไป)
    try:

        file_info = {
            "filename": file.filename,
            "url": get_url_path,    ## โยนให้เป็น get _ http://host.docker.internal:8000/
            "timestamp": datetime.now().isoformat(),
            "size": os.path.getsize(filePath),
            "path": filePath
        }

        notify_response = requests.post(
            N8N_WEBHOOK_URL,
            json=file_info,
            timeout=5
        )
        print(notify_response.status_code)
        
    except requests.exceptions.ConnectionError:
        print("n8n no connection")

    return jsonify({
        "message":"Good point you uploaded files",
        "filename": file.filename,
        "url":get_url_path   ## โยนให้เป็น get
    }),201

if __name__ == "__main__":
    app.run(port=8000, debug=False)