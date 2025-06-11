import speech_recognition as sr
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 環境変数にGoogle Cloud Speech-to-Text APIのサービスアカウントキーのパスを設定
# ダウンロードしたJSONファイルのパスに置き換えてください
# 例: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"
# プログラムと同じディレクトリにある場合はファイル名だけでもOK
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_service_account_key_file.json"

OUTPUT_TXT_FILE = "./" + datetime.now().strftime('%Y%m%d_%H_%M') +".txt"

def recognize_voice_and_store(silence_duration_sec=3): # api_key引数は不要になります
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("エラー: Google Cloud Speech-to-Text APIのサービスアカウントキーが設定されていません。")
        print("os.environ[\"GOOGLE_APPLICATION_CREDENTIALS\"] にJSONファイルのパスを設定してください。")
        return ""

    r = sr.Recognizer()
    r.pause_threshold = silence_duration_sec

    with sr.Microphone() as source:
        print(f"周囲のノイズレベルを調整します。約1秒間、静かにしてください...")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"ノイズ調整中にエラーが発生しました: {e}")

        print(f"\n音声を入力してください。{silence_duration_sec}秒間無音になると自動的に録音を終了します。")

        audio_data = None
        try:
            audio_data = r.listen(source)
            print("録音終了。音声を処理しています...")
        except sr.WaitTimeoutError:
            print("タイムアウト: 音声が開始されませんでした。")
            return ""
        except Exception as e:
            print(f"録音中にエラーが発生しました: {e}")
            return ""

        if audio_data:
            try:
                # recognize_google_cloud を使用
                # GOOGLE_APPLICATION_CREDENTIALS が設定されていれば、credentials_json 引数は不要です
                # 変更前
                # recognized_text = r.recognize_google_cloud(audio_data, language='ja-JP')

                # 変更後
                recognized_text = r.recognize_google_cloud(audio_data, language_code='ja-JP')
                print("文字起こしが完了しました。")
                return recognized_text
            except sr.UnknownValueError:
                print("Google Cloud Speech-to-Text は音声を理解できませんでした。")
            except sr.RequestError as e:
                print(f"Google Cloud Speech-to-Text サービスからの結果を要求できませんでした; {e}")
            except Exception as e:
                print(f"文字起こし中に予期せぬエラーが発生しました: {e}")
        else:
            print("録音された音声データがありません。")

    return ""

if __name__ == '__main__':
    print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    input('音声を入力する準備ができたら、Enterキーを押してください: ')
    print("音声認識を開始します...")
    # api_key 引数はもう不要
    input_voice = recognize_voice_and_store(silence_duration_sec=3)

    if input_voice:
        print("\n--- 認識されたテキストデータ ---")
        print(input_voice)
        print("-----------------------------")
    else:
        print("音声からテキストを抽出できませんでした。")