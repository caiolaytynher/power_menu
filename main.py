#!/home/caio/.pyenv/versions/3.12.2/bin/python

import os
import subprocess
from enum import StrEnum
from pathlib import Path

WORKSPACE = Path(__file__).parent


class PowerOffOpt(StrEnum):
    SHUTDOWN = ""
    REBOOT = ""
    LOGOUT = ""


class ConfirmOpt(StrEnum):
    YES = "Yes"
    NO = "No"


def main() -> None:
    theme = {
        "power_off": str(WORKSPACE / "themes/power_off.rasi"),
        "confirm": str(WORKSPACE / "themes/confirm.rasi"),
    }

    power_off_opts = "\n".join(list(PowerOffOpt))

    power_off_process = subprocess.run(
        ["/usr/bin/rofi", "-dmenu", "-theme", theme["power_off"]],
        input=power_off_opts,
        encoding="utf-8",
        capture_output=True,
    )

    if power_off_process.stderr:
        return

    power_off_opt = power_off_process.stdout.strip()
    if not power_off_opt:
        return

    confirm_process = subprocess.run(
        ["/usr/bin/rofi", "-dmenu", "-p", "Are you sure?", "-theme", theme["confirm"]],
        input="Yes\nNo",
        encoding="utf-8",
        capture_output=True,
    )

    if confirm_process.stderr:
        return

    confirm_opt = confirm_process.stdout.strip()
    if confirm_opt == ConfirmOpt.NO or not confirm_opt:
        return

    match power_off_opt:
        case PowerOffOpt.SHUTDOWN:
            cmd = ["poweroff"]
        case PowerOffOpt.REBOOT:
            cmd = ["reboot"]
        case PowerOffOpt.LOGOUT:
            desktop_session = os.environ.get("DESKTOP_SESSION")
            match desktop_session:
                case "hyprland":
                    cmd = ["hyprctl", "dispatch", "exit"]
                case "qtile":
                    cmd = ["qtile", "cmd-obj", "-o", "cmd", "-f", "shutdown"]
                case _:
                    return
        case _:
            return

    subprocess.run(cmd)


if __name__ == "__main__":
    main()
