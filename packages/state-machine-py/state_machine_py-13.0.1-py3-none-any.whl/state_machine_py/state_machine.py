import time
import queue
from state_machine_py.request import Request


class StateMachine():
    """状態遷移マシーン（State diagram machine）

    Example
    -------
    # Contextクラス、state_creator_dictディクショナリー, transition_dictディクショナリー は別途作っておいてください

    context = Context()
    sm = StateMachine(context, state_creator_dict=state_creator_dict, transition_dict=transition_dict)

    sm._arrive("[Init]") # Init状態は作っておいてください
    """

    def __init__(self, context=None, state_creator_dict={}, transition_dict={}, intermachine=None, name=None):
        """初期化

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です。 Defaults to None.
        state_creator_dict : dict
            状態を作成する関数のディクショナリーです。 Defaults to {}.
        transition_dict : dict
            遷移先の状態がまとめられたディクショナリーです。 Defaults to {}.
        """
        self._context = context
        self._state_creator_dict = state_creator_dict
        self._transition_dict = transition_dict
        self._verbose = False
        self._edge_path = []
        self._lines_getter = None  # 標準入力とか１個しかないけど
        self._state = None
        self._is_terminate = False  # 永遠に停止
        self._intermachine = intermachine
        self._name = name
        self._input_queue = queue.Queue()

    @property
    def context(self):
        """このステートマシンは、このContextが何なのか知りません。
        外部から任意に与えることができる変数です"""
        return self._context

    @context.setter
    def context(self, val):
        self._context = val

    @property
    def state(self):
        """現在の状態"""
        return self._state

    @property
    def edge_path(self):
        """現在の辺"""
        return self._edge_path

    @property
    def verbose(self):
        """標準出力にデバッグ情報を出力するなら真"""
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        self._verbose = val

    @property
    def is_terminate(self):
        """永遠に停止"""
        return self._is_terminate

    @property
    def input_queue(self):
        """入力キュー"""
        return self._input_queue

    @property
    def name(self):
        """他のステートマシンと区別するためのキーとして使われます"""
        return self._name

    def terminate(self):
        """ステートマシンを終了させます"""
        if self.verbose:
            print(
                f"{self._alternate_state_machine_name()} Terminate")

        self._is_terminate = True

        req = Request(
            context=self._context,
            edge_path=self.edge_path,
            intermachine=self._intermachine)
        self.on_terminate(req)

    def dequeue_item(self):
        # queue の get() でブロックするとデッドロックしてしまう
        while True:
            # ステートマシンの終了のタイミングの３つ目です。ループの先頭で終了させます
            if self._is_terminate:
                if self.verbose:
                    print(
                        f"{self._alternate_state_machine_name()} Terminate the state machine (Dequeue)")
                return None  # 関数を終わります

            try:
                line = self._input_queue.get(
                    block=False)
                self._input_queue.task_done()

                if self.verbose:
                    print(
                        f"{self._alternate_state_machine_name()} Dequeue line={line}")
                return line

            except queue.Empty:
                pass

            time.sleep(0)

    def start(self, next_state_name):
        """ステートマシンを開始します"""

        # [Arrive] --> [Leave] を最小単位とするループです。
        # しかしコードは [Leave] --> [Arrive] になってしまっているので
        # スタート直後の１回だけ [Leave] をスキップしてください
        is_skip_leave = True

        # 無限ループ
        while True:

            # ステートマシンの終了のタイミングの１つ目です。 ループの先頭で終了させます
            if self._is_terminate:
                if self.verbose:
                    print(
                        f"{self._alternate_state_machine_name()} Terminate the state machine (Loop A begin)")
                return  # start関数を終わります

            if self.verbose:
                print(
                    f"{self._alternate_state_machine_name()} Loop(A) Begin next_state_name={next_state_name}")

            # 次のループの初回だけ、無条件に通ります
            is_enter_loop = True

            # キューに内容がある間、繰り返します
            while is_enter_loop or not self._input_queue.empty:

                # ステートマシンの終了のタイミングの２つ目です。ループの先頭で終了させます
                if self._is_terminate:
                    if self.verbose:
                        print(
                            f"{self._alternate_state_machine_name()} Terminate the state machine (Loop B begin)")
                    return  # start関数を終わります

                is_enter_loop = False

                if self.verbose:
                    print(
                        f"{self._alternate_state_machine_name()} Loop(B) Begin")

                if is_skip_leave:
                    # 初回の Leave をスキップしました
                    if self.verbose:
                        print(
                            f"{self._alternate_state_machine_name()} Passed first leave")
                    is_skip_leave = False
                else:
                    if self.verbose:
                        print(
                            f"{self._alternate_state_machine_name()} Wait GetQueueline")

                    # +-------+
                    # |       |
                    # | Leave |
                    # |       |
                    # +-------+
                    next_state_name = self._leave()

                    if self.verbose:
                        print(
                            f"{self._alternate_state_machine_name()} After leave next_state_name={next_state_name}")

                    # ステートマシンの終了のタイミングの４つ目です。ループの先頭で終了させます
                    if next_state_name is None:
                        self.terminate()

                        if self.verbose:
                            print(
                                f"{self._alternate_state_machine_name()} Terminate the state machine (After leave)")
                        return  # start関数を終わります

                if self.verbose:
                    print(
                        f"{self._alternate_state_machine_name()} Before arrive next_state_name={next_state_name}")

                # ループの初回はここから始まります
                #
                # +--------+
                # |        |
                # | Arrive |
                # |        |
                # +--------+
                self._arrive(next_state_name)

            if self.verbose:
                print(
                    f"{self._alternate_state_machine_name()} Queue is empty")

            # このままでは いつまでも ここを通るので 少し待ってみます
            time.sleep(0.016)  # TODO スリープタイムを設定できたい

            # ここまでが１つの処理です

    def _alternate_state_machine_name(self):
        if self.name is None:
            return "[[state_machine]]"
        else:
            return self.name

    def _arrive(self, next_state_name):
        """指定の状態に遷移します
        entryコールバック関数を呼び出します。

        Parameters
        ----------
        str : next_state_name
            次の状態の名前
        """

        if self.verbose:
            edge_path = '/'.join(self._edge_path)
            print(
                f"{self._alternate_state_machine_name()} Arrive to {next_state_name} {edge_path}")

        if next_state_name in self._state_creator_dict:
            # 次のステートへ引継ぎ
            self._state = self._state_creator_dict[next_state_name]()

            req = Request(context=self._context,
                          edge_path=self._edge_path,
                          intermachine=self._intermachine)

            self._state.entry(req)

        else:
            # Error
            raise ValueError(f"Next state [{next_state_name}] is not found")

    def _leave(self):
        """次の状態の名前と、遷移に使ったキーを返します。
        exitコールバック関数を呼び出します。
        stateの遷移はまだ行いません

        Returns
        -------
        str
            次の状態の名前
        """

        req = Request(
            context=self._context,
            edge_path=self.edge_path,
            intermachine=self._intermachine)
        next_edge_name = self._state.exit(req)

        if self.verbose:
            print(
                f"{self._alternate_state_machine_name()} After exit next_edge_name={next_edge_name}")

        # exitがNoneを返すのは Terminate したからとします
        if next_edge_name is None:
            if self.verbose:
                print(
                    f"{self._alternate_state_machine_name()} Terminate the state machine (After exit)")
            return  # 関数を終わります

        # 例えば [Apple]ステート に居るとき ----Banana----> エッジに去るということは、
        #
        # "[Apple]": {
        #     "----Banana---->" : "[Zebra]"
        # }
        #
        # "[Apple]": {
        #     "----Banana---->" : {
        #         "----Cherry---->" : "[Zebra]"
        #     }
        # }
        #
        # "[Apple]": {
        #     "----Banana---->" : None
        # }
        #
        # といった方法で値を取ってきます。
        # 値は "[Zebra]"文字列かも知れませんし、 "----Cherry---->"ディクショナリーかもしれませんし、
        # None かもしれません。

        # まずはカレントステートを指定してディクショナリーを取ってきましょう
        if self.state.name in self._transition_dict:
            curr_dict = self._transition_dict[self.state.name]
            if curr_dict is None:
                self.terminate()
                return
        else:
            raise ValueError(
                f"Current state is not found. name=[{self.state.name}]")

        # カレントエッジを下りていきましょう
        for i, edge in enumerate(self._edge_path):
            if edge in curr_dict:
                curr_dict = curr_dict[edge]
                if curr_dict is None:
                    self.terminate()
                    return
            else:
                raise ValueError(
                    f"Edge[{i}] is not found. name=[{edge}] path=[{self._edge_path}]")

        # 最後に、次のエッジへ下りていきましょう
        if next_edge_name == '':
            # （Noneではなく）空文字を指定したら、踏みとどまります
            next_state_name = self.state.name  # まだ現在のステートです

        elif next_edge_name in curr_dict:
            # ディクショナリーか、文字列のどちらかです
            obj = curr_dict[next_edge_name]

            if type(obj) is str:
                # State
                next_state_name = obj
                self._edge_path = []  # 辺パスをクリアーします
            else:
                # Edge
                next_state_name = self.state.name  # まだ現在のステートです
                self._edge_path.append(next_edge_name)  # 辺パスを伸ばします
        else:
            raise ValueError(
                f"Next edge is not found. name=[{next_edge_name}] current state=[{self.state.name}] path=[{self._edge_path}]")

        return next_state_name

    def on_line(self, line):
        pass

    def on_terminate(self, req):
        """永遠に停止

        Parameters
        ----------
        req : Request
            ステートマシンからステートへ与えられる引数のまとまり
        """
        pass
