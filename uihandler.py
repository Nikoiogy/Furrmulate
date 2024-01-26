import curses

class UIHandler:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        height, width = self.stdscr.getmaxyx()
        self.history_win = curses.newwin(height - 2, width // 2, 0, 0)
        self.output_win = curses.newwin(height - 3, width // 2, 0, width // 2)
        self.alert_win = curses.newwin(1, width, height - 2, 0)  # New alert window
        self.input_win = curses.newwin(1, width, height - 1, 0)

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
        self.output_win.clear()
        self.output_win.addstr(0, 0, output)
        self.output_win.refresh()

    def update_alert(self, alert):
        self.alert_win.clear()
        height, width = self.alert_win.getmaxyx()
        curses.init_pair(3, curses.COLOR_RED, -1)  # Red text with default background color
        self.alert_win.addstr(0, 0, alert[:width - 1], curses.color_pair(3))
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

    def map_handler(self, dungeon):
        def get_cell_char(cell):
            return cell.symbol + " "

        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        map_height = height - 3
        map_width = width // 2

        if len(dungeon) > map_height or len(dungeon[0]) > map_width:
            camera_x = max(0, len(dungeon[0]) - map_width)
            camera_y = max(0, len(dungeon) - map_height)

            while True:
                key = self.stdscr.getch()
                if key == ord('e'):  # Exit the map if 'e' is pressed
                    return "Exited map view."
                elif key == curses.KEY_UP and camera_y > 0:
                    camera_y -= 1
                elif key == curses.KEY_DOWN and camera_y < len(dungeon) - map_height:
                    camera_y += 1
                elif key == curses.KEY_LEFT and camera_x > 0:
                    camera_x -= 1
                elif key == curses.KEY_RIGHT and camera_x < len(dungeon[0]) - map_width:
                    camera_x += 1

                for y in range(map_height):
                    for x in range(map_width):
                        if y + camera_y < len(dungeon) and x + camera_x < len(dungeon[0]):
                            self.stdscr.addch(y, x, get_cell_char(dungeon[y + camera_y][x + camera_x]))
                self.stdscr.refresh()
        else:
            for y in range(len(dungeon)):
                for x in range(len(dungeon[0])):
                    self.stdscr.addch(y, x, get_cell_char(dungeon[y][x]))

        self.stdscr.refresh()
        
        
    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()