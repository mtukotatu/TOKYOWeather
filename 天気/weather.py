import os
import requests
import scratchattach as sa


# =========================================================
# 設定
# =========================================================

PROJECT_ID = "1368004496"

# GitHub Actions Secrets
SESSION_ID = os.environ.get("SCRATCH_SESSION_ID")

# Scratchクラウド変数
CLOUD_VARIABLE = "TokyoWeather"

# 気象庁・東京
JMA_URL = (
    "https://www.jma.go.jp/"
    "bosai/forecast/data/forecast/130000.json"
)


# =========================================================
# 東京の天気を取得
# =========================================================

def get_weather():

    print("気象庁からデータを取得しています...")

    response = requests.get(
        JMA_URL,
        timeout=30,
        headers={
            "User-Agent": "TOKYOWeather/1.0"
        }
    )

    response.raise_for_status()

    data = response.json()

    print("気象庁データを取得しました")

    for series_index, series in enumerate(
        data[0].get("timeSeries", [])
    ):

        print(f"timeSeries {series_index}")

        for area in series.get("areas", []):

            area_name = area.get(
                "area",
                {}
            ).get(
                "name",
                ""
            )

            print(f"  地域: {area_name}")

            if area_name != "東京地方":
                continue

            weather_list = area.get(
                "weathers",
                []
            )

            code_list = area.get(
                "weatherCodes",
                []
            )

            if not weather_list:
                continue

            weather = weather_list[0]

            if code_list:
                weather_code = int(
                    code_list[0]
                )
            else:
                weather_code = 2

            print(
                "東京地方を発見しました！"
            )

            print(
                f"天気: {weather}"
            )

            print(
                f"気象庁コード: {weather_code}"
            )

            return weather, weather_code

    print()
    print("取得した地域一覧:")

    for series in data[0].get(
        "timeSeries",
        []
    ):

        for area in series.get(
            "areas",
            []
        ):

            name = area.get(
                "area",
                {}
            ).get(
                "name",
                ""
            )

            print(f" - {name}")

    raise RuntimeError(
        "東京地方の天気データが見つかりませんでした。"
    )


# =========================================================
# Scratch用天気コードへ変換
# =========================================================

def convert_weather_code(
    weather,
    jma_code
):

    weather = weather.replace(
        " ",
        ""
    )

    # 晴れ
    if (
        "晴" in weather
        and "雨" not in weather
        and "雪" not in weather
    ):
        return 1

    # 雨
    if "雨" in weather:
        return 3

    # 雪
    if "雪" in weather:
        return 4

    # くもり・その他
    return 2


# =========================================================
# Scratchにログイン
# =========================================================

def connect_scratch():

    print()
    print("Scratchに接続しています...")

    if not SESSION_ID:

        raise RuntimeError(
            "SCRATCH_SESSION_ID が設定されていません。\n"
            "GitHub Actions の Secrets に "
            "SCRATCH_SESSION_ID を設定してください。"
        )

    print(
        "SCRATCH_SESSION_ID: 設定済み"
    )

    print(
        f"プロジェクトID: {PROJECT_ID}"
    )

    print(
        f"クラウド変数: {CLOUD_VARIABLE}"
    )

    # -----------------------------------------------------
    # 重要
    #
    # Session(SESSION_ID) ではなく
    # login_by_id() を使う
    # -----------------------------------------------------

    try:

        session = sa.login_by_id(
            SESSION_ID
        )

        print(
            "Scratchログイン成功"
        )

    except Exception as e:

        print()
        print(
            "================================"
        )

        print(
            "Scratchログインエラー"
        )

        print(
            "================================"
        )

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

        print(
            "================================"
        )

        raise

    # -----------------------------------------------------
    # セッションIDが実際に入っているか確認
    # -----------------------------------------------------

    if not session.id:

        raise RuntimeError(
            "Scratch Sessionは作成されましたが、"
            "session.id が空です。"
        )

    print(
        "ScratchセッションID確認OK"
    )

    return session


# =========================================================
# クラウド変数更新
# =========================================================

def update_cloud_variable(
    session,
    value
):

    print()
    print(
        f"クラウド変数 "
        f"{CLOUD_VARIABLE} を "
        f"{value} に変更します..."
    )

    # -----------------------------------------------------
    # Scratch Cloudに接続
    # -----------------------------------------------------

    try:

        print(
            "Scratchクラウドへ接続しています..."
        )

        cloud = session.connect_scratch_cloud(
            PROJECT_ID
        )

        print(
            "Scratchクラウドに接続しました！"
        )

    except Exception as e:

        print()
        print(
            "================================"
        )

        print(
            "Scratchクラウド接続エラー"
        )

        print(
            "================================"
        )

        print(
            f"プロジェクトID: {PROJECT_ID}"
        )

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

        print(
            "================================"
        )

        raise

    # -----------------------------------------------------
    # クラウド変数に書き込み
    # -----------------------------------------------------

    try:

        print(
            f"{CLOUD_VARIABLE} に "
            f"{value} を送信しています..."
        )

        cloud.set_var(
            CLOUD_VARIABLE,
            value
        )

        print()
        print(
            "クラウド変数を更新しました！"
        )

        print(
            f"変数: {CLOUD_VARIABLE}"
        )

        print(
            f"値: {value}"
        )

    except Exception as e:

        print()
        print(
            "================================"
        )

        print(
            "クラウド変数更新エラー"
        )

        print(
            "================================"
        )

        print(
            f"変数名: {CLOUD_VARIABLE}"
        )

        print(
            f"値: {value}"
        )

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

        print(
            "================================"
        )

        raise

    finally:

        try:
            cloud.disconnect()
        except Exception:
            pass


# =========================================================
# メイン
# =========================================================

def main():

    print()
    print("================================")
    print("TOKYOWeatherを開始します")
    print("================================")

    # -----------------------------------------------------
    # 天気取得
    # -----------------------------------------------------

    print()
    print(
        "東京の天気を取得しています..."
    )

    weather, jma_code = get_weather()

    print()
    print("東京の天気:")
    print(weather)

    print(
        f"気象庁コード: {jma_code}"
    )

    # -----------------------------------------------------
    # Scratch用コード
    # -----------------------------------------------------

    weather_code = convert_weather_code(
        weather,
        jma_code
    )

    print()
    print(
        f"Scratch用天気コード: "
        f"{weather_code}"
    )

    # -----------------------------------------------------
    # Scratchログイン
    # -----------------------------------------------------

    session = connect_scratch()

    # -----------------------------------------------------
    # クラウド変数更新
    # -----------------------------------------------------

    update_cloud_variable(
        session,
        weather_code
    )

    # -----------------------------------------------------
    # 完了
    # -----------------------------------------------------

    print()
    print("================================")
    print(
        "東京の天気をScratchへ送信しました！"
    )
    print(
        f"送信値: {weather_code}"
    )
    print("================================")


# =========================================================
# 実行
# =========================================================

if __name__ == "__main__":
    main()
