import os
import time
import scratchattach as sa


# =========================================================
# 設定
# =========================================================
print(
    "scratchattach version:",
    getattr(sa, "__version__", "unknown")
)

print(
    "Scratch username:",
    session.get_linked_user().username
)

PROJECT_ID = "1368672819"
SESSION_ID = os.environ.get("SCRATCH_SESSION_ID")

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

    if not SESSION_ID:
        raise RuntimeError(
            "SCRATCH_SESSION_ID が設定されていません。"
        )

    # -----------------------------------------------------
    # ログイン
    # -----------------------------------------------------

    print()
    print("Scratchにログインしています...")

    session = sa.login_by_id(
        SESSION_ID
    )

    print("✅ Scratchログイン成功")

    # -----------------------------------------------------
    # Cloud接続
    # -----------------------------------------------------

    print()
    print("Scratch Cloudへ接続しています...")

    cloud = session.connect_scratch_cloud(
        PROJECT_ID
    )

    print("✅ Scratch Cloud接続成功")

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

    cloud.set_var(
        CLOUD_VARIABLE,
        TEST_VALUE
    )

    print()
    print(
        "✅ set_var() 完了"
    )

    # -----------------------------------------------------
    # Cloudログ取得
    # -----------------------------------------------------

    print()
    print(
        "Scratch Cloudのログを確認しています..."
    )

    time.sleep(3)

    try:

        logs = cloud.logs(
            filter_by_var_named=CLOUD_VARIABLE,
            limit=20
        )

        print()
        print(
            f"取得したログ数: {len(logs)}"
        )

        print()
        print(
            "================================"
        )
        print(
            "Cloudログ"
        )
        print(
            "================================"
        )

        for log in logs:

            print(
                f"時刻: {log.timestamp}"
            )

            print(
                f"ユーザー: {log.username}"
            )

            print(
                f"変数: {log.var}"
            )

            print(
                f"種類: {log.type}"
            )

            print(
                f"値: {log.value}"
            )

            print(
                "--------------------------------"
            )

    except Exception as e:

        print()
        print(
            "❌ Cloudログ取得エラー"
        )

        print(
            f"種類: {type(e).__name__}"
        )

        print(
            f"内容: {e}"
        )

    # -----------------------------------------------------
    # 切断
    # -----------------------------------------------------

    try:

        cloud.disconnect()

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
