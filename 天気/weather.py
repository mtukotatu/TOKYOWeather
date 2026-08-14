import os
import scratchattach as sa


# =========================================================
# 設定
# =========================================================

# GitHub Actions Secretsから取得
SESSION_ID = os.environ.get(
    "SCRATCH_SESSION_ID"
)

SCRATCH_USERNAME = os.environ.get(
    "SCRATCH_USERNAME"
)

PROJECT_ID = os.environ.get(
    "PROJECT_ID"
)

# Scratchクラウド変数
CLOUD_VARIABLE = "TokyoWeather"

# 今回のテスト値
TEST_VALUE = "3"


# =========================================================
# 設定確認
# =========================================================

def check_config():

    print()
    print("================================")
    print("設定を確認しています")
    print("================================")

    # -----------------------------------------------------
    # SCRATCH_SESSION_ID
    # -----------------------------------------------------

    if not SESSION_ID:

        raise RuntimeError(
            "SCRATCH_SESSION_ID が設定されていません。\n"
            "GitHub Actions Secretsを確認してください。"
        )

    print(
        "SCRATCH_SESSION_ID: 設定済み"
    )

    # -----------------------------------------------------
    # SCRATCH_USERNAME
    # -----------------------------------------------------

    if SCRATCH_USERNAME:

        print(
            f"SCRATCH_USERNAME: {SCRATCH_USERNAME}"
        )

    else:

        print(
            "⚠️ SCRATCH_USERNAME: 未設定"
        )

    # -----------------------------------------------------
    # PROJECT_ID
    # -----------------------------------------------------

    if not PROJECT_ID:

        raise RuntimeError(
            "PROJECT_ID が設定されていません。\n"
            "GitHub Actions Secretsを確認してください。"
        )

    print(
        f"PROJECT_ID: {PROJECT_ID}"
    )

    # -----------------------------------------------------
    # Cloud variable
    # -----------------------------------------------------

    print(
        f"クラウド変数: {CLOUD_VARIABLE}"
    )

    print(
        f"テスト値: {TEST_VALUE}"
    )


# =========================================================
# Scratchログイン
# =========================================================

def login_scratch():

    print()
    print("================================")
    print("Scratchにログインしています")
    print("================================")

    try:

        session = sa.login_by_id(
            SESSION_ID
        )

        print(
            "✅ Scratchログイン成功"
        )

    except Exception as e:

        print()
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

    return session


# =========================================================
# ログインユーザー確認
# =========================================================

def check_logged_in_user(session):

    print()
    print("================================")
    print("ログインユーザーを確認します")
    print("================================")

    try:

        user = session.get_linked_user()

        username = user.username

        print(
            f"Scratchユーザー: {username}"
        )

        # -------------------------------------------------
        # Secretsのユーザー名と比較
        # -------------------------------------------------

        if SCRATCH_USERNAME:

            if username == SCRATCH_USERNAME:

                print(
                    "✅ Scratchユーザー名が一致しました"
                )

            else:

                print()
                print(
                    "⚠️ Scratchユーザー名が一致しません"
                )

                print(
                    f"Secrets: {SCRATCH_USERNAME}"
                )

                print(
                    f"実際:    {username}"
                )

        return username

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

        return None


# =========================================================
# Scratch Cloud接続
# =========================================================

def connect_cloud(session):

    print()
    print("================================")
    print("Scratch Cloudへ接続しています")
    print("================================")

    print(
        f"プロジェクトID: {PROJECT_ID}"
    )

    try:

        cloud = session.connect_scratch_cloud(
            PROJECT_ID
        )

        print(
            "✅ Scratch Cloud接続成功"
        )

    except Exception as e:

        print()
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

    return cloud


# =========================================================
# クラウド変数へ書き込み
# =========================================================

def write_cloud_variable(cloud):

    print()
    print("================================")
    print("クラウド変数を書き込みます")
    print("================================")

    print(
        f"変数: {CLOUD_VARIABLE}"
    )

    print(
        f"送信値: {TEST_VALUE}"
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


# =========================================================
# Scratch Cloudログ確認
# =========================================================

def check_cloud_logs(cloud):

    print()
    print("================================")
    print("Scratch Cloudログを確認します")
    print("================================")

    try:

        logs = cloud.logs(
            filter_by_var_named=CLOUD_VARIABLE,
            limit=20
        )

        print(
            f"取得したログ数: {len(logs)}"
        )

        if not logs:

            print()
            print(
                "⚠️ Cloudログが0件です"
            )

            return

        print()

        for index, log in enumerate(
            logs,
            start=1
        ):

            print(
                f"--- Log {index} ---"
            )

            # -------------------------------------------------
            # scratchattachのバージョンによって
            # 属性が違う可能性があるため安全に取得
            # -------------------------------------------------

            print(
                f"時刻: "
                f"{getattr(log, 'timestamp', '不明')}"
            )

            print(
                f"ユーザー: "
                f"{getattr(log, 'username', '不明')}"
            )

            print(
                f"変数: "
                f"{getattr(log, 'var', '不明')}"
            )

            print(
                f"種類: "
                f"{getattr(log, 'type', '不明')}"
            )

            print(
                f"値: "
                f"{getattr(log, 'value', '不明')}"
            )

    except Exception as e:

        print()
        print(
            "⚠️ Cloudログ取得中にエラーが発生しました"
        )

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )


# =========================================================
# メイン
# =========================================================

def main():

    print()
    print("================================")
    print("TOKYOWeather Scratch Cloud診断")
    print("================================")

    # -----------------------------------------------------
    # 設定確認
    # -----------------------------------------------------

    check_config()

    # -----------------------------------------------------
    # Scratchログイン
    # -----------------------------------------------------

    session = login_scratch()

    # -----------------------------------------------------
    # ログインユーザー確認
    # -----------------------------------------------------

    check_logged_in_user(
        session
    )

    # -----------------------------------------------------
    # Scratch Cloud接続
    # -----------------------------------------------------

    cloud = connect_cloud(
        session
    )

    try:

        # -------------------------------------------------
        # 固定値3を書き込む
        # -------------------------------------------------

        write_cloud_variable(
            cloud
        )

        # -------------------------------------------------
        # Cloudログ確認
        # -------------------------------------------------

        check_cloud_logs(
            cloud
        )

    finally:

        # -------------------------------------------------
        # Cloud切断
        # -------------------------------------------------

        try:

            cloud.disconnect()

            print()
            print(
                "Scratch Cloudから切断しました"
            )

        except Exception:

            pass

    # -----------------------------------------------------
    # 最終案内
    # -----------------------------------------------------

    print()
    print("================================")
    print("診断終了")
    print("================================")

    print()
    print(
        f"Scratch側の ☁ {CLOUD_VARIABLE} を確認してください。"
    )

    print(
        f"期待値: {TEST_VALUE}"
    )

    print()


# =========================================================
# 実行
# =========================================================

if __name__ == "__main__":

    main()
