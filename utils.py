"""
General utilities for building functions
"""
import sys
import types


def check_param(*args, p:str='') -> None:
    """
    Asserts the preconditions specified in args for parameter.
    
    Preconditions can be types or equalities. Ex: (str, ">= 4", "<100")
    
    This function displays a helpful little error message stating the parameter,
    function, and precondition violated.

    :param args: The preconditions to assert as explained above
    :param p: The name of the parameter to check as a str (this function looks up the value using the name)
    :return: None
    """
    assert p, "You forgot to set p in utils.check_param"
    frame = sys._getframe(1)
    pv = frame.f_locals[p]
    func_name = frame.f_code.co_name
    for x in args:
        if isinstance(x, type | types.UnionType):
            assert isinstance(pv, x), f"{func_name}(): {p} is not {x}"
        elif isinstance(x, str):
            equals = x[1] == '='
            if x[0] == '>':
                assert pv >= float(x[2:]) if equals else pv > float(x[1:]), (
                f"{func_name}(): {p} is not {x}")
            elif x[0] == '<':
                assert pv >= float(x[2:]) if equals else pv < float(x[1:]), (
                f"{func_name}(): {p} is not {x}")
        else:
            continue