from bs4 import BeautifulSoup as Soup
from collections import Counter
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def analyse_file(filename):
    handler = open(filename).read()
    soup = Soup(handler,'lxml')

    ## analysis of characters and their turns
    characters_freq = []
    characters = []
    utterances = []
    id = 0
    for c in soup.dialog.find_all("conversation"):
        characters.append([])
        utterances.append([])
        for each_utt in c.find_all("utt"):
            characters[id].append(find_between(str(each_utt),'uid=','>'))
            utterances[id].append(find_between(str(each_utt),'>','<'))
        characters_freq.append(Counter(characters[id]))
        id +=1

    characters_freq_dialog = sum(characters_freq, Counter())
    unique_characters = list(characters_freq_dialog.keys())

    ## analysis of the utterance by various characters
    words_per_character_per_conversation = []
    for i in range(len(utterances)):
        words_per_character_per_conversation.append(Counter())
        for char in characters_freq[i].keys():
            charid = [id for id in range(len(characters[i])) if characters[i][id] == char]
            words = [len(utterances[i][id].split()) for id in charid]
            words_per_character_per_conversation[i][char] = sum(words)

    words_per_character_per_dialog = sum(words_per_character_per_conversation, Counter())
    no_of_words = sum(words_per_character_per_dialog.values())

    print("Names of characters:")
    print(unique_characters)

    print("\n Turns per characters per dialog:")
    print(characters_freq_dialog)

    print("\n Turns per characters per conversations(format[conversationID, turns]):")
    [print([i] + [characters_freq[i]]) for i in range(len(characters_freq))]

    print("\n number of words: ")
    print(no_of_words)

    print("\n Number of words per characters per dialog:")
    print(words_per_character_per_dialog)
    #
    print("\n number of words per character per conversation(format[conversationID, {character: words}])")
    [print([i] + [words_per_character_per_conversation[i]]) for i in range(len(words_per_character_per_conversation))]




    return [unique_characters, characters_freq_dialog, characters_freq, no_of_words, words_per_character_per_dialog, words_per_character_per_conversation]


if __name__ == "__main__":
    analyse_file("sample_output.xml")