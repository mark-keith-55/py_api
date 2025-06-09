from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # flashメッセージのために必要


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def hello():
    greeting_input = request.form['greeting']
    name = request.form['name']
    lang = request.form.get('lang', 'en') # デフォルトは 'en'

    # 入力チェック( バリデーション )
    if not greeting_input or not name:
        flash('挨拶と名前の両方を入力してください。', 'error')
        return redirect(url_for('index'))

    # 英語の返答リスト (0:Good morning, 1:Good evening, 2:Hello, 3:bye)
    reply_en = ['Good morning', 'Good evening', 'Hello', 'bye']
    # 日本語の返答リスト (reply_enのインデックスと対応)
    reply_ja = ['おはようございます', 'こんばんは', 'こんにちは', 'さようなら']

    output_greeting = ""

    # 挨拶の判定とメッセージの選択
    if lang == 'en':
        if greeting_input.lower() in ('おはよう', 'オハヨウ', 'おはようございます', 'おはよ'):
            output_greeting = reply_en[0]  # Good morning
        elif greeting_input.lower() in ('こんばんは', 'コンバンハ'):
            output_greeting = reply_en[1]  # Good evening
        elif greeting_input.lower() in ('こんにちは', 'コンニチハ'):
            output_greeting = reply_en[2]  # Hello
        elif greeting_input.lower() in ('さようなら', 'サヨウナラ', 'バイバイ'):
            output_greeting = reply_en[3]  # bye
        else:
            output_greeting = reply_en[2]  # デフォルトは Hello
    elif lang == 'ja':
        if greeting_input.lower() in ('おはよう', 'オハヨウ', 'おはようございます', 'おはよ'):
            output_greeting = reply_ja[0]  # おはようございます
        elif greeting_input.lower() in ('こんばんは', 'コンバンハ'):
            output_greeting = reply_ja[1]  # こんばんは
        elif greeting_input.lower() in ('こんにちは', 'コンニチハ'):
            output_greeting = reply_ja[2]  # こんにちは
        elif greeting_input.lower() in ('さようなら', 'サヨウナラ', 'バイバイ'):
            output_greeting = reply_ja[3]  # さようなら
        else:
            output_greeting = reply_ja[2]  # デフォルトは こんにちは

    # ログ出力
    print(f"Input: {greeting_input}, Name: {name}, Lang: {lang}, Output: {output_greeting}")

    return render_template('reply.html', greeting=output_greeting, name=name, lang=lang)

if __name__ == '__main__':
    # サーバー起動、debug=Trueはホットリローディングと≒
    app.run(debug=True)
