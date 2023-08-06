
# ファイル入出力ツール [fies]
# 【動作確認 / 使用例】

import sys
from sout import sout
from ezpip import load_develop
fies = load_develop("fies", "../", develop_flag = True)

# json書き出し
fies["./test.json"] = {"hoge": 23, "dummy_data": "fuga"}

# json読み込み
sout(fies["./test.json"])

# プレーンテキスト書き出し
fies["./test.txt"] = "hogehoge"

# プレーンテキスト読み込み
print(fies["./test.txt"])

# pickleファイル書き出し
fies["./test.pickle"] = [("hoge", 23), 5.7]

# pickleファイル読み込み
print(fies["./test.pickle"])

# フォーマット指定書き出し
fies["./test.myext", "json"] = {"hoge": 23, "dummy_data": "fuga"}
