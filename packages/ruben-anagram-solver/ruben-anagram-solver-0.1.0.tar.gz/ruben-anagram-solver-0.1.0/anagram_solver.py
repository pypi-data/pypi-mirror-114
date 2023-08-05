from collections import Counter, defaultdict
import re


def compute_letter_counts(s):
    return frozenset(Counter(re.sub(r"[^a-zA-Z0-9]", "", s.lower())).items())


with open("words.txt") as f:
    # Read list of English words from text file and split into a list
    # IIRC words.txt is from: https://github.com/dwyl/english-words
    words = f.read().splitlines()  # From: https://stackoverflow.com/a/3925701/3806231

    # Case is ignored by converting to lower case
    # Non-alphanumeric characters are ignored by removing them from the string
    # Idea is to convert each word to a representation that ignores order of the letters
    # This representation is a Counter which stores the number of occurrences of each letter in the word
    # Another alternative would be to sort the letters in each word
    # Create a list which contains each word along with this order-insensitive representation
    words_letters = [(word, compute_letter_counts(word)) for word in words]

    # Create a dictionary whose keys are the order-insensitive representation described above and whose values are the
    # set of words that correspond to that representation - e.g. key = {"a": 1, "b": 1, "t": 1}, value = {"bat", "tab"}
    # Using defaultdict so no need to handle the case where the key doesn't exist
    # Dictionary is a good idea if the program was extended to allow looking up more than one word, so that lookups are
    # more efficient
    letters_word_dict = defaultdict(set)
    for item in words_letters:
        letters_word_dict[item[1]].add(item[0])

    # Input a string from the user
    anagram = input("Enter string: ")

    # Convert this string to the order-insensitive representation and use this to lookup corresponding words in the
    # dictionary created above
    anagram_letters = compute_letter_counts(anagram)

    # Output the corresponding words
    print(sorted(letters_word_dict[anagram_letters]))
