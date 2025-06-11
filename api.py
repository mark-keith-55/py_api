from google import genai
import os 
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# スクリプトのディレクトリを基準に音声ファイルの絶対パスを構築
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file_name = 'audio/sample_1.mp3' # 'api.py' と同じ階層の 'audio' フォルダを指定
audio_file_path = os.path.join(script_dir, audio_file_name)

# ファイルの存在と種類を確認
if not os.path.exists(audio_file_path):
    print(f"エラー: 指定されたパスにファイルが見つかりません: {audio_file_path}")
    exit(1)
if not os.path.isfile(audio_file_path):
    print(f"エラー: 指定されたパスはファイルではありません: {audio_file_path}")
    exit(1)

myfile = client.files.upload(file=audio_file_path)
prompt = 'Generate a transcript of the speech in japanese.'

response = client.models.generate_content(
  model='gemini-1.5-flash', # モデル名をgemini-1.5-flashに更新 (または適切なモデル名)
  contents=[prompt, myfile]
)

print(response.text)