#!/home/caio/.pyenv/versions/3.12.2/bin/python

import os
import subprocess
from enum import StrEnum
from pathlib import Path

WORKSPACE = Path(__file__).parent


class PowerOffOpt(StrEnum):
    SHUTDOWN = "\uf011"
    REBOOT = "\uf2ea"
    LOCK = "\uf023"
    LOGOUT = "\uf2f5"
    SUSPEND = "\uf28b"
    HIBERNATE = "\uf192"
    UEFI = "\uf2db"


def main() -> None:
    theme = {
        "power_off": str(WORKSPACE / "themes/power_off.rasi"),
        "confirm": str(WORKSPACE / "themes/confirm.rasi"),
    }

    power_off_opts = "\n".join(list(PowerOffOpt))

    power_off_prompt = subprocess.run(
        ["/usr/bin/rofi", "-dmenu", "-theme", theme["power_off"]],
        input=power_off_opts,
        encoding="utf-8",
        capture_output=True,
    )

    if power_off_prompt.stderr:
        return

    power_off_opt = power_off_prompt.stdout.strip()
    if not power_off_opt:
        return

    confirm_prompt = subprocess.run(
        ["/usr/bin/rofi", "-dmenu", "-p", "Are you sure?", "-theme", theme["confirm"]],
        input="Yes\nNo",
        encoding="utf-8",
        capture_output=True,
    )

    if confirm_prompt.stderr:
        return

    confirm_opt = confirm_prompt.stdout.strip()
    if confirm_opt == "No" or not confirm_opt:
        return

    desktop_session = os.environ.get("DESKTOP_SESSION")

    match power_off_opt:
        case PowerOffOpt.SHUTDOWN:
            power_off_cmd = ["poweroff"]

        case PowerOffOpt.REBOOT:
            power_off_cmd = ["reboot"]

        case PowerOffOpt.LOCK:
            match desktop_session:
                case "hyprland":
                    power_off_cmd = ["swaylock"]
                case _:
                    return

        case PowerOffOpt.LOGOUT:
            match desktop_session:
                case "hyprland":
                    power_off_cmd = ["hyprctl", "dispatch", "exit"]
                case "qtile":
                    power_off_cmd = ["qtile", "cmd-obj", "-o", "cmd", "-f", "shutdown"]
                case _:
                    return

        case PowerOffOpt.SUSPEND:
            power_off_cmd = ["systemctl", "suspend"]

        case PowerOffOpt.HIBERNATE:
            power_off_cmd = ["systemctl", "hibernate"]

        case PowerOffOpt.UEFI:
            support_uefi = Path("/sys/firmware/efi").exists()
            if not support_uefi:
                return

            power_off_cmd = ["systemctl", "reboot", "--firmware-setup"]
        case _:
            return

    subprocess.run(power_off_cmd)


if __name__ == "__main__":
    main()
