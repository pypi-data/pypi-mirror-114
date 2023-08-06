from antidote import Constants, const


class Config(Constants):
    HOST = const[str]("localhost")
    PORT = const[int](27017)
    USER = const[str]("")
    PASSWORD = const[str]("")
    DATABASE = const[str]("test_asterisk")

    # def __init__(self):
    #     self._data = dict(host=self.HOST, port=self.PORT)

    # def provide_const(self, name: str, arg: str):
    #     # Only called when needed.
    #     return self._data[arg]


# class Conf(ProductionEnvironment):
#     pass
