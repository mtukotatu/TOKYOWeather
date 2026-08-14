import os
import scratchattach as sa


# =========================================================
# 設定
# =========================================================

PROJECT_ID = "1368004496"

# GitHub Actions Secrets
SESSION_ID = os.environ.get("SCRATCH_SESSION_ID")

# Scratchクラウド変数
CLOUD_VARIABLE = "TokyoWeather"

# テストで送る値
TEST_VALUE = "3"


# =========================================================
# Scratchクラウド変数へ固定値を送信
# =========================================================

def main():

    print()
    print("================================")
    print("Scratch Cloud 書き込みテスト")
    print("================================")

    # -----------------------------------------------------
    # Session ID確認
    # -----------------------------------------------------

    if not SESSION_ID:

        raise RuntimeError(
            "SCRATCH_SESSION_ID が設定されていません。"
        )

    print()
    print(
        "SCRATCH_SESSION_ID: 設定済み"
    )

    print(
        f"プロジェクトID: {PROJECT_ID}"
    )

    print(
        f"クラウド変数: {CLOUD_VARIABLE}"
    )

    print(
        f"送信値: {TEST_VALUE}"
    )

    # -----------------------------------------------------
    # Scratchログイン
    # -----------------------------------------------------

    print()
    print(
        "Scratchにログインしています..."
    )

    try:

        session = sa.login_by_id(
            SESSION_ID
        )

        print(
            "✅ Scratchログイン成功"
        )

    except Exception as e:

        print(
            "❌ Scratchログイン失敗"
        )

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

        raise

    # -----------------------------------------------------
    # Scratch Cloudへ接続
    # -----------------------------------------------------

    print()
    print(
        "Scratch Cloudへ接続しています..."
    )

    try:

        cloud = session.connect_scratch_cloud(
            PROJECT_ID
        )

        print(
            "✅ Scratch Cloud接続成功"
        )

    except Exception as e:

        print(
            "❌ Scratch Cloud接続失敗"
        )

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

        raise

    # -----------------------------------------------------
    # 書き込み
    # -----------------------------------------------------

    print()
    print(
        "クラウド変数を書き換えます..."
    )

    print(
        f"{CLOUD_VARIABLE} ← {TEST_VALUE}"
    )

    try:

        cloud.set_var(
            CLOUD_VARIABLE,
            TEST_VALUE
        )

        print()
        print(
            "================================"
        )

        print(
            "✅ set_var() が正常に実行されました！"
        )

        print(
            "================================"
        )

    except Exception as e:

        print()
        print(
            "================================"
        )

        print(
            "❌ set_var() でエラーが発生しました"
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

        raise

    # -----------------------------------------------------
    # 終了
    #
    # get_var() は使わない
    # -----------------------------------------------------

    print()
    print(
        "Scratch側でクラウド変数を確認してください。"
    )

    print()
    print(
        f"☁ {CLOUD_VARIABLE} が"
    )

    print(
        f"「{TEST_VALUE}」になっているか確認してください。"
    )

    # -----------------------------------------------------
    # 切断
    # -----------------------------------------------------

    try:

        cloud.disconnect()

        print()
        print(
            "Scratch Cloudから切断しました。"
        )

    except Exception:

        pass

    print()
    print(
        "================================"
    )

    print(
        "テスト終了"
    )

    print(
        "================================"
    )


# =========================================================
# 実行
# =========================================================

if __name__ == "__main__":

    main()
