import configparser
import os
import sys
from getopt import getopt

from gi.repository import Gio, GLib

USAGE = """
xdgterm: Launch the user's preferred terminal

USAGE:
    xdgterm [FLAGS] [--] [COMMAND]

FLAGS:
    -h, --help         Prints this help information
    -k, --hold         Keep the terminal open after the command completes

COMMAND:
    The command to run in the terminal. If not given, the default shell is executed.
"""

INTERFACE = "org.freedesktop.Terminal1"


def nul_terminated(b: bytes):
    return b + b"\0"


def env_list():
    return [k + b"=" + v + b"\0" for k, v in os.environb.items()]


def search_dirs():
    yield os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config/"))
    yield from os.getenv("XDG_CONFIG_DIRS", "/etc/xdg/").split(":")
    yield from os.getenv("XDG_DATA_DIRS", "/usr/local/share:/usr/share/").split(":")


def intent_configs():
    desktop = os.getenv("XDG_CURRENT_DESKTOP")
    for d in search_dirs():
        if desktop:
            yield os.path.join(d, desktop + "-intentapps.list")
        yield os.path.join(d, "intentapps.list")


def terminal_intent_apps():
    for f in intent_configs():
        cfg = configparser.ConfigParser()
        if cfg.read(f) == []:
            continue
        try:
            yield from cfg["Default Applications"][INTERFACE].split(";")
        except KeyError:
            continue


class XdgTerm:
    def __init__(self):
        app = self.find_launcher()
        bus_name = os.path.basename(app.get_filename())
        # strip the .desktop suffix
        if bus_name.endswith(".desktop"):
            bus_name = bus_name[:-8]

        path = "/" + bus_name.translate({ord("."): "/", ord("-"): "_"})

        # NOTE: we are assuming that the app implements dbus activation
        self.proxy = Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SESSION,
            Gio.DBusProxyFlags.DO_NOT_AUTO_START_AT_CONSTRUCTION,
            None,
            bus_name,
            path,
            INTERFACE,
        )

    def launch(self, cmd: list, keep_open=False):
        options = {}
        if keep_open:
            options["keep-terminal-open"] = True

        platform_data = {}
        startup_id = os.getenv("DESKTOP_STARTUP_ID")
        if startup_id:
            platform_data["desktop-startup-id"] = startup_id
            os.unsetenv("DESKTOP_STARTUP_ID")

        args = GLib.Variant(
            "(aayayayaaya{sv}a{sv})",
            (
                [os.fsencode(a) + b"\0" for a in cmd],
                os.getcwdb() + b"\0",  # working directory
                b"\0",  # Desktop entry
                env_list(),
                options,
                platform_data,
            ),
        )
        self.proxy.call_sync("LaunchCommand", args, Gio.DBusCallFlags.NONE, -1, None)

    def find_launcher(self):
        for desktop_id in terminal_intent_apps():
            app_info = Gio.DesktopAppInfo.new(desktop_id)
            implements = app_info.get_string_list("Implements")
            if implements and INTERFACE in implements:
                return app_info


def main():
    flags, cmd = getopt(sys.argv[1:], "hk", ["help", "hold"])

    hold = False
    for flag, _ in flags:
        if flag in ["-h", "--help"]:
            print(USAGE, file=sys.stderr)
            os.exit()
        elif flag in ["-k", "--hold"]:
            hold = True

    term = XdgTerm()
    term.launch(cmd, hold)


if __name__ == "__main__":
    main()
