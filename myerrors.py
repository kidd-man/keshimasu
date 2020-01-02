#
# 例外定義
#


class TimeUpException(Exception):
    """時間切れしたことを知らせる例外クラス"""
    pass


class InputError(Exception):
    """入力に関するエラーの例外クラス"""
    pass


def signal_handler(signum, frame):
    """時間制限で用いる signalの受信時に実行するハンドラ"""
    raise TimeUpException("時間切れです.")
