from typing import Any, Callable, Generic, NoReturn, TypeVar, Union


T = TypeVar("T")
E = TypeVar("E", bound=BaseException)


class Ok(Generic[T, E]):
    _value: T
    __match_args__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self.unwrap()

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self.unwrap()

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"

class Err(Generic[T, E]):
    _err: E
    __match_args__ = ("_err",)

    def __init__(self, err: E):
        self._err = err

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Err):
            return self._err == other._err
        return False

    def unwrap(self) -> NoReturn:
        raise self._err

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self._err)

    def __repr__(self) -> str:
        return f"Err({repr(self._err)})"

Result = Union[Ok[T, E], Err[T, E]]

# def devide(x: float, y: float) -> Result[float, ZeroDivisionError]:
#     if y == 0:
#         return Err(ZeroDivisionError("Cannot divide by 0"))
#     return Ok(x / y)

# match devide(3, 2):
#     case Ok(v):
#         test = v
#     case Err(e):
#         print(f"The error is `{e}`")
#         test = "error"

# print(test)
# print("ok")
