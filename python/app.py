from flask import Flask as _Flask, jsonify, flash, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask import render_template
from json import JSONEncoder
import utils
import time
import os

class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


class Flask(_Flask):
    json_encoder = JSONEncoder


app = Flask(__name__)
app.secret_key = 'your_unique_secret_key'  # 设置秘密密钥
CORS(app)

#管理用户
@app.route('/api/getUserNum', methods=['GET'])
def get_data_num():
    res = utils.get_user_num();
    print(res)
    return jsonify({'num':res});
@app.route('/api/getUserData', methods=['POST'])
def get_user_data():
    data = request.get_json()
    page_size = data.get('page_size')
    current_page = data.get('current_page')
    res = utils.get_user_data(page_size,current_page);
    return res;
@app.route('/api/deleteUser', methods=['POST'])
def delete_user_data():
    if request.method == 'POST':
        try:
            # 从请求体中获取要删除的数据的 ID 列表
            data = request.get_json()
            ids = data.get('ids', [])
            # 执行删除操作
            utils.delete_user_data(ids)

            return jsonify({'message': 'Data deleted successfully'}), 200
        except Exception as e:
            print('Error occurred while deleting data:', e)
            return jsonify({'message': 'Failed to delete data'}), 500
@app.route('/api/uploadUser', methods=['POST'])
def upload_user_data():
    if request.method == 'POST':
        try:
            # 解析从前端传递过来的JSON数据
            data = request.json
            utils.upload_user_data(data)
            
            return jsonify({"message": "Data inserted successfully"}), 200
        except Exception as e:
            print('Error occurred while inserting data:', e)
            return jsonify({"message": f"Failed to insert data: {str(e)}"}), 500
@app.route('/api/updateUser', methods=['POST'])
def update_user_data():
    if request.method == 'POST':
        try:
            # 解析从前端传递过来的JSON数据
            data = request.json
            utils.update_user_data(data)
            
            return jsonify({"message": "Data updated successfully"}), 200
        except Exception as e:
            print('Error occurred while updating data:', e)
            return jsonify({"message": f"Failed to update data: {str(e)}"}), 500
        
if __name__ == '__main__':
    # 端口号设置
    app.run(host="127.0.0.1", port=5000)
