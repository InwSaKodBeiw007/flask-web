from flask import Flask,render_template,send_from_directory,request,jsonify
import os

app = Flask(__name__) 

uploadPath = "uploads"

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
## เช็ค 'file' ได้จาก request.files ได้เพราะเราต้องเข้าถึง url= http://localhost:8000/uploads ก่อน request ถึงจะมี requset.files ได้, ซึ่ง มันรอจนกว่าจะมีคนเข้าถึง def(function) นี้ถึงทำงาน
    if 'file' not in request.files:
        return jsonify({'error':"NO detect file"}),400
    
    file = request.files['file']

    filePath = os.path.join("uploads",file.filename)
    file.save(filePath)

    return jsonify({
        "message":"Good point you uploaded files",
        "filename": file.filename,
        "url":f"/uploads/{file.filename}"
    }),201

if __name__ == "__main__":
    app.run(port=8000, debug=True)