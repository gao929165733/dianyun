# encoding:utf-8
import os
from publicMethod import mkdir, converter, segRoot, LASmerge, wayTXTcrossfile, wayTXTdangerfile, wayTXTtowerfile
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import send_from_directory
from flask import send_file
from flask import make_response
from werkzeug import secure_filename
from flask import redirect
from flask import json, jsonify
import shutil



# 上传文件后缀检查
ALLOWED_EXTENSIONS = set(['ply', 'laz', 'las', 'xyz', 'ptx', 'binary'])
txtToJson_Path_All = set(['txt'])
# 上传路径
UPLOAD_FOLDER = 'G:\\python\\the_dianyun\\static\\projects'

txtToJson_Path = os.path.join(os.path.dirname(__file__), 'jsonFile')
print(txtToJson_Path)

# 转化变量
converterCmd = r"G:\A点云workplace\PotreeConverter\master\PotreeConverter\PotreeConverter.exe"
global project_path


app = Flask(__name__)
# app = Flask(__name__, static_folder='', static_url_path='')

# 生成文件访问的url
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['txtToJson_Path'] = txtToJson_Path
# 编码
app.config['JSON_AS_ASCII'] = False

# ~主页
@app.route('/')
def index():
    # return render_template('show.html')
    return render_template('index.html')


# ~浏览目录
@app.route('/select_prj', methods=['POST', 'GET'])
def select_prj(name=None):
    error = None
    if request.method == 'POST':
        selPro_name = request.form['project']
        print('sel_project: '+selPro_name)
        project_path = os.path.join(UPLOAD_FOLDER, selPro_name)
        print(project_path)
        isExists = os.path.exists(project_path)
        if not isExists:
            return render_template('error.html')
        else:
            temp = render_template('show.html',result=selPro_name)
            response = make_response(temp)
            return response


# ~创建目录
@app.route('/create_prj', methods=['POST', 'GET'])
def create_prj():
    error = None
    if request.method == 'POST':
        global crePro_name
        crePro_name = request.form['project']
        print(crePro_name)
        global project_path
        project_path = os.path.join(UPLOAD_FOLDER, crePro_name)
        print(project_path)
        if mkdir(project_path):
            return 'ok'
            # return redirect(url_for('index'))
        else:
            return '文件夹已经存在'
    else:
        return 'error'



# ~删除目录
@app.route('/delete_pri', methods=['POST', 'GET'])
def delete_prj():
    error = None
    if request.method == 'POST':
        delPro_name = request.form['project']
        print('project_name '+delPro_name)
        project_path = os.path.join(UPLOAD_FOLDER, delPro_name)
        print('project_path'+project_path)
        if delPro_name == '':
            return render_template('error.html')
        elif os.path.exists(project_path):
            shutil.rmtree(project_path)
            return render_template('ok.html')
        else:
            return render_template('error.html')


# ~文件上传
# 文件后缀名检查
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# 上传
@app.route('/file_upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['myFile']
        if file and allowed_file(file.filename):
            filename = file.filename
            print('filename  ' + file.filename)

            # # 创建文件夹
            # filePro = filename.rsplit('.')[0]
            # the_result = filePro
            # filePro = os.path.join(CONVERT_DATE, filePro)
            # global project_path_1
            # project_path_1 = filePro
            # if mkdir(filePro):
            #     file_path = os.path.join(filePro, filename)
            #     file.save(file_path)
            #     print('file_path  ' + file_path)
            #     # potreeConver
            #     the_input = file_path
            #     the_output = filePro
            #     # converter(converterCmd, the_input, 'try', the_output, None, 1, None, None)
            #     converter(converterCmd, the_input, None, the_output, None, 1, None, None)
            #
            #     the_url = "static/dotDate/" + the_result + "/cloud.js"
            #     response = make_response(the_url)
            #     print('--------------------',response)
            #
            #     return response
            # else:
            #     return '文件夹已经存在'

            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            print('file_path  ' + file_path)
            # potreeConver
            global project_path
            print('project_path  ' + project_path)
            the_input = file_path
            the_output = project_path
            # converter(converterCmd, the_input, 'try', the_output, None, 1, None, None)
            converter(converterCmd, the_input, None, the_output, None, 1, None, None)
            global crePro_name
            print('global crePro_name', crePro_name)
            return render_template('convert.html', result=project_path)
        else:
            return render_template('error.html')

# 转换
@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        # 可视化
        if request.form['submit_button'] == 'view':
            view_pro = segRoot(project_path)
            temp = render_template('show.html',result=view_pro)
            response = make_response(temp)
            return response
        # 数据下载
        elif request.form['submit_button'] == 'dataDownload':
            in_path = os.path.join(project_path, 'data\\r')
            out_path = os.path.join(project_path, 'data.las')
            if LASmerge(in_path, out_path):
                return render_template('ok.html')
            else:
                return render_template('error.html')
        # 删除文件夹
        else:
            if os.path.exists(project_path):
                shutil.rmtree(project_path)
                return render_template('ok.html')
            else:
                return render_template('error.html')
    elif request.method == 'GET':
        return render_template('index.html')


# ~txtToJson
from werkzeug import secure_filename
def txt_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in txtToJson_Path_All
# 交跨点
@app.route('/TXTcrossfile', methods=['GET', 'POST'])
def TXTcrossfile():
    if request.method == 'POST':
        file = request.files['cross-uploadTXT']
        if file and txt_file(file.filename):
            filename = secure_filename(file.filename)

            txtPath = os.path.join(txtToJson_Path, filename)
            file.save(txtPath)

            print('--txtPath--', txtPath)
            return jsonify(wayTXTcrossfile(txtPath))
    return True

# 危险点
@app.route('/uploadDangerTXT', methods=['GET', 'POST'])
def uploadDangerTXT():
    if request.method == 'POST':
        file = request.files['danger-uploadTXT']
        if file and txt_file(file.filename):
            filename = secure_filename(file.filename)

            txtPath = os.path.join(txtToJson_Path, filename)
            file.save(txtPath)

            print('--txtPath--', txtPath)
            return jsonify(wayTXTdangerfile(txtPath))
    return True

# 杆塔
@app.route('/uploadTowerTXT', methods=['GET', 'POST'])
def TXTtowerfile():
    if request.method == 'POST':
        file = request.files['tower-uploadTXT']
        if file and txt_file(file.filename):
            filename = secure_filename(file.filename)

            txtPath = os.path.join(txtToJson_Path, filename)
            file.save(txtPath)

            print('--txtPath--', txtPath)
            return jsonify(wayTXTtowerfile(txtPath))
    return True



if __name__ == '__main__':
    port = 5000
    app.debug = True
    app.run('',port)