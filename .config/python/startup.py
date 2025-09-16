import readline

readline.write_history_file = lambda *args: None
readline.set_auto_history(False)
