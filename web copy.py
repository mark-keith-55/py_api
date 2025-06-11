from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # flashメッセージのために必要


@app.route('/')
def index():
    return render_template('voice_index.html')

@app.route('/voice_result', methods=['POST'])
def voice_result():
    voice_input = request.form['voice']
    
    # ログ出力
    print(f"voice_input: {voice_input}")

    return render_template('voice_result.html', voice_input=voice_input)

if __name__ == '__main__':
    # サーバー起動、debug=Trueはホットリローディングと≒
    app.run(debug=True)
