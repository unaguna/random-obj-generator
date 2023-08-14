import os
import typing as t


class EnvVarSnapshot:
    """環境変数のスナップショットを取得

    このインスタンスのコンテキストで試験を実施することで、その中で変更された環境変数がコンテキストを抜けるときに元に戻される。

    主に、@pytest.mark.parametrize で繰り返し試験する際に環境変数の変更が引き継がれてしまうことを防ぐために使用する。
    """

    _env: t.Mapping[str, str]

    def __enter__(self):
        self.save()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.apply()

    def save(self):
        self._env = os.environ.copy()

    def apply(self):
        os.environ.clear()
        os.environ.update(self._env)
