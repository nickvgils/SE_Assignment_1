import csv
import nltk

nltk.download('punkt')
nltk.download('stopwords')
# nltk.download()


class Requirements:
    def __init__(self):
        self.masterVocabulary = []
        self.highRequirements = self.getCSV("high")
        self.lowRequirements = self.getCSV("low")
        self.similarityMatrix = []

    def getCSV(self, requirement):
        requirements = []

        # Open csv file and loop through rows
        filename = "input/" + requirement + ".csv"

        with open(filename, "r") as inputfile:
            csv_dict_reader = csv.DictReader(inputfile)
            for row in csv_dict_reader:
                print(row['id'], row['text'])

                # Tokenization
                tokenizedSentence = nltk.word_tokenize(row['text'])

                # Stop-words removal and Stemming
                ps = nltk.PorterStemmer()
                filtered_words = [
                    ps.stem(word) for word in tokenizedSentence if word not in nltk.corpus.stopwords.words('english')]

                # Construct vocabulary of csv file
                self.masterVocabulary += filtered_words

                # Store the id and filtered_words in 'requirements' array
                requirements.append(
                    Requirement(row['id'], filtered_words))

        return requirements


class Requirement:
    def __init__(self, id, tokens):
        self.id = id
        self.tokens = tokens
        self.vectorRepr = []
