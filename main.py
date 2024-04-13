import os
import subprocess
from enum import StrEnum
from pathlib import Path

WORKSPACE = Path(__file__).parent
DESKTOP_SESSION = os.environ.get("DESKTOP_SESSION")
ROFI = Path("/usr/bin/rofi")


class Option(StrEnum):
    SHUTDOWN = "\uf011"
    REBOOT = "\uf2ea"
    LOCK = "\uf023"
    LOGOUT = "\uf2f5"
    SUSPEND = "\uf28b"
    HIBERNATE = "\uf192"
    UEFI = "\uf2db"


def popup(msg: str) -> None:
    popup_msg = subprocess.run([ROFI, "-e", msg], capture_output=True)
    if popup_msg.stderr:
        raise Exception("Failed to display popup.")


def main() -> None:
    power_menu = subprocess.run(
        [
            ROFI,
            "-dmenu",
            "-theme",
            WORKSPACE / "themes/power_menu.rasi",
        ],
        input="\n".join(list(Option)),
        encoding="utf-8",
        capture_output=True,
    )

    if power_menu.stderr:
        popup(f"Command {ROFI} failed: {power_menu.stderr}")
        return

    power_opt = power_menu.stdout.strip()
    if not power_opt:
        return

    confirm_prompt = subprocess.run(
        [
            ROFI,
            "-dmenu",
            "-p",
            "Are you sure?",
            "-theme",
            WORKSPACE / "themes/confirm.rasi",
        ],
        input="Yes\nNo",
        encoding="utf-8",
        capture_output=True,
    )

    if confirm_prompt.stderr:
        popup(f"Command {ROFI} failed: {confirm_prompt.stderr}")
        return

    confirm_opt = confirm_prompt.stdout.strip()
    if confirm_opt != "Yes":
        return

    match power_opt:
        case Option.SHUTDOWN:
            power_cmd = ["poweroff"]

        case Option.REBOOT:
            power_cmd = ["reboot"]

        case Option.LOCK:
            match DESKTOP_SESSION:
                case "hyprland":
                    power_cmd = ["swaylock"]
                case _:
                    return

        case Option.LOGOUT:
            match DESKTOP_SESSION:
                case "hyprland":
                    power_cmd = ["hyprctl", "dispatch", "exit"]
                case "qtile":
                    power_cmd = ["qtile", "cmd-obj", "-o", "cmd", "-f", "shutdown"]
                case _:
                    popup(f"Desktop session '{DESKTOP_SESSION}' not recognized.")
                    raise NotImplementedError()

        case Option.SUSPEND:
            power_cmd = ["systemctl", "suspend"]

        case Option.HIBERNATE:
            power_cmd = ["systemctl", "hibernate"]

        case Option.UEFI:
            supports_uefi = Path("/sys/firmware/efi").exists()
            if not supports_uefi:
                popup(f"The system does not support UEFI.")
                return

            power_cmd = ["systemctl", "reboot", "--firmware-setup"]
        case "":
            return
        case _:
            raise Exception("Unreachable")

    subprocess.run(power_cmd)


if __name__ == "__main__":
    main()
