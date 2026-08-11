import os
import requests
import scratchattach as scratch3


# =========================
# GitHub Actions Secrets
# =========================

USERNAME = os.environ["SCRATCH_USERNAME"]
SESSION_ID = os.environ["SCRATCH_SESSION_ID"]
PROJECT_ID = os.environ["PROJECT_ID"]


# =========================
# 気象庁
# 東京地方の天気予報
# =========================

JMA_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"


# =========================
# 天気を取得
# =========================

def get_weather():
    response = requests.get(JMA_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    # 最初の予報データ
    time_series = data[0]["timeSeries"][0]

    # 東京の天気を探す
    areas = time_series["areas"]

    tokyo = None

    for area in areas:
        if area.get("area", {}).get("name") == "東京":
            tokyo = area
            break

    if tokyo is None:
        raise RuntimeError("東京の天気データが見つかりませんでした。")

    weather = tokyo["weathers"][0]
    weather_code = tokyo["weatherCodes"][0]

    return weather, weather_code


# =========================
# 天気コードをScratch用の数字に変換
#
# 1 = 晴れ
# 2 = くもり
# 3 = 雨
# 4 = 雪
# =========================

def convert_weather_code(weather_code):
    code = int(weather_code)

    # 100番台 = 晴れ
    if 100 <= code < 200:
        return 1

    # 200番台 = くもり
    elif 200 <= code < 300:
        return 2

    # 300番台 = 雨
    elif 300 <= code < 400:
        return 3

    # 400番台 = 雪
    elif 400 <= code < 500:
        return 4

    # 不明
    else:
        return 2


# =========================
# Scratchクラウド変数に送信
# =========================

def send_to_scratch(value):
    print("Scratchに接続しています...")

    # セッションIDでログイン
    session = scratch3.login_by_id(
        SESSION_ID,
        username=USERNAME
    )

    print("Scratchログイン成功")

    # クラウド変数に接続
    cloud = session.connect_scratch_cloud(PROJECT_ID)

    print("Scratchクラウドに接続成功")

    # TokyoWeatherを更新
    cloud.set_var("TokyoWeather", value)

    print(f"TokyoWeather = {value}")


# =========================
# メイン処理
# =========================

def main():
    print("TOKYOWeatherを開始します")

    weather, weather_code = get_weather()

    print(f"東京: {weather}")
    print(f"気象庁コード: {weather_code}")

    value = convert_weather_code(weather_code)

    print(f"Scratch用コード: {value}")

    send_to_scratch(value)

    print("TOKYOWeather完了")


if __name__ == "__main__":
    main()
