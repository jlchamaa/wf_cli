import curses
import logging
log = logging.getLogger("wfcli")


class NormalMode:
    key_mapping = {
        (ord('d'), ord('d')): "delete_item",
        (ord('c'),): "complete",
        (ord('i'),): "edit_item",
        (ord('k'),): "nav_up",
        (ord('j'),): "nav_down",
        (ord('h'),): "nav_left",
        (ord('l'),): "nav_right",
        (ord('o'),): "open_below",
        (ord('p'),): "print_data",
        (ord('q'),): "quit_app",
        (ord('s'),): "save_data",
        (ord('u'),): "undo",
        (9,): "indent",            # TAB
        (10,): "open_below",       # ENTER
        (27, 91, 90): "unindent",  # SHIFT-TAB
    }

    def __init__(self, sc):
        self.sc = sc

    @property
    def indicators(self):
        return {"closed": ">", "open": "v", "item": "-"}

    @property
    def note(self):
        return "Normal Mode"

    @property
    def selection(self):
        return curses.A_REVERSE

    def get_keypress(self):
        while True:
            keypress = self.sc.getch()
            if keypress < 0:
                continue
            elif keypress == 27:  # an ESCAPE code
                key_combo = []
                while keypress >= 0:
                    key_combo.append(keypress)
                    keypress = self.sc.getch()
            elif keypress in [100]:  # combo keys
                key_combo = [keypress]
                keypress = -1
                while keypress < 0:
                    keypress = self.sc.getch()
                key_combo.append(keypress)
            else:
                key_combo = [keypress]
            key_combo = tuple(key_combo)
            return key_combo

    def get_command(self):
        while True:
            key_combo = self.get_keypress()
            if key_combo in self.key_mapping:
                result = self.key_mapping[key_combo]
                return (result, {})
            else:
                log.error("This command is dogshit - {}".format(key_combo))
