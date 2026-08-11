import requests
import time
import scratchattach as sa

import os

USERNAME = os.environ["USERNAME"]
SESSION_ID = os.environ["SESSION_ID"]
PROJECT_ID = os.environ["PROJECT_ID"]


# =========================
# 設定
# =========================

JMA_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

# 10分ごとに更新
UPDATE_INTERVAL = 60


# =========================
# 天気コード → Scratchの数字
# =========================

def weather_to_number(code):

    code = int(code)

    # 晴れ
    if 100 <= code < 200:
        return 1

    # くもり
    elif 200 <= code < 300:
        return 2

    # 雨
    elif 300 <= code < 400:
        return 3

    # 雪
    elif 400 <= code < 500:
        return 4

    return 0


# =========================
# 気象庁から東京の天気取得
# =========================

def get_weather():

    response = requests.get(
        JMA_URL,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    # 東京地方
    area = data[0]["timeSeries"][0]["areas"][0]

    weather = area["weathers"][0]
    code = area["weatherCodes"][0]

    number = weather_to_number(code)

    return weather, code, number


# =========================
# Scratchへ接続
# =========================

print("Scratchに接続中...")

session = sa.Session(
    username=USERNAME,
    id=SESSION_ID
)

cloud = session.connect_cloud(PROJECT_ID)

print("Scratch接続成功！")


# =========================
# 自動更新
# =========================

while True:

    try:

        weather, code, number = get_weather()

        print()
        print("==============================")
        print("東京の天気")
        print("==============================")
        print("天気:", weather)
        print("気象庁コード:", code)
        print("Scratchへ送る値:", number)

        # Scratchへ送信
        cloud.set_var(
            "天気",
            number
        )

        print("☁ 天気 に送信完了！")
        print("次の更新まで1分...")

        time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:

        print()
        print("終了しました。")
        break

    except Exception as e:

        print()
        print("エラー:", e)
        print("30秒後に再試行します...")

        time.sleep(30)
