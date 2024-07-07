import streamlit as st
import fitz
from gtts import gTTS
from googletrans import Translator
from io import BytesIO

# 翻訳器の初期化
translator = Translator()

# サイドバーでの言語選択
option = st.sidebar.selectbox('出力言語を選択してください', ('日本語', '英語', '中国語'))

# サイドバーでのファイルアップローダー
uploaded_file = st.sidebar.file_uploader("テキストファイルまたはPDFファイルをアップロードしてください", type=["pdf", "txt"])

text_input_display = ""  # 読み取ったテキストを表示するための変数

# ファイルがアップロードされた場合の処理
if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/pdf":
            # PDFファイルの内容を読み込む
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                text_from_pdf = ""
                for page in doc:
                    text_from_pdf += page.get_text()
            text_input_display = text_from_pdf  # PDFから抽出したテキスト
        elif uploaded_file.type == "text/plain":
            # テキストファイルの場合
            text_input_display = uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")

# テキストエリアでテキストを表示し、ユーザーに編集を許可
edited_text = st.text_area("テキストを編集してください", text_input_display, height=300)

# 読み上げボタン
if st.button(f"{option}で読み上げ") and edited_text:
    try:
        # 翻訳の方向を設定
        if option == '英語':
            src_lang = 'ja'
            dest_lang = 'en'
        elif option == '中国語':
            src_lang = 'ja'
            dest_lang = 'zh-cn'
        else:
            src_lang = 'en'
            dest_lang = 'ja'

        # 翻訳が必要な場合、翻訳を実行
        if src_lang != dest_lang:
            translated = translator.translate(edited_text, src=src_lang, dest=dest_lang)
            text_to_speak = translated.text
        else:
            text_to_speak = edited_text

        # gTTSを使用してテキストを音声に変換
        tts = gTTS(text=text_to_speak, lang=dest_lang)
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        # 音声を再生
        st.audio(audio_data, format="audio/mp3")

        # 翻訳されたテキストを表示
        if src_lang != dest_lang:
            st.write(f"翻訳された{option}: {text_to_speak}")

    except Exception as e:
        st.error(f"読み上げ中にエラーが発生しました: {e}")