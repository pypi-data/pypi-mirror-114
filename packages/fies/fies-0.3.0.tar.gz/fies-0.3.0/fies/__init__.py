
# ファイル入出力ツール [fies]

import os
import sys
import json
import pickle

# read_modeを表すオブジェクト
class _ReadMode:
	# 初期化処理
	def __init__(self):
		pass

# ファイルフォーマット略記辞書
abb_ff_dic = {
	"text": ["t", "txt"],
	"json": ["j", "js"],
	"pickle": ["p", "pkl", "pick"]
}

# ファイルフォーマット指定の解決 (略記, auto)
def cleanup_file_format(file_format, filename, data):
	# 自動指定の場合
	if file_format == "auto":
		_, ext = os.path.splitext(filename)
		if ext == ".json": return "json"
		if ext == ".pickle": return "pickle"
		return "text"
	# 略記の解決
	for formal in abb_ff_dic:
		if file_format.lower() == formal.lower(): return formal
		for abb in abb_ff_dic[formal]:
			if file_format.lower() == abb.lower(): return formal
	# 解決できない場合
	raise Exception("[fies error] invalid file_format.")

# テキストファイルの読み込み
def text_read(filename, **kw_args):
	with open(filename, "r", encoding = "utf-8") as f:
		data = f.read()
	return data

# テキストファイルの書き出し
def text_write(filename, data, **kw_args):
	with open(filename, "w", encoding = "utf-8") as f:
		f.write(data)

# jsonファイルの読み込み
def json_read(filename, **kw_args):
	json_str = text_read(filename, **kw_args)	# テキストファイルの読み込み
	return json.loads(json_str)

# jsonファイルの書き出し
def json_write(filename, data, **kw_args):
	json_str = json.dumps(data, indent = 4, ensure_ascii = False)
	text_write(filename, json_str, **kw_args)	# テキストファイルの書き出し

# pickleファイルの読み込み
def pickle_read(filename, **kw_args):
	with open(filename, "rb") as f:
		data = pickle.load(f)
	return data

# pickleファイルの書き出し
def pickle_write(filename, data, **kw_args):
	with open(filename, "wb") as f:
		pickle.dump(data, f)

# ファイル入出力ツール [fies]
class Fies:
	# 初期化処理
	def __init__(self):
		pass
	# ファイル読み書き
	def __call__(self, filename, data = _ReadMode(), file_format = "auto", **kw_args):
		# ファイルフォーマット指定の解決 (略記, auto)
		file_format = cleanup_file_format(file_format, filename, data)
		# 読み/書き で分岐
		if type(data) == _ReadMode:
			return self._read(filename, file_format, **kw_args)
		else:
			self._write(filename, data, file_format, **kw_args)
	# ファイルの読み込み (略記)
	def __getitem__(self, query):
		# auto指定が省略されている場合
		if type(query) == type(""): query = (query, "auto")
		filename, file_format = query
		return self(filename, file_format = file_format)
	# ファイルの保存 (略記)
	def __setitem__(self, query, data):
		# auto指定が省略されている場合
		if type(query) == type(""): query = (query, "auto")
		filename, file_format = query
		return self(filename, data, file_format = file_format)
	# 読み込み
	def _read(self, filename, file_format, **kw_args):
		if file_format == "json":
			return json_read(filename, **kw_args)	# jsonファイルの読み込み
		elif file_format == "text":
			return text_read(filename, **kw_args)	# テキストファイルの読み込み
		elif file_format == "pickle":
			return pickle_read(filename, **kw_args)	# pickleファイルの読み込み
		else:
			raise Exception("[fies error] invalid file_format.")
	# 書き出し
	def _write(self, filename, data, file_format, **kw_args):
		if file_format == "json":
			json_write(filename, data, **kw_args)	# jsonファイルの書き出し
		elif file_format == "text":
			text_write(filename, data, **kw_args)	# テキストファイルの書き出し
		elif file_format == "pickle":
			pickle_write(filename, data, **kw_args)	# pickleファイルの書き出し
		else:
			raise Exception("[fies error] invalid file_format.")

# 呼び出しの準備
fies = Fies()	# Fies型のオブジェクトを予め実体化
sys.modules[__name__] = fies	# モジュールオブジェクトとfiesオブジェクトを同一視
