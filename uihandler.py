import curses

class UIHandler:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        height, width = self.stdscr.getmaxyx()
        self.history_win = curses.newwin(height - 3, width // 2, 0, 0)
        self.output_win = curses.newwin(height - 3, width // 2, 0, width // 2)
        self.alert_win = curses.newwin(1, width, height - 2, 0)  # New alert window
        self.input_win = curses.newwin(1, width, height - 1, 0)

    def update_history(self, history):
        self.history_win.clear()
        for i, command in enumerate(history):
            self.history_win.addstr(i, 0, command)
        self.history_win.refresh()

    def update_output(self, output):
        self.output_win.clear()
        self.output_win.addstr(0, 0, output)
        self.output_win.refresh()

    def update_alert(self, alert):
        self.alert_win.clear()
        height, width = self.alert_win.getmaxyx()
        self.alert_win.addstr(0, 0, alert[:width - 1])
        self.alert_win.refresh()

    def get_command(self):
        self.input_win.clear()
        curses.start_color() # Enable color
        curses.use_default_colors()  # Use default colors
        curses.init_pair(1, curses.COLOR_YELLOW, -1)  # Yellow text with default background color
        curses.init_pair(2, curses.COLOR_WHITE, -1)  # White text with default background color
        self.input_win.addstr(0, 0, "Enter a command ", curses.color_pair(1))
        self.input_win.addstr("# ", curses.color_pair(2))
        curses.echo()  # Enable echoing of input
        command = self.input_win.getstr().decode()
        curses.noecho()  # Disable echoing of input
        self.input_win.refresh()
        return command
        
    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()