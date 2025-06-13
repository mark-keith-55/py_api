from flask import Flask, render_template, request, redirect, url_for
import os
import io
import datetime
from werkzeug.utils import secure_filename
from google.cloud import speech
from dotenv import load_dotenv

# 現在のディレクトリにある.envファイルを明示的に読み込む
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# .envファイルからサービスアカウントキーのパスを取得
# .envファイルには GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json" のように記述
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS が .env ファイルに設定されていません。サービスアカウントキーのJSONファイルパスを指定してください。")
if not os.path.exists(credentials_path):
    raise FileNotFoundError(f"指定されたサービスアカウントキーファイルが見つかりません: {credentials_path}")
# load_dotenv() によって環境変数 GOOGLE_APPLICATION_CREDENTIALS が設定されていれば、
# Google Cloud Client Libraries は自動的にそれを参照します。

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TRANSCRIPT_FOLDER'] = 'transcripts'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg', 'm4a'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def transcribe_audio(file_path):
    """Google Cloud Speech-to-Text APIを使用して音声ファイルをテキストに変換する"""
    client = speech.SpeechClient()
    
    # ファイルを読み込む
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()
    
    # ファイル形式から適切な設定を選択
    file_ext = file_path.split('.')[-1].lower()
    
    if file_ext == 'wav':
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="ja-JP",
        )
    else:  # mp3, ogg, m4a
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            language_code="ja-JP",
        )
    
    # 音声認識を実行
    response = client.recognize(config=config, audio=audio)
    
    # 認識結果を文字列に変換
    transcript_text = ""
    for result in response.results:
        transcript_text += result.alternatives[0].transcript + "\n"
    
    return transcript_text

def save_transcript(text, original_filename):
    """文字起こし結果をテキストファイルとして保存"""
    # ファイル名から拡張子を除去して、日時を追加
    base_name = os.path.splitext(original_filename)[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_filename = f"{base_name}_{timestamp}.txt"
    
    # 保存先パス
    transcript_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], transcript_filename)
    
    # テキストファイルに保存
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    return transcript_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['audio_file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 音声ファイルの文字起こし
        try:
            transcript_text = transcribe_audio(file_path)
            transcript_filename = save_transcript(transcript_text, filename)
            
            return render_template('success.html', 
                                  filename=filename, 
                                  transcript_filename=transcript_filename,
                                  transcript_text=transcript_text)
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
