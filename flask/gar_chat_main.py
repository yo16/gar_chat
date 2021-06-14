import os
import random, string
import datetime
import glob
from flask import Flask, render_template, request, send_from_directory


LOG_DIR = './room_log/'

app = Flask(__name__)

def get_room_no():
    room_no_length = 20
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(room_no_length)]
    return ''.join(randlst)


def room_init(no):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(f'{LOG_DIR}{no}.txt', mode='w', encoding='utf-8') as f:
        f.write('')


def put_logs(no, un, ch):
    dt_now = datetime.datetime.now()
    time_stamp = dt_now.strftime('%Y/%m/%d %H:%M:%S')
    with open(f'{LOG_DIR}{no}.txt', mode='a', encoding='utf-8') as f:
        f.write(f'{un}\t{time_stamp}\t{ch}\n')


def get_logs(no):
    ret_obj = []
    with open(f'{LOG_DIR}{no}.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            uname, time_stamp, chat = line.split('\t')
            ret_obj.append({'uname':uname, 'time': time_stamp, 'chat':chat})
    
    return ret_obj


def show_page(room_no='', uname='', logs=[]):
    return render_template('chat_main.html', cur_url=request.url, room_no=room_no, uname=uname, logs=logs)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico',)


@app.route('/', methods=['GET','POST'])
def top():
    uname = ''
    room_no = ''
    logs = []
    if request.method == 'POST':
        uname = request.form['uname']
        room_no = request.form['room_no']
        chat = request.form['chat']

        if len(uname)>0 and len(chat)>0:
            # 書き込み
            put_logs(room_no, uname, chat)

        # ログファイルを取得
        logs = get_logs(room_no)

    else:
        # ルーム番号を取得
        room_no = get_room_no()
        
        # 部屋初期化
        room_init(room_no)
    
    return show_page(room_no=room_no, uname=uname, logs=logs)


@app.route('/<string:room_no>')
def show_room(room_no):
    logs = get_logs(room_no)
    if len(logs)==0:
        return show_page()
        
    return show_page(room_no=room_no, uname='', logs=logs)


def delete_lod_logs():
    del_files = []
    # ログフォルダ内の全ファイルの更新日時を見る
    for log_file in glob.glob(f'{LOG_DIR}*'):
        stat_result = os.stat(log_file)
        dt = datetime.datetime.fromtimestamp(stat_result.st_mtime)
        # print(log_file)
        # print(dt)
        spent_time_s = datetime.datetime.now() - dt
        if spent_time_s.days > 1:
            # ２日以上経ってたら消す
            del_files.append(log_file)
    
    # 消す
    for log_file in del_files:
        print(f'Removed log file "{log_file}".')
        os.remove(log_file)


if __name__ == "__main__":
    # 古いファイルを消す
    delete_lod_logs()

    app.run(debug=True, host='0.0.0.0')
