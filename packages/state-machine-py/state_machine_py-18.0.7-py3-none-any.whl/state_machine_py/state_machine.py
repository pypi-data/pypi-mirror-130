import time
import queue
from state_machine_py.request import Request
from state_machine_py.state_machine_helper import StateMachineHelper


class StateMachine():
    """状態遷移マシーン（State diagram machine）

    Example
    -------
    # Context クラス、 state_gen ディクショナリー、 transition ディクショナリー は別途作っておいてください

    context = Context()
    sm = StateMachine(context, state_gen=state_gen, transition=transition)

    # Init状態は作っておいてください
    self._state = StateMachineHelper.create_state(state_gen, [INIT])
    """

    def __init__(self, context=None, state_gen={}, transition={}, intermachine=None, name=None):
        """初期化

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です。 Defaults to None.
        state_gen : dict
            状態を作成する関数のディクショナリーです。 Defaults to {}.
        transition : dict
            遷移先の状態がまとめられたディクショナリーです。 Defaults to {}.
        """
        self._context = context
        self._state_gen = state_gen
        self._transition = transition
        self._verbose = False
        self._state_path = None
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
    def state_path(self):
        """状態パス"""
        return self._state_path

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
            state_path=self.state_path,
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

    def start(self, start_state_path):
        """ステートマシンを開始します

        Parameters
        ----------
        start_state_path : list
            開始時の状態パス
        """
        self._state_path = start_state_path

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
                    f"{self._alternate_state_machine_name()} Loop(A) Begin _state_path={self._state_path}")

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

                    # +--------+
                    # |        |
                    # | Update |
                    # |        |
                    # +--------+
                    req = Request(
                        context=self._context,
                        state_path=self.state_path,
                        intermachine=self._intermachine)

                    next_edge_name = self._state.update(req)

                    if self.verbose:
                        print(
                            f"{self._alternate_state_machine_name()} After update next_edge_name={next_edge_name}")

                    # update がNoneを返すのは Terminate したからとします
                    if next_edge_name is None:
                        if self.verbose:
                            print(
                                f"{self._alternate_state_machine_name()} next_edge_name is None (212)")
                        self.terminate()
                        return  # 関数を終わります

                    # +-----------------+
                    # |                 |
                    # | Next state path |
                    # |                 |
                    # +-----------------+
                    self._state_path = StateMachineHelper.lookup_next_state_path(
                        self._transition, self._state_path, next_edge_name)

                    if self.verbose:
                        print(
                            f"{self._alternate_state_machine_name()} After lookup_next_state_path _state_path={self._state_path}")

                    # update がNoneを返すのは Terminate したからとします
                    if self._state_path is None:
                        if self.verbose:
                            print(
                                f"{self._alternate_state_machine_name()} self._state_path is None (212)")
                        self.terminate()
                        return  # 関数を終わります

                if self.verbose:
                    print(
                        f"{self._alternate_state_machine_name()} Before arrive _state_path={self._state_path}")

                # ループの初回はここから始まります
                #
                # +--------+
                # |        |
                # | Arrive |
                # |        |
                # +--------+
                if self.verbose:
                    state_path_str = '/'.join(self._state_path)
                    print(
                        f"{self._alternate_state_machine_name()} Arrive to {state_path_str}")

                # +--------------+
                # |              |
                # | Create state |
                # |              |
                # +--------------+
                # 次のステートへ引継ぎ
                self._state = StateMachineHelper.create_state(
                    self._state_gen, self._state_path)

            if self.verbose:
                print(
                    f"{self._alternate_state_machine_name()} Queue is empty")

            # このままでは いつまでも ここを通るので 一瞬だけ他の処理に譲ります
            time.sleep(0)

            # ここまでが１つの処理です

    def _alternate_state_machine_name(self):
        if self.name is None:
            return "[[state_machine]]"
        else:
            return self.name

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
