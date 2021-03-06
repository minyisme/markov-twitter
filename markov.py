from random import choice
import sys
import os
import twitter

def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file_text = open(file_path).read()

    file_text = file_text.replace("\n"," ").rstrip()

    return file_text


def make_chains(text_string, n_gram_length):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    # your code goes here
    text_list = text_string.split()
    text_key = []
    # Iterates through the list of words to create lists of n_gram_length
    for x in range(len(text_list) - n_gram_length + 1):
        for i in range(n_gram_length):
            text_key.append(text_list[x + i])
        # Convert list to tuple to use as a dictionary key in chains
        text_key = tuple(text_key)
        # If statement handles 1st entry of key-value and subsequent
        if text_key not in chains:
            try:
                chains[text_key] = [text_list[x + n_gram_length]]
            except IndexError:
                chains[text_key] = [None]
        else:
            try:
                chains[text_key].append(text_list[x + n_gram_length])
            except IndexError:
                chains[text_key].append(None)
        text_key = []

    return chains


def make_text(chains, n_gram_length):
    """Takes dictionary of markov chains; returns random text."""

    text = ""

    #Initializing words_list with random tuple, making sure key starts with a capital
    while True:
        words_list = list(choice(chains.keys()))
        first_word = words_list[0]
        if first_word[0].isupper():
            break

    # Establishes words_list_characters to hold the count of characters in words_list.
    words_list_characters = 0
    for word in words_list:
        words_list_characters += len(word) + 1 # Plus one for space added later.
    # While loop creates key from last n items in word_list,
    # picks a random word from possible values,
    # appends word to word_list, and
    # repeats until either the None item is added or
    # word list is greater than length specified.
    while (words_list[-1] != None):
        # Initialize empty list for key creation
        list_to_look_up = []
        # Iterating through our last n items of word list from left to right
        # Adding last n items to our key list
        for i in range(n_gram_length, 0, -1):
            list_to_look_up.append(words_list[-i])
        # Turning our key list into a tuple
        tuple_to_look_up = tuple(list_to_look_up)
        # Getting the value -a list- for our key
        a_list_of_words = chains[tuple_to_look_up]
        # Getting the random new word to add from the value list
        new_word = choice(a_list_of_words)
        # Adds character count to words_list_characters plus one for the space added later.
        words_list_characters += len(new_word) + 1
        if words_list_characters >= 140:
            break
        # Appending the random new word to our words list
        words_list.append(new_word)

    # Removing the final None item from our list.
    if words_list[-1] == None:
        words_list = words_list[:-1]

    # # While loop deletes the last word from words_list until it 
    # # finds a final word that ends in a punctuation mark.
    while True:
        test_word = words_list[-1]
        if test_word[-1].isalnum():
            del words_list[-1]
        else:
            break

    # Joins words_list as string called text
    text = " ".join(words_list)

    return text


def tweet(status_update):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    # print api.VerifyCredentials()

    api.PostUpdate(status_update)
    # print status.text

    pass


def loop_text(chains, n_gram_length):
    while True:
        possible_tweet = make_text(chains, n_gram_length)
        print possible_tweet
        print "*Press 'y' to post this tweet."
        print "*Press 'n' to try another tweet."
        print "*Press 'q' to quit without posting."

        decision = raw_input("What would you like to do? ").lower()

        if decision == 'q':
            break
        elif decision == 'y':
            tweet(possible_tweet)
            print "Great, your tweet has been posted."
            print
            print
            print "Here's another possible tweet:"
            continue
        elif decision == 'n':
            print
            print
            print "Here's another possible tweet:"
            continue


input_path = sys.argv[1]
input_path2 = sys.argv[2]
n_gram_length = int(sys.argv[3])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)
input_text2 = open_and_read_file(input_path2)
input_text = input_text + " " + input_text2

# Get a Markov chain
chains = make_chains(input_text, n_gram_length)

# Produce random text
loop_text(chains, n_gram_length)

