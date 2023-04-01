def console_overwrite(text: str):
    print(text, end="\033[K\r")
