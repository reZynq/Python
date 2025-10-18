#!/usr/bin/env python3
"""
extract_wifi_keys.py

- Enumerates Wi‑Fi profiles and extracts the 'Key Content' (password) if present.
- Saves results to a timestamped text/CSV-like file and per-profile raw output files.
- Works whether or not Key Content appears; if it doesn't, the password cell will be empty.
"""

import subprocess, re, time, csv
from pathlib import Path
from datetime import datetime

OUT_DIR = Path.cwd() / "wifi_output"
OUT_DIR.mkdir(exist_ok=True)
TS = datetime.now().strftime("%Y%m%d-%H%M%S")
SUMMARY_FILE = OUT_DIR / f"wifi_passwords_{TS}.txt"  # CSV-like (comma separated)
RAW_DIR = OUT_DIR / f"raw_profiles_{TS}"
RAW_DIR.mkdir(exist_ok=True)

def run_netsh(args):
    cmd = ["netsh"] + list(args)
    try:
        out = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="replace")
    except subprocess.CalledProcessError as e:
        out = e.output or ""
    return out

def get_profile_names():
    out = run_netsh(["wlan", "show", "profiles"])
    names = re.findall(r"All User Profile\s*:\s*(.+)", out, flags=re.IGNORECASE)
    seen = set(); unique = []
    for n in names:
        n = n.strip()
        if n and n not in seen:
            seen.add(n); unique.append(n)
    return unique

def get_profile_dump(profile_name):
    # Use quotes so spaces are handled; pass as separate arg to avoid shell parsing issues
    out = run_netsh(["wlan", "show", "profile", f'name="{profile_name}"', "key=clear"])
    return out

def extract_key_content(profile_dump):
    m = re.search(r"Key Content\s*:\s*(.+)", profile_dump, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""

def main():
    profiles = get_profile_names()
    if not profiles:
        print("No Wi‑Fi profiles found.")
        return

    rows = []
    for p in profiles:
        print("Processing:", p)
        dump = get_profile_dump(p)
        # save raw
        safe = re.sub(r'[^A-Za-z0-9_\- ]', '_', p)[:120]
        raw_file = RAW_DIR / f"profile_{safe}.txt"
        raw_file.write_text(dump, encoding="utf-8")
        # extract password
        pw = extract_key_content(dump)
        rows.append((p, pw))

    # write summary CSV-like file
    with SUMMARY_FILE.open("w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Profile", "Password"])
        for r in rows:
            writer.writerow(r)

    print(f"Saved summary to: {SUMMARY_FILE}")
    print(f"Raw outputs saved in: {RAW_DIR}")
    # Optionally print any found passwords to console (careful with shoulder-surfing)
    print("\nFound credentials:")
    for p, pw in rows:
        print(f"- {p} : {pw or '<no key displayed>'}")

if __name__ == "__main__":
    import re
    main()
