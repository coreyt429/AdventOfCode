import requests
import os
from getpass import getpass
import sys

SESSION_FILE = '.aoc.session'

def get_session_id():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_session_id(session_id):
    with open(SESSION_FILE, 'w') as f:
        f.write(session_id)

def login_to_aoc(session_id):
    session = requests.Session()
    session.cookies.set('session', session_id)
    return session

def test_session(session):
    response = session.get('https://adventofcode.com')
    return 'Advent of Code' in response.text

def get_input(session, year, day):
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve input. Status code: {response.status_code}")
        return None

def save_input(content, year, day):
    if not os.path.exists(f'{year}'):
        os.makedirs(f'{year}')
    with open(f'{year}/{day}/input.txt', 'w') as f:
        f.write(content)

def main():
    session_id = get_session_id()
    session = None

    while True:
        if session_id:
            session = login_to_aoc(session_id)
            if test_session(session):
                break
            else:
                print("Saved session ID is invalid.")
                session_id = None
        
        if not session_id:
            print("Please enter your Advent of Code session ID.")
            print("You can find this in your browser's cookies for adventofcode.com")
            session_id = getpass("Session ID: ")
            save_session_id(session_id)

    try:
        year = int(sys.argv[1])
        day = int(sys.argv[2])
    except IndexError as error_message:
        print("usage: python fetch_input.py {YEAR} {DAY}")
        sys.exit()
    except ValueError:
        print("usage: python fetch_input.py {YEAR} {DAY}")
        sys.exit()


    input_content = get_input(session, year, day)
    if input_content:
        save_input(input_content, year, day)
        print(f"Input for day {day} of year {year} has been saved.")

if __name__ == "__main__":
    main()