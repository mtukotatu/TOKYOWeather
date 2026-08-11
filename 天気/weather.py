import os
import time
import requests
import scratchattach as sa


# =========================================================
# 設定
# =========================================================

PROJECT_ID = "1368004496"

# GitHub Actions の Secrets から取得
SESSION_ID = os.environ.get("SCRATCH_SESSION_ID")

# Scratchのクラウド変数名
CLOUD_VARIABLE = "TokyoWeather"

# 気象庁・東京地方
JMA_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"


# =========================================================
# 東京の天気を取得
# =========================================================

def get_weather():
    response = requests.get(
        JMA_URL,
        timeout=30,
        headers={
            "User-Agent": "TOKYOWeather/1.0"
        }
    )

    response.raise_for_status()

    data = response.json()

    # 気象庁JSONから東京地方を探す
    for series in data[0].get("timeSeries", []):
        for area in series.get("areas", []):

            area_name = area.get("area", {}).get("name", "")

            if area_name == "東京地方":

                weather_list = area.get("weathers", [])
                code_list = area.get("weatherCodes", [])

                if not weather_list:
                    continue

                weather = weather_list[0]

                if code_list:
                    weather_code = int(code_list[0])
                else:
                    weather_code = 2

                return weather, weather_code

    raise RuntimeError(
        "東京の天気データが見つかりませんでした。"
    )


# =========================================================
# 天気コードをScratch用の数字に変換
# =========================================================

def convert_weather_code(weather, jma_code):

    weather = weather.replace(" ", "")

    # 晴れ
    if "晴" in weather and "雨" not in weather and "雪" not in weather:
        return 1

    # 雨
    if "雨" in weather:
        return 3

    # 雪
    if "雪" in weather:
        return 4

    # それ以外（くもりなど）
    return 2


# =========================================================
# Scratchに接続
# =========================================================

def connect_scratch():

    if not SESSION_ID:
        raise RuntimeError(
            "SCRATCH_SESSION_ID が設定されていません。\n"
            "GitHub Actions の Secrets に "
            "SCRATCH_SESSION_ID を設定してください。"
        )

    print("Scratchに接続しています...")

    session = sa.Session(
        SESSION_ID,
        username=None
    )

    project = session.connect_project(PROJECT_ID)

    print("Scratchに接続しました！")

    return project


# =========================================================
# クラウド変数を書き換え
# =========================================================

def update_cloud_variable(project, value):

    print(
        f"クラウド変数 {CLOUD_VARIABLE} を "
        f"{value} に変更します..."
    )

    cloud = project.cloud

    cloud.set_var(
        CLOUD_VARIABLE,
        value
    )

    print("クラウド変数を更新しました！")


# =========================================================
# メイン
# =========================================================

def main():

    print("TOKYOWeatherを開始します")

    # -----------------------------------------------------
    # 天気取得
    # -----------------------------------------------------

    print("東京の天気を取得しています...")

    weather, jma_code = get_weather()

    print()
    print("東京の天気:")
    print(weather)
    print(f"気象庁コード: {jma_code}")

    # -----------------------------------------------------
    # Scratch用コードへ変換
    # -----------------------------------------------------

    weather_code = convert_weather_code(
        weather,
        jma_code
    )

    print()
    print(f"Scratch用天気コード: {weather_code}")

    # -----------------------------------------------------
    # Scratch接続
    # -----------------------------------------------------

    project = connect_scratch()

    # -----------------------------------------------------
    # クラウド変数更新
    # -----------------------------------------------------

    update_cloud_variable(
        project,
        weather_code
    )

    print()
    print("================================")
    print("東京の天気をScratchへ送信しました！")
    print("================================")


# =========================================================
# 実行
# =========================================================

if __name__ == "__main__":
    main()
