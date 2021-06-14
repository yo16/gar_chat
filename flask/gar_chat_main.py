import os
import random, string
import datetime
from flask import Flask, render_template, request


LOG_DIR = './room_log/'

app = Flask(__name__)

def get_room_no():
    room_no_length = 20
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(room_no_length)]
    return ''.join(randlst)


def room_init(no):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_DIR + no + '.txt', mode='w', encoding='utf-8') as f:
        f.write('')


def put_logs(no, un, ch):
    dt_now = datetime.datetime.now()
    time_stamp = dt_now.strftime('%Y/%m/%d %H:%M:%S')
    with open(LOG_DIR + no + '.txt', mode='a', encoding='utf-8') as f:
        f.write(un + '\t' + time_stamp + '\t' + ch + '\n')


def get_logs(no):
    ret_obj = []
    with open(LOG_DIR + no + '.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            uname, time_stamp, chat = line.split('\t')
            ret_obj.append({'uname':uname, 'time': time_stamp, 'chat':chat})
    
    return ret_obj


@app.route('/', methods=['GET','POST'])
def top():
    uname = ''
    room_no = ''
    logs = []
    if request.method == 'POST':
        uname = request.form['uname']
        room_no = request.form['room_no']
        chat = request.form['chat']

        if len(chat)>0:
            # 書き込み
            put_logs(room_no, uname, chat)

        # ログファイルを取得
        logs = get_logs(room_no)

    else:
        # ルーム番号を取得
        room_no = get_room_no()
        
        # 部屋初期化
        room_init(room_no)
    
    return render_template('chat_main.html', room_no=room_no, uname=uname, logs=logs)


if __name__ == "__main__":
    app.run(debug=True)
