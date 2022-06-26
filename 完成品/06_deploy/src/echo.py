import json
import os


def init():
    # ここでモデルを読み込む
    print("This is init")


def run(data):
    # リクエストbodyを返却
    body = json.loads(data)
    return f"{body}"