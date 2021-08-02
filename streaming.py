#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify, Response 
import cv2
import io

app = Flask(__name__) # 플라스크 앱 생성
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

@app.route('/') # 기본('/') 웹주소로 요청이 오면                     
def hello(): # hello 함수 실행
    return "Hello world"

@app.route("/user/<username>")
def user(username):
    return jsonify({'name': username})


def gen():
    """Video streaming generator function."""
    while True:
        ret, frame = capture.read()
        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')

        
@app.route("/cam")
def cam():
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == '__main__': # 현재 파일 실행시 개발용 웹서버 구동
    app.run(host='0.0.0.0', port=5051)