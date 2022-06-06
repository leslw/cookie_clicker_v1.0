"""
This app run uses Selenium to play the classic version of Cookie Clicker for five minutes.
You can adjust the time interval between buying upgrade to try to achieve a higher cookie per second score.
"""

from cookie_clicker import CookieClicker

# Choose your power ups purchase interval
POWER_UP_CHECK_INTERVAL_IN_SECS = 30


def main():
    # initialize the CookieClicker object with the chosen interval
    cc = CookieClicker(interval=POWER_UP_CHECK_INTERVAL_IN_SECS)
    # Click the cookie for the set amount of time before purchasing upgrades
    cc.start()
    # Display the ending cookies per second
    print(cc.cookies_per_sec())
    # Close the browser
    cc.quit()
    # Check the high score
    high_score(cc.cps)


def high_score(cps):
    """Checks the current high score and displays results"""
    with open("score.txt", "r") as file:
        hs = float(file.read())

    if float(cps) > hs:
        with open("score.txt", "w") as file:
            file.write(cps)
        print("You have the new high score!")
    else:
        print(f"The current high score is: {cps} cookies per second")


if __name__ == "__main__":
    main()
