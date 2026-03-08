#!/usr/bin/env python3
"""
WiFi Password Viewer CLI
View saved WiFi passwords on Windows, macOS, Linux
"""

import argparse
import subprocess
import sys
import platform
import re
import json

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False

try:
    import pyperclip
    CLIPBOARD = True
except ImportError:
    CLIPBOARD = False

def cprint(text, color=Fore.WHITE, **kwargs):
    if COLOR:
        print(color + text + Style.RESET_ALL, **kwargs)
    else:
        print(text, **kwargs)

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        cprint(f"Error executing command: {e}", Fore.RED)
        sys.exit(1)

def get_windows_profiles():
    output = run_command(["netsh", "wlan", "show", "profiles"])
    profiles = []
    for line in output.splitlines():
        if "All User Profile" in line:
            ssid = line.split(":", 1)[1].strip()
            profiles.append(ssid)
    return profiles

def get_windows_password(ssid):
    cmd = ["netsh", "wlan", "show", "profile", f"name={ssid}", "key=clear"]
    output = run_command(cmd)
    password = None
    for line in output.splitlines():
        if "Key Content" in line:
            password = line.split(":", 1)[1].strip()
            break
    return password

def get_macos_profiles():
    output = run_command(["networksetup", "-listpreferredwirelessnetworks", "en0"])
    profiles = [line.strip() for line in output.splitlines()[1:] if line.strip()]
    return profiles

def get_macos_password(ssid):
    cmd = ["security", "find-generic-password", "-ga", ssid]
    try:
        output = run_command(cmd)
        password = None
        for line in output.splitlines():
            if "password:" in line.lower():
                password = re.search(r'"(.*)"', line)
                if password:
                    return password.group(1)
        return None
    except:
        return None

def get_linux_profiles():
    try:
        output = run_command(["nmcli", "-f", "NAME", "connection", "show"])
        profiles = [line.strip() for line in output.splitlines()[1:] if line.strip()]
        return [p for p in profiles if "wifi" in run_command(["nmcli", "connection", "show", p])]
    except:
        return []

def get_linux_password(ssid):
    try:
        output = run_command(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid])
        return output.strip() if output else None
    except:
        return None

def main():
    parser = argparse.ArgumentParser(
        description="View saved WiFi passwords on your machine",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--ssid", type=str, help="Show password for specific SSID only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--clipboard", action="store_true", help="Copy output to clipboard (requires pyperclip)")
    parser.add_argument("--list-only", action="store_true", help="List SSIDs only, no passwords")

    args = parser.parse_args()

    system = platform.system().lower()

    if system == "windows":
        profiles = get_windows_profiles()
        get_pass_func = get_windows_password
    elif system == "darwin":  # macOS
        profiles = get_macos_profiles()
        get_pass_func = get_macos_password
    elif system == "linux":
        profiles = get_linux_profiles()
        get_pass_func = get_linux_password
    else:
        cprint(f"Unsupported OS: {platform.system()}", Fore.RED)
        sys.exit(1)

    if not profiles:
        cprint("No saved WiFi profiles found.", Fore.YELLOW)
        return

    results = []

    if args.ssid:
        if args.ssid not in profiles:
            cprint(f"SSID '{args.ssid}' not found.", Fore.RED)
            return
        profiles = [args.ssid]

    if args.list_only:
        cprint("\nSaved WiFi Networks:", Fore.CYAN)
        for ssid in profiles:
            print(f"  - {ssid}")
        return

    for ssid in profiles:
        password = get_pass_func(ssid)
        if password:
            results.append({"ssid": ssid, "password": password})
            if not args.json:
                cprint(f"SSID     : {ssid}", Fore.CYAN)
                cprint(f"Password : {password}", Fore.GREEN)
                print("-" * 40)
        else:
            if not args.json:
                cprint(f"SSID     : {ssid}", Fore.CYAN)
                cprint("Password : Not found / Not accessible", Fore.YELLOW)
                print("-" * 40)

    if args.json:
        print(json.dumps(results, indent=2))

    if args.clipboard and CLIPBOARD:
        if args.json:
            pyperclip.copy(json.dumps(results, indent=2))
        else:
            output_text = "\n".join([f"{r['ssid']}: {r['password']}" for r in results if r.get('password')])
            pyperclip.copy(output_text)
        cprint("\nOutput copied to clipboard!", Fore.GREEN)

if __name__ == "__main__":
    main()
