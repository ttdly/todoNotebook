import hashlib
import os
import json
import shutil
from datetime import datetime, timedelta

BASE_DIR=os.path.join(os.getcwd(), 'database')
DATE_DIR=os.path.join(BASE_DIR,'date')
TODO_DIR=os.path.join(BASE_DIR,'todo')
TODO_INDEX=os.path.join(TODO_DIR,'index')
TODO_WORKING=os.path.join(TODO_INDEX,'working')
TODO_COMPONETE=os.path.join(TODO_INDEX,'complete')
TODO_CANCEL=os.path.join(TODO_INDEX,'cancel')
DATE_INDEX_FILE=os.path.join(DATE_DIR,'date.list')

def init_all_directory():
    dirs = [DATE_DIR,TODO_DIR, TODO_COMPONETE,TODO_WORKING,TODO_CANCEL]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def get_format_date(symbol='-'):
    """获取格式化年月日

    Args:
        symbol (str, optional): 分隔符。 默认是 '-'。

    Returns:
        str: 格式化后的年月日
    """

    now = datetime.now()
    return f"{now.year}{symbol}{now.month}{symbol}{now.day}"

def get_date_notes(start,end):
    result = []
    start_obj = datetime.fromisoformat(start).replace(tzinfo=None)
    end_obj = datetime.fromisoformat(end).replace(tzinfo=None)
    today = datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d"))
    if end_obj > today:
        end_obj = today
    for date in dates_between(start_obj, end_obj):
        # print()
        result += get_one_day_note(date.strftime("%Y-%m-%d"))
    # date_list = os.listdir(DATE_DIR)
    # for iDate in date_list:
    #     date_path = os.path.join(DATE_DIR, iDate)
    #     note_list = os.listdir(date_path)
    #     for item in note_list:
    #         todo_hash = item.split('&')[0]
    #         todo_info = get_todo_info(todo_hash)
    #         result.append({
    #             'title': todo_info['title'],
    #             'start': iDate
    #         })
    return result

def get_one_day_note(date):
    date_path = os.path.join(DATE_DIR, date)
    if not os.path.exists(date_path):
        return []
    result = []
    note_list = os.listdir(date_path)
    for item in note_list:
        todo_hash = item.split('&')[0]
        todo_info = get_todo_info(todo_hash)
        result.append({
            'title': todo_info['title'],
            'start': date,
            'color': f"#{todo_hash[:6]}"
        })
    return result

def save_file_index_by_date(store_file_name):
    date_dir = os.path.join(DATE_DIR, datetime.now().strftime("%Y-%m-%d"))
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    file_name = os.path.join(date_dir, store_file_name)
    create_empty_file(file_name)

def save_note_content(content,dir):
    """以摘要为名保存信息

    Args:
        message (str): 需要存储的消息
        directory (str, optional): 存储文件的目录。 默认是 './'

    Returns:
        str: 消息的 md5 摘要
    """
    date=f"# {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n"
    content = date + content
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    file_name = os.path.join(dir, content_hash)
    with open(file_name, "w", encoding='utf-8') as file_obj:
        file_obj.write(content)
    return content_hash

def save_todo(info=""):
    """存储TODO

    Args:
        info (str, optional): TODO的信息。默认为空

    Returns:
        str: 成功返回 hash，否则返回错误
    """
    todo_hash = hashlib.md5(info.encode("utf-8")).hexdigest()
    info_obj = json.loads(info)
    info_obj['hashCode'] = todo_hash
    info_obj['createDate'] = datetime.now().strftime("%Y-%m-%d")
    info = json.dumps(info_obj)
    todo_dir = os.path.join(TODO_DIR, todo_hash)
    todo_info_path = os.path.join(todo_dir, 'info.json')
    todo_notes_dir = os.path.join(todo_dir, 'notes')
    try:
        os.mkdir(todo_dir)
        with open(todo_info_path, "w", encoding="utf-8") as info_file:
            info_file.write(info)
        os.mkdir(todo_notes_dir)
        save_todo_to_working(todo_hash)
        return todo_hash
    except Exception as e:
        return f"Error: {e}"

def save_todo_note(todo_hash, content):
    todo_dir = os.path.join(TODO_DIR, todo_hash)
    todo_notes_dir = os.path.join(todo_dir, 'notes')
    content_hash = save_note_content(content ,todo_notes_dir)
    file_name = todo_hash+"&"+content_hash
    save_file_index_by_date(file_name)
    return file_name

def save_todo_to_working(hash):
    file_name = os.path.join(TODO_WORKING, hash)
    create_empty_file(file_name)

def change_todo_state(todo_hash, state):
    # 首先在 info.json 中修改
    todo_dir = os.path.join(TODO_DIR, todo_hash)
    todo_info_path = os.path.join(todo_dir, 'info.json')
    with open(todo_info_path, 'r', encoding="utf-8") as file_obj:
        todo_info = json.load(file_obj)
    if todo_info['state'] == state:
        return "complete value is not change"
    src = os.path.join(get_state_dir(todo_info['state']),todo_hash)
    todo_info['state'] = state
    if state == 1:
        todo_info['completeDate'] = datetime.now().strftime("%Y-%m-%d")
    with open(todo_info_path, 'w', encoding="utf-8") as file_obj:
        json.dump(todo_info, file_obj, ensure_ascii=False)
    # 然后在文件列表中修改
    dst = os.path.join(get_state_dir(state),todo_hash)
    shutil.move(src, dst)
    return "success"

def get_todo_info(todo_hash):
    todo_dir = os.path.join(TODO_DIR, todo_hash)
    todo_info_path = os.path.join(todo_dir, 'info.json')
    with open(todo_info_path, 'r+', encoding="utf-8") as file_obj:
        todo_info = json.load(file_obj)
    return todo_info

def get_todo_list(state):
    result = []
    dir = TODO_WORKING
    if state == 1:
        dir = TODO_COMPONETE
    elif state == 2:
        dir = TODO_CANCEL
    todos = os.listdir(dir)
    for todo in todos:
        result.append(get_todo_info(todo))
    sorted_tasks = sorted(result, key=lambda x: (x['level'], x['createDate']))
    return sorted_tasks

def get_note_content(todo_hash, note_hash):
    todo_dir = os.path.join(TODO_DIR, todo_hash)
    note_path = os.path.join(todo_dir, 'notes' ,note_hash)
    if not os.path.exists(note_path):
        return f"file not exists {note_path}"
    with open(note_path, 'r', encoding='utf-8') as file_obj:
        content = file_obj.read()
    return content

def get_todo_all_notes(todo_hash):
    todo_notes_dir = os.path.join(TODO_DIR,todo_hash,'notes')
    note_list = os.listdir(todo_notes_dir)
    msg = ''
    for note in note_list:
        note_path = os.path.join(todo_notes_dir, note)
        with open(note_path, 'r', encoding='utf-8') as file:
            msg += f"{file.read()}\n"
    return msg

def create_empty_file(file_name):
    with open(file_name,'w') as file:
        file.write('')

def get_state_dir(state):
    if state == 0:
        return TODO_WORKING
    if state == 1:
        return TODO_COMPONETE
    return TODO_CANCEL

def dates_between(start, end):
    if start > end:
        start, end = end, start
    date_list = [start]
    current = start
    while current <= end:
        date_list.append(current)
        current += timedelta(days=1)
    
    return date_list


if __name__ == "__main__":
    todo_hash = '551cb72593e6244c3c8737b098c77538'
    # get_todo_all_notes(todo_hash)
    # unittest.main()
    # get_todos_name_by_date('2024-2-28')
    # init_all_directory()
    # print(save_todo("{a:'b','c':'d'}"))
    # print(save_todo_note(todo_hash,'hello2'))
    print(get_date_notes('2024-02-26T00:00:00+08:00','2024-04-08T00:00:00+08:00'))
    # print(change_todo_to_complete(todo_hash,1))
    # print(os.getcwd())
    # E:\code\Web\notebook\server\database\todo