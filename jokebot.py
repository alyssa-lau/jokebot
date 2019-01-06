import time
import csv
import sys
import requests, json

def tell_joke(prompt, punchline):
    """ A function that delivers jokes """
    print(prompt)
    #wait 2 seconds
    time.sleep(2)
    print(punchline)

def read_input():
    """ A function that reads user input """
    user_input = input("Type 'next' to hear another joke or 'quit'.")
    if (user_input == 'next'):
        return True
    elif (user_input == 'quit'):
        return False
    else:
        print("I don't understand. Please input 'next' or 'quit'.")
        read_input()

def read_jokes(csv_file):
    """ A function that reads jokes from a CSV """
    with open(csv_file, 'rt') as f:
        reader = csv.reader(f)
        joke_list = list(reader)
    return joke_list

def get_reddit_jokes():
    """ a function that gets a list of Reddit posts from /r/dadjokes """
    r = requests.get('https://www.reddit.com/r/dadjokes.json', \
        headers = {'User-agent': 'your bot 0.1'})
    data = r.json()
    #individual posts stored as list of dictionaries
    unfiltered_posts = data['data']['children']

    #filtering out posts where over_18 is True to ensure safe for work
    safe_posts = list(filter(lambda d: d['data']["over_18"] == False, unfiltered_posts))
    #keeping only posts that begin with a question
    #also using lower() function to make my filtering case insensitive
    filtered_posts = list(filter(lambda d: \
        d['data']['title'].lower().startswith(('why', 'what', 'how')), safe_posts))
    reddit_jokes = [(p['data']["title"], p['data']["selftext"]) for p in filtered_posts]
    return reddit_jokes

#the following executes the code based on command line arguments
if __name__ == "__main__":
    try:
        #uses the csv if jokebot called with an argument
        input_csv = sys.argv[1]
        list_of_jokes = read_jokes(input_csv)
    except IndexError:
        #uses reddit as data source if jokebot called without arguments
        list_of_jokes = get_reddit_jokes()

for joke in list_of_jokes:
    tell_joke(joke[0], joke[1])
    if (read_input() == False):
        break
