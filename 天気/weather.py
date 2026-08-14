import os
import scratchattach as sa


# =========================================================
# 設定
# =========================================================

PROJECT_ID = "1368004496"

SESSION_ID = os.environ.get(
    "SCRATCH_SESSION_ID"
)

CLOUD_VARIABLE = "TokyoWeather"

TEST_VALUE = "3"


# =========================================================
# メイン
# =========================================================

def main():

    print()
    print("================================")
    print("Scratch Cloud 書き込み診断")
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
    # ログインユーザー確認
    # -----------------------------------------------------

    try:

        user = session.get_linked_user()

        print()
        print(
            "Scratchユーザー:"
        )

        print(
            user.username
        )

    except Exception as e:

        print()
        print(
            "⚠️ Scratchユーザー名を取得できませんでした"
        )

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

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
    print("================================")
    print("クラウド変数を書き込みます")
    print("================================")

    print(
        f"変数: {CLOUD_VARIABLE}"
    )

    print(
        f"値: {TEST_VALUE}"
    )

    try:

        cloud.set_var(
            CLOUD_VARIABLE,
            TEST_VALUE
        )

        print()
        print(
            "✅ set_var() が正常に実行されました！"
        )

    except Exception as e:

        print()
        print(
            "❌ set_var() でエラーが発生しました"
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
        "Scratch側で確認してください。"
    )

    print()
    print(
        f"☁ {CLOUD_VARIABLE}"
    )

    print(
        f"期待値: {TEST_VALUE}"
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
    print("================================")
    print("診断終了")
    print("================================")


# =========================================================
# 実行
# =========================================================

if __name__ == "__main__":

    main()
