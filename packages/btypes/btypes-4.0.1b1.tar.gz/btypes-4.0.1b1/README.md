# btypes

> Aliases with correct capitalization for built-in Python types.

[PEP8](https://www.python.org/dev/peps/pep-0008/#class-names) states that classes should have names in CamelCase.
However, all the built-in types are lower case: `str`, `bool`, `int`, `float`, `list`, `dict`, etc.
This library provides aliases for all these types that are capitalized correctly.
They are straightforward aliases and can be used exactly like the original types.

## Install

Requires Python 3.9+.

```
pip install btypes
```

## Examples

```python
from btypes import Int, List, Str

def comma_list(lst: List[Int]) -> Str:
    return ", ".join(Str(e) for e in lst)

def range_list(limit: Int) -> List[Int]:
    return List(range(limit))
```

Also works with pattern matching:
```python
from btypes import Bool, Str, Union

def print_type(x: Union[Bool, Str]) -> None:
    match x:
        case Bool():
            print("a boolean")
        case Str():
            print("a string")
```

## FAQs

### Why require Python 3.9 as the minimum version?

Because Python 3.9 introduced generic collections in the standard library: `list[int]`, `dict[str, float]`;
and the whole point of `btypes` is that you can use the same identifier as constructor and as type annotation.
