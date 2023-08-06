def main():
    import logging
    from sys import platform
    import os
    from typing import Any, Callable
    from tepezza import TepezzaApi

    assert platform == 'darwin', 'Cannot be called as module on non-MacOS systems'
        
    api = TepezzaApi()
    logging.basicConfig(level=logging.INFO)

    def input_with_default(s: str, default: Any, conversion_func: Callable[[str], Any] = str) -> Any:
        s = s.replace('{DEFAULT}', default)
        res = input(s)
        if res == '':
            res = default
        return conversion_func(res)

    every = input_with_default("Enter sample rate or press Enter for default {DEFAULT}. ", '5', int)
    filepath = input_with_default(
        "Where would you like data to be saved? Type a path or press Enter for default {DEFAULT}. ", 
        os.path.join(os.path.expanduser("~/Desktop"), "tepezza_data.csv")
    )
    write_out = input_with_default(
        "Enter n to disable recording to csv every cycle. Defaults to True. ", 
        "", 
        lambda s: s != "n"
    )
    start_from = input_with_default(
        "Enter a zipcode to start from. To start from beginning press Enter. ",
        '',
        lambda s: None if s == '' else s
    )

    try:
        with TepezzaApi() as api:
            api.startup()
            api.get_data(every, filepath, write_out, start_from)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()