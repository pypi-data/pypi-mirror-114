# fies

下の方に日本語の説明があります

## Overview
- A tool to easily read and write json files and plain text files.
- It will be extended to other formats. (csv, pickle, binary, etc.)

## Usage
```python
import fies

# Save json file
fies["./test.json"] = {"hoge": 23, "dummy_data": "fuga"}

# Read json file
print(fies["./test.json"])	# -> {'hoge': 23, 'dummy_data': 'fuga'}

# Save plain text file
fies["./test.txt"] = "hogehoge"

# Read plain text file
print(fies["./test.txt"])	# -> hogehoge
````

## Advanced usage
```python
# format-specified save
fies["./test.myext", "json"] = {"hoge": 23, "dummy_data": "fuga"}
````

## 概要
- jsonファイル, プレーンテキストのファイルを簡単に読み書きできるツールです。
- 他の形式にも拡張予定です。(csv, pickle, バイナリ など)

## 使い方
```python
import fies

# jsonファイル保存
fies["./test.json"] = {"hoge": 23, "dummy_data": "fuga"}

# jsonファイル読み込み
print(fies["./test.json"])	# -> {'hoge': 23, 'dummy_data': 'fuga'}

# プレーンテキストファイル書き出し
fies["./test.txt"] = "hogehoge"

# プレーンテキストファイル読み込み
print(fies["./test.txt"])	# -> hogehoge
```

## 発展的な使い方
```python
# フォーマット指定書き出し
fies["./test.myext", "json"] = {"hoge": 23, "dummy_data": "fuga"}
```
