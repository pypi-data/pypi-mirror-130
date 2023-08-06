class ProcError(OSError):pass
class ProcessKilledWarning(UserWarning):pass
class DuplicationWarning(UserWarning):pass
class DuplicationError(ProcError):pass
class FDError(ProcError):pass
