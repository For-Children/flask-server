#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify, Response 
import cv2

app = Flask(__name__) # 플라스크 앱 생성

@app.route('/') # 기본('/') 웹주소로 요청이 오면                     
def hello(): # hello 함수 실행
    return "Hello world"

@app.route("/user/<username>")
def user(username):
    return jsonify({'name': username})
        
@app.route("/cam")
def cam():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ret, frame = capture.read()
    
    _, img_encoded = cv2.imencode('.png', frame)
    response = img_encoded.tostring()
    
    return Response(response=response, status=200, mimetype='image/png')
    

if __name__ == '__main__': # 현재 파일 실행시 개발용 웹서버 구동
    app.run(host='0.0.0.0', port=9000)
    
    