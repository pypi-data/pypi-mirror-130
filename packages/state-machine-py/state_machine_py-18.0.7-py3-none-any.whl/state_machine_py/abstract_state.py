class AbstractState():
    """状態"""

    def __init__(self):
        pass

    def update(self, req):
        """この状態から抜け出たときに呼び出されます。ただし初期化時、アボート時は呼び出されません

        Parameters
        ----------
        req : Request
            ステートマシンからステートへ与えられる引数のまとまり

        Returns
        -------
        str
            次（下位）の辺の名前

        Examples
        --------
        req.intermachine.enqueue_myself("Login")
        自分（ステートマシン）の入力キューに "Login" の文字を送ります

        line = req.intermachine.dequeue_myself()
        自分（ステートマシン）の入力キューから何かの文字を取り出します。
        ステートマシンが終了するとNoneを返すので、すぐにこの関数から抜けてください
        """
        return None
