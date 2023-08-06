class Request():
    """ステートマシンからステートへ与えられる引数のまとまり"""

    def __init__(self, context, intermachine, state_path=[]):
        self._context = context
        self._state_path = state_path
        self._intermachine = intermachine

    @property
    def context(self):
        """このステートマシンは、このContextが何なのか知りません。
        外部から任意に与えることができる変数です。 Defaults to None."""
        return self._context

    @property
    def state_path(self):
        """状態パス
        Examples
        --------
        list
            ["this","is","a","edge","path"]
        """
        return self._state_path

    @property
    def intermachine(self):
        """ステートマシン間の通信手段"""
        return self._intermachine
