import curses

class UIHandler:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        height, width = self.stdscr.getmaxyx()
        half_width = width // 2
        half_height = height // 2

        self.history_win = curses.newwin(height - 2, half_width, 0, 0)
        self.map_win = curses.newwin(half_height, half_width, 0, half_width)  # New map window
        self.output_win = curses.newwin(half_height - 2, half_width, half_height, half_width)
        self.alert_win = curses.newwin(1, width, height - 2, 0)
        self.input_win = curses.newwin(1, width, height - 1, 0)

    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def update_history(self, history):
        self.history_win.clear()
        height, width = self.history_win.getmaxyx()
        for i, command in enumerate(reversed(history)):
            line_number = height - 2 - i
            if 0 <= line_number < height:
                if len(command) > width - 4:
                    command = command[:width - 4] + '...'
                self.history_win.addstr(line_number, 0, command)
        self.history_win.refresh()

    def update_output(self, output):
        if output is None:
            output = ""
        self.output_win.clear()
        height, width = self.output_win.getmaxyx()
        lines = output.split('\n')
        for i, line in enumerate(lines):
            if i < height:
                self.output_win.addstr(i, 0, line[:width - 1])
        self.output_win.refresh()

    def update_alert(self, alert):
        self.alert_win.clear()
        height, width = self.alert_win.getmaxyx()
        curses.init_pair(3, curses.COLOR_RED, -1)
        self.alert_win.addstr(0, 0, alert[:width - 1], curses.color_pair(3))
        self.alert_win.refresh()

    def get_command(self):
        self.input_win.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW, -1)
        curses.init_pair(2, curses.COLOR_WHITE, -1)
        self.input_win.addstr(0, 0, "Enter a command ", curses.color_pair(1))
        self.input_win.addstr("# ", curses.color_pair(2))
        curses.echo()
        command = self.input_win.getstr().decode()
        curses.noecho()
        self.input_win.refresh()
        return command

    def map_handler(self, map, player_x, player_y):
        height, width = self.map_win.getmaxyx()  # Use map_win dimensions
        map_width = len(map[0])
        map_height = len(map)
        start_x = max(0, min(map_width - width // 4, player_x - width // 4))  # Adjust for spaces
        start_y = max(0, min(map_height - height, player_y - height // 2))
        end_x = min(map_width, start_x + width // 2)  # Adjust for spaces
        end_y = min(map_height, start_y + height)
        map_string = ""
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                cell = map[y][x]
                if cell == "":
                    symbol = "_"
                else:
                    symbol = cell.symbol
                if y - start_y < height - 1 and x - start_x < width // 2:  # Adjust for spaces
                    if x == player_x and y == player_y:
                        symbol = "@"
                    map_string += symbol + " "  # Add a space after each cell
            map_string += "\n"
        self.map_win.clear()  # Clear map_win
        lines = map_string.split('\n')
        for i, line in enumerate(lines):
            if i < height:
                self.map_win.addstr(i, 0, line[:width - 1])
        self.map_win.refresh()  # Refresh map_win

    # DEBUG COMMANDS
    
    def debug_map_handler(self, map, utils):
        self.cleanup()

        for row in map:
            for cell in row:
                print(utils.color_text(cell.symbol, cell.color), end=" ")
            print()

        input("Press Enter to continue...")
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def debug_leavecurses_temporarily(self):
        input("Press Enter to continue...")
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)