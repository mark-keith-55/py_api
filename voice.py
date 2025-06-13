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
    'database': 'voicies',
    'raise_on_warnings': True,
    'auth_plugin': 'mysql_native_password'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_to_database(audio_path, dictation_text):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 現在のタイムスタンプ
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # データの挿入
        query = """
        INSERT INTO consultations 
        (dictation_text, summary_text, audio_file_path, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # パスを相対パスに変換
        relative_audio_path = os.path.relpath(audio_path, start=os.path.dirname(__file__))
        
        # 初期段階では summary_text は NULL
        cursor.execute(query, (
            dictation_text,      # dictation_text
            None,               # summary_text (初期値はNULL)
            relative_audio_path, # audio_file_path
            current_time,       # created_at
            current_time        # updated_at
        ))
        
        # 挿入されたIDを取得
        consultation_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"データが正常に保存されました。ID: {consultation_id}")
        return True
        
    except Exception as e:
        print(f"データベースエラー: {e}")
        import traceback
        traceback.print_exc()  # 詳細なエラー情報を出力
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
        try:
            # ファイル名を生成（日付_時間_ランダム文字列.拡張子）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            original_extension = file.filename.rsplit('.', 1)[1].lower()
            random_string = os.urandom(4).hex()  # 8文字のランダム文字列
            filename = f"{timestamp}_{random_string}.{original_extension}"
            
            # アップロードフォルダが存在しない場合は作成
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            # ファイルの保存
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 仮の文字起こしテキスト（後でGemini AIで実装）
            dictation_text = "これは仮の文字起こしテキストです。"
            
            # データベースに保存
            if save_to_database(file_path, dictation_text):
                flash('音声ファイルの処理が完了しました', 'success')
            else:
                flash('データベースへの保存に失敗しました', 'error')
                return redirect(url_for('index'))
            
            return render_template('voice_result.html', 
                                voice_input=dictation_text,
                                audio_path=file_path)
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            flash(f'処理中にエラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    flash('許可されていないファイル形式です', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'production':
        # 本番環境用
        from waitress import serve
        print("本番環境でサーバーを起動します...")
        serve(app, host='0.0.0.0', port=8080)
    else:
        # 開発環境用
        print("開発環境でサーバーを起動します...")
        app.run(debug=True)
