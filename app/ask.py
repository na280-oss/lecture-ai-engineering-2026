"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --chat     # 会話履歴を保ったまま、続けて質問する（exit で終了）

既定の呼び出しはツールも会話履歴も持たない「素の」呼び出し。
--chat では履歴を毎回送るため、表示される input トークン数は履歴の分も含みます。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def print_usage(usage) -> None:
    input_tokens = usage.prompt_token_count if usage else "不明"
    output_tokens = usage.candidates_token_count if usage else "不明"
    print(f"[usage] input={input_tokens}, output={output_tokens}")


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)

    print_usage(response.usage_metadata)

    return response.text


def chat_loop() -> None:
    """会話履歴を保ったまま質問を続ける。履歴は chat オブジェクトが持つ。"""
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)
    print("会話モードです。終了するには exit または Ctrl+D を入力します。")
    while True:
        try:
            question = input("\n質問> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if question == "exit":
            return
        if not question:
            continue
        try:
            # 成功した応答だけが履歴に入る。エラーになったターンは次の質問に含まれない
            response = chat.send_message(question)
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            continue
        print_usage(response.usage_metadata)
        print(response.text)


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--chat", action="store_true", help="会話履歴を保ったまま、続けて質問する")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    if args.chat:
        if args.question:
            parser.error("--chat のときは質問を引数で渡さず、対話モードで入力してください")
        chat_loop()
        return

    question = args.question or DEFAULT_QUESTION
    print(f"[質問] {question}\n")
    try:
        print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
