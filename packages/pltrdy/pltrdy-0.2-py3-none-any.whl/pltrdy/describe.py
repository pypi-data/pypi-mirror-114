import sys


def has_module(module_name):
    return module_name in sys.modules


def tab_print(*args, sep="        ", lvl=0, **kwargs):
    args = list(args)
    if lvl > 0:
        tabs = sep * lvl
        args[0] = tabs + args[0]
    print(*args, **kwargs)


def describe(o, max_elements=20, max_depth=100, depth=1, file=sys.stdout):
    def _print(*args, **kwargs):
        print(*args, **kwargs, file=file)

    next_kwargs = {
        "max_elements": max_elements,
        "max_depth": (max_depth - 1),
        "depth": (depth + 1),
        "file": file,
    }

    lines = []

    if max_depth == 0:
        _print("(max depth reached)")
        return

    if isinstance(o, dict):
        keys = o.keys()
        n = len(o)
        _print("Dict (len: %d)" % n)
        if n <= max_elements:
            keys = sorted(o.keys())
            for k in keys:
                v = o[k]
                tab_print("%s:" % k, lvl=depth, end=" ", file=file)
                describe(v, **next_kwargs)
    elif isinstance(o, list):
        n = len(o)
        _print("List (len: %d)" % n)
        if n <= max_elements:
            for i, v in enumerate(o):
                tab_print("#%d:" % i, lvl=depth, end=" ", file=file)
                describe(v, **next_kwargs)
    elif has_module("torch"):
        import torch
        if isinstance(o, torch.Tensor):
            tensor_shape = str(list(o.size()))
            tensor_type = str(o.type())

            _print("%s: %s" % (tensor_type, tensor_shape))
    else:
        _print(repr(o))


def describe_str(*args, **kwargs):
    from io import StringIO
    s = StringIO()
    describe(*args, file=s, **kwargs)

    return s.getvalue()


def describe_lines(*args, **kwargs):
    return describe_str(*args, **kwargs).split("\n")
