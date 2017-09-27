from bs4 import BeautifulSoup
import re



# num of episodes in each season
seasons = [
    1,
    24,
    25,
    24,
    24,
    25,
    24,
    24,
    24,
    18
]



#Formats input string to remove all unnecessary characters
def custom_format(string):
	#removes text between brackets
	string = re.sub('\[.*?\]\s?', "", string, 0, re.DOTALL)
	#replaces <b><b> with <b> and </b></b> with </b>
	string = re.sub('<b><b>',"<b>",string)
	string = re.sub('</b></b>',"</b>",string)
	#replaces <b> with "" and </b> with | for later splitting
	string = re.sub('<b>\s?',"",string)
	string = re.sub('</b>\s?',r"|",string)

	#Removes puncation, newlines, loose tags, other various things
	string = re.sub('</?[ip]>|\s?\n\s?|[.?!,-]|\s?:|', "", string)
	string = string.replace(u'\xa0',"")
	string = string.replace("»","")
	string = string.replace("«","")
	return string.strip()

#Gets nicely formatted conversations from the given input file
def get_conversations(input_file_name):
	conversations = [[]]
	utterances = []
	conversation_index = 0

	file = open(input_file_name, 'r')
	soup = BeautifulSoup(file, 'html5lib')
	siblings = soup.h3.find_next_siblings()
	#Separates html into groups of conversations by dividing at the headers
	for sibling in siblings:
		if "<h3" in str(sibling):
			conversation_index += 1
			conversations.append([])
			continue
		else:
			conversations[conversation_index].append(custom_format(str(sibling)))
	return conversations

#Prints to xml specification given conversations from input_file
def write_output(conversations,output_file_name):
	file = open(output_file_name, "a")
	for conversation in conversations:
		conversation = list(filter(lambda x: "<h3" not in x and "<a" not in x and len(x)>=2, conversation))
		if not len(conversation):
			continue
		file.write("\t<s>\n")
		person_uid = dict()
		p_index = 0
		for person_utterance in conversation:
			person_utterance = str(person_utterance).split("|")
			if "<h3" in str(person_utterance) or "<a" in str(person_utterance) or len(person_utterance) < 2:
				continue
			person = person_utterance[0]
			utterance = person_utterance[1]
			if person in person_uid:
				person = person_uid[person]
			else:
				person_uid[person] = p_index
				p_index += 1
				person = person_uid[person]
			file.write("\t\t<utt uid=\"" + str(person) + "\">" + utterance + "</utt>\n")
		file.write("\t</s>\n")
	
if __name__ == "__main__":
	output_file_name = "output.xml"
	file = open(output_file_name, "w")
	file.write("<dialog>\n")
	file.close()
	for season in range(len(seasons)):
		for episode in range(seasons[season]):
			input_file_name = 'raw_scripts/friends_{}_{}.htm'.format(season+1,episode+1)
			conversations = get_conversations(input_file_name)
			write_output(conversations,output_file_name)
	file = open(output_file_name, "a")
	file.write("</dialog>\n")
	file.close()