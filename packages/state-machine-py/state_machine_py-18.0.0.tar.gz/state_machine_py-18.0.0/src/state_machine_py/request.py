class Request():
    """ステートマシンからステートへ与えられる引数のまとまり"""

    def __init__(self, context, intermachine, edge_path=[]):
        self._context = context
        self._edge_path = edge_path
        self._intermachine = intermachine

    @property
    def context(self):
        """このステートマシンは、このContextが何なのか知りません。
        外部から任意に与えることができる変数です。 Defaults to None."""
        return self._context

    @property
    def edge_path(self):
        """辺パス
        Examples
        --------
        list
            ["this","is","a","edge","path"]
        """
        return self._edge_path

    @property
    def intermachine(self):
        """ステートマシン間の通信手段"""
        return self._intermachine
