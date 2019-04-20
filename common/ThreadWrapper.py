from threading import Thread


class ThreadWrapper:
    def __init__(self, whatClass, initArgs, startFunctions):
        """
            startFunctions: is a tuple of tuples like 
                (
                    ("funcCalledFirst", (arg1, arg2)),
                    (funcCalledSecond, (arg1, arg2)),
                    ...
                )
        """
        self.t = Thread(target=self._start)
        self.cls = whatClass(initArgs)
        self.startFunctions = startFunctions

    def start(self):
        self.t.start()

    def _start(self):
        for func in self.startFunctions:
            getattr(self.cls, func[0])(func[1])