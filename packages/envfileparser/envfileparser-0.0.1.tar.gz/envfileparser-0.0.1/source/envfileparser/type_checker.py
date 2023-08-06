def is_int(*args) -> bool:
    try:
        for v in args:
            int(v)
        return True
    except ValueError:
        return False
