from bs4 import BeautifulSoup
import re

#Formats input string to remove all unnecessary characters
def format(string):
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

	file = open(input_file_name)
	soup = BeautifulSoup(file, 'html.parser')
	siblings = soup.h3.find_next_siblings()
	#Separates html into groups of conversations by dividing at the headers
	for sibling in siblings:
		if "<h3>" in str(sibling):
			conversation_index += 1
			conversations.append([])
			continue
		else:
			conversations[conversation_index].append(format(str(sibling)))
	return conversations

#Prints to xml specification given conversations from input_file
def write_output(conversations,output_file_name):
	file = open(output_file_name, "w")
	file.write("<dialog>\n")
	for conversation in conversations:
		file.write("\t<conversation>\n")
		for person_utterance in conversation:
			person_utterance = str(person_utterance).split("|")
			if "<h3" in str(person_utterance) or "<a" in str(person_utterance) or len(person_utterance) < 2:
				print(person_utterance)
				continue
			person = person_utterance[0]
			utterance = person_utterance[1]
			file.write("\t\t<utt uid=" + person + ">" + utterance + "</utt>\n")
		file.write("\t</conversation>\n")
	file.write("</dialog>\n")



if __name__ == "__main__":
	input_file_name = "Friends_1_1.html";
	output_file_name = "output.xml"
	conversations = get_conversations(input_file_name)
	write_output(conversations,output_file_name)