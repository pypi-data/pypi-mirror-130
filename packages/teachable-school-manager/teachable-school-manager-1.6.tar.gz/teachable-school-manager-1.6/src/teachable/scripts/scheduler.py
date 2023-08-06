import schedule
import time
import subprocess


def remind():
    # process to remind users and course managers
    subprocess.run(["teachable_remind"])
    return


def statements():
    # process to fetch statements from teachable
    subprocess.run(["teachable_statements", "-e"])
    return

def auto_unenroll():
    # process to auto unenroll people that have been enrolled for a year
    subprocess.run(['teachable_unenroll', '-d 365'])
    return


def main():
    schedule.every().saturday.at("13:15").do(remind)
    schedule.every().saturday.at("13:15").do(statements)
    schedule.every(4).weeks.do(auto_unenroll)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
