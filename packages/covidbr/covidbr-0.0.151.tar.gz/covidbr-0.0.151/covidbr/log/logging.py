from .puts import puts

show_logs = False

def show_console(argument:bool):
    global show_logs
    show_logs = argument


def log(*txt,sep=' '):
    if show_logs:
        return puts(*txt,sep=sep)
    else:
        pass