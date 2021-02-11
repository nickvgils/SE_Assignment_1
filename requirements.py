import csv
import nltk

nltk.download('punkt')
nltk.download('stopwords')
# nltk.download()


class Requirements:
    def __init__(self, path):
        self.requirements = []
        self.vocabulary = []
        self.getCSV(path)

    def getCSV(self, requirement):

        filename = "input/" + requirement + ".csv"

        with open(filename, "r") as inputfile:
            csv_dict_reader = csv.DictReader(inputfile)
            for row in csv_dict_reader:
                print(row['id'], row['text'])

                tokenizedSentence = nltk.word_tokenize(row['text'])

                ps = nltk.PorterStemmer()

                filtered_words = [
                    ps.stem(word) for word in tokenizedSentence if word not in nltk.corpus.stopwords.words('english')]

                self.vocabulary += filtered_words

                # row variable is a list that represents a row in csv
                self.requirements.append(
                    Requirement(row['id'], filtered_words))


class Requirement:
    def __init__(self, id, text):
        self.id = id
        self.text = text
