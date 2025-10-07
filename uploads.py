from flask import Flask,render_template,send_from_directory,request,jsonify
import os,requests,threading
from datetime import datetime

app = Flask(__name__) 
latest_answer = None    ## จำเป็นต้องประกาศตัวแปรเด้อ

uploadPath = "uploads"
# n8n Webhook URL
# N8N_WEBHOOK_URL = "http://localhost:5678/webhook/new-image"
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/new-image"

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

    if file.filename == '':
        return jsonify({'error': "No selected file"}), 400
    
    filePath = os.path.join("uploads",file.filename)
    file.save(filePath)

    # สร้าง URL สำหรับดาวน์โหลด
    get_url_path = f"http://host.docker.internal:8000/uploads/{file.filename}"

    def send_n8n_webhook(file_info):
        ## แจ้ง n8n ว่ามีไฟล์ใหม่ (ส่ง metadata ไป)
        try:
            requests.post(
                url=N8N_WEBHOOK_URL,
                json=file_info,
                timeout=5
            )
        except requests.exceptions.ConnectionError:
            print("n8n no connection")

    file_info = {
        "filename": file.filename,
        "url": get_url_path,    ## โยนให้เป็น get _ http://host.docker.internal:8000/
        "timestamp": datetime.now().isoformat(),
        "size": os.path.getsize(filePath),
        "path": filePath
    }

    # Start a new thread to send the webhook
    webhook_thread = threading.Thread(target=send_n8n_webhook, args=(file_info,))
    webhook_thread.start()

    return jsonify({
        "message":"Good point you uploaded files",
        "filename": file.filename,
        "url":get_url_path   ## โยนให้เป็น get
    }),201

@app.route('/receive', methods=['GET','POST'])
def receive():
    data = request.json or {}
    data.get("answer")

    def on_new_answer(answer):
        # ส่งคำตอบไปให้ project.py POST ไป endpoint localhost://9000
        try:
            requests.post(url="http://localhost:9000/new-answer", json={"answer": data}, timeout=3)
        except Exception as e:
            print("Error sending :", e)

    threading.Thread(target=on_new_answer, args=(data,), daemon=True).start()

    return jsonify({"status": "ok", "received": data})


if __name__ == "__main__":
    app.run(port=8000, debug=False)