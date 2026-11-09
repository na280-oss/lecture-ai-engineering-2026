# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
  - 第1回は一般的にありそうな回答であったが、今回は用語集の内容に沿った回答が返ってきた
- `--trace` で見えたツール呼び出し（ツール名と引数）：
  - search_glossary({'query': 'LoRA'})
  - search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：2
- 追加したツールと、docstring に書いた説明：
  - make_quiz

    ```python
    """指定した回の用語から1つを選び、
    確認問題と答えを返す。
    「第2回の確認問題を出して」のように、
    復習用の問題を求められたときに使う。
    """
    ```

## 宿題

- 取り組んだレベル：実装
- やったこと：
  - save_learning_logツールを作成し、docstringには以下を記載

    ```text
    学習の記録を learning_log/ フォルダに Markdown ファイルとして保存する。

    「今日学んだことを記録して」のように、利用者が記録を残すよう頼んだときだけ使う。
    title には記録の短い見出し、content には保存する本文（Markdown）を入れる。
    保存の前に利用者の確認がある。
    引数: {"title": {"type": "string"}, "content": {"type": "string"}}
    ```

  - `uv run python -m app.agent --trace "「LoRAについて調べ、要点を学習の記録として保存して"`というコマンドを実行
- 結果：
  - コマンドと出力
    ```console
    $ uv run python -m app.agent --trace "LoRAについて調べて、要点を学習の記録として保存して"
    [model] gemini-3.5-flash-lite

    [承認待ち] save_learning_log
      title: LoRAについての学習記録
      content: # LoRAの学習記録

    ## 概要
    事前学習済みの重みを固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。

    ## 主な特徴
    - 学習するパラメータ数が大幅に少ないため、効率的なファインチューニングが可能。
    - 学習結果（アダプタ）を小さなファイルサイズで保存できる。
    - QLoRAなどの発展手法と組み合わせることで、さらに省メモリでの学習が可能になる。

    （関連回：第2回）
    実行してよいですか？ [y/N]: y
    LoRAについての学習記録を作成し、`learning_log/` フォルダに保存しました。

    ### LoRAの要点
    * **定義**: 事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法です。
    * **特徴**: 学習するパラメータ数が少なく、学習結果（アダプタ）も小さなファイルで保存できます。

    （関連回：第2回）

    --- trace ---
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
    [tool call]   save_learning_log({'title': 'LoRAについての学習記録', 'content': '# LoRAの学習記録\n\n## 概要\n事前学習済みの重みを固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。\n\n## 主な特徴\n- 学習するパラメータ数が大幅に少ないため、効率的なファインチューニングが可能。\n- 学習結果（アダプタ）を小さなファイルサイズで保存できる。\n- QLoRAなどの発展手法と組み合わせることで、さらに省メモリでの学習が可能になる。\n\n（関連回：第2回）'})
    [tool return] save_learning_log -> learning_log/20261109-055051.md に保存しました。…
    [usage] RunUsage(cost=Decimal('0.0005909'), details={'text_prompt_tokens': 1053}, input_text_tokens=1053, input_tokens=1053, output_tokens=110, requests=1, tool_calls=1)

    ```

- 気づき・疑問：
  - 試しにsave_learning_logツールのdocstringに記載した"利用者が記録を残すよう頼んだときだけ使う。"という文言を消して実行したところ無条件で保存しようとした。docstringの内容をモデルが理解していることが理解できた