from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import json
import data_utils
import webbrowser

# base_dir = '../front/'
base_dir = './'
app = Flask(__name__, 
            static_folder=base_dir+'dist/assets',
            template_folder=base_dir+'dist')
CORS(app, resources={r'/*':{'origins': '*'}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_all')
def return_all():
    return jsonify([{'name':'a'},{'id': 'b'}])

@app.route('/api/todo', methods=['POST'])
def create_todo():
    todo_info = request.json
    msg = data_utils.save_todo(json.dumps(todo_info))
    return jsonify({"msg":msg})

@app.route('/api/todo', methods=['PATCH'])
def update_todo_to_complete():
    info = request.json
    todo_hash = info['todo_hash']
    state =  info['state']
    msg = "please gave state value"
    if state == -1:
        return warp_msg(msg)
    msg = "todo_hash is null"
    if not todo_hash == 'null':
        msg = data_utils.change_todo_state(todo_hash,state)
    return warp_msg(msg)

@app.route('/api/todo', methods=['GET'])
def get_todo():
    state = request.args.get('state')
    state = int(state)
    msg = data_utils.get_todo_list(state)
    return warp_msg(msg)

@app.route('/api/todo/info', methods=['GET'])
def get_todo_info():
    todo_hash = request.args.get("todo_hash","null")
    return warp_msg(data_utils.get_todo_info(todo_hash))

@app.route('/api/todo/note', methods=['POST'])
def add_todo_note():
    post_info = request.json
    todo_hash = post_info['todo_hash']
    content = post_info['content']
    msg = data_utils.save_todo_note(todo_hash,content)
    return warp_msg(msg)

@app.route('/api/todo/note', methods=['GET'])
def get_note_content():
    todo_hash = request.args.get('todo_hash')
    note_hash = request.args.get('note_hash')
    if not note_hash == '':
        return warp_msg(data_utils.get_note_content(todo_hash, note_hash))
    return warp_msg(data_utils.get_todo_all_notes(todo_hash))

@app.route('/api/date/note', methods=['GET'])
def get_date_note():
    start = request.args.get("start")
    end = request.args.get("end")
    return jsonify(data_utils.get_date_notes(start, end))

@app.route('/api/note', methods=['GET'])
def get_todo_note():
    todo_hash = request.args.get("todo_hash")
    return warp_msg(data_utils.get_todo_all_notes(todo_hash))

def warp_msg(msg):
    return jsonify({"msg":msg})

if __name__ == '__main__':
    data_utils.init_all_directory()
    webbrowser.open_new_tab('http://127.0.0.1:5000')
    app.run()
