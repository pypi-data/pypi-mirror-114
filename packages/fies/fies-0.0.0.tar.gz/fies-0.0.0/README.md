# fies

下の方に日本語の説明があります

## Overview
This is a tool to read and write json files easily.
It will be extended to other formats. (csv, pickle, plain text, binary, etc.)

## Usage
```python
import fies

# Save json
fies["./test.json"] = {"hoge": 23, "dummy_data": "fuga"}

# Read json
print(fies["./test.json"]) # -> {'hoge': 23, 'dummy_data': 'fuga'}
````

## 概要
jsonファイルを簡単に読み書きできるツールです。
他の形式にも拡張予定です。(csv, pickle, プレーンテキスト, バイナリ など)

## 使い方
```python
import fies

# json保存
fies["./test.json"] = {"hoge": 23, "dummy_data": "fuga"}

# json読み込み
print(fies["./test.json"])	# -> {'hoge': 23, 'dummy_data': 'fuga'}
```
