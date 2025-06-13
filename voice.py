from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
import mysql.connector
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# アップロードフォルダの設定
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gemini AIの設定
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# データベース接続設定
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'voicies'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_to_database(audio_path, dictation_text):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 現在のタイムスタンプ
        current_time = datetime.now()
        
        # データの挿入
        query = """
        INSERT INTO consultations 
        (dictation_text, audio_file_path, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (dictation_text, audio_path, current_time, current_time))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"データベースエラー: {e}")
        return False

@app.route('/')
def index():
    return render_template('voice_index.html')

@app.route('/voice_result', methods=['POST'])
def voice_result():
    if 'voice' not in request.files:
        flash('ファイルが選択されていません', 'error')
        return redirect(url_for('index'))
    
    file = request.files['voice']
    if file.filename == '':
        flash('ファイルが選択されていません', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # ファイル名を安全に処理
        filename = secure_filename(file.filename)
        
        # アップロードフォルダが存在しない場合は作成
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # ファイルの保存
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Gemini AIを使用して文字起こし
            model = genai.GenerativeModel('gemini-pro')
            # ここで音声ファイルをテキストに変換する処理を実装
            # 仮の文字起こしテキスト
            dictation_text = "これは仮の文字起こしテキストです。"
            
            # データベースに保存
            if save_to_database(file_path, dictation_text):
                flash('音声ファイルの処理が完了しました', 'success')
            else:
                flash('データベースへの保存に失敗しました', 'error')
            
            return render_template('voice_result.html', 
                                 voice_input=dictation_text,
                                 audio_path=file_path)
            
        except Exception as e:
            flash(f'処理中にエラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    flash('許可されていないファイル形式です', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
