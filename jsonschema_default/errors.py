class RefCycleError(RuntimeError):
    def __init__(self, refs: list[str]):
        super().__init__(" -> ".join(refs))
