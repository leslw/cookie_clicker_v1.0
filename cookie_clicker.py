"""
This app run uses Selenium to play the classic version of Cookie Clicker for five minutes.
You can adjust the time interval between buying upgrade to try to achieve a higher cookie per second score.
"""

from cookie_clicker import CookieClicker

# Choose your power ups purchase interval
POWER_UP_CHECK_INTERVAL_IN_SECS = 30


def main():
    # Instantiate the CookieClicker object with the specified power-up check interval
    cc = CookieClicker(interval=POWER_UP_CHECK_INTERVAL_IN_SECS)
    # Start the game and perform actions
    cc.start()
    # Retrieve the cookies per second value
    cps = cc.get_cookies_per_sec()
    print(f"Cookies Per Second: {cps}")
    # Close the browser
    cc.quit()
    # Check and display the high score
    check_high_score(cps)


def check_high_score(cps):
    # Check the current high score and update if necessary
    high_score = 0.0
    try:
        with open("score.txt", "r") as file:
            high_score = float(file.read())
    except FileNotFoundError:
        pass

    if cps > high_score:
        with open("score.txt", "w") as file:
            file.write(str(cps))
        print("Congratulations! You have a new high score!")
    else:
        print(f"The current high score is: {high_score} cookies per second")


if __name__ == "__main__":
    main()
