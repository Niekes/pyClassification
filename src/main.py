from os import listdir
import math,re


class Classification():

    def __init__(self):
        self.stop_words = set()
        self.vocabulary = set()
        self.data_path = "../data/"
        self.train_path = "/train"
        self.test_path = "/test"
        self.classes = ["sport", "politik", "wirtschaft"]
        self.docs_count = {"_total": 0}
        self.cond_prob = {}  # conditional probabilities for all words and class combinations
        self.results = {}  # here we save the score for all words and class combinations when testing data
        self.class_len = {}  # save sizes of classes for better performance
        self.classes_word_count = {}


    def init(self):
        self.init_stopwords()

        for cls in self.classes:
            class_tokens = self.train_data(cls, {})
            self.classes_word_count[cls] = self.create_word_dict(class_tokens)
            self.class_len[cls] = self.get_len_of_class(cls)
            self.class_len["_all_words"] = len(self.vocabulary)
        self.do_condprob()

        for cls in self.classes:
            self.results[cls] = {}
            self.test_data(cls)

        self.print_results(self.results)
        #self.print_dict(self.classes_word_count)

    def init_stopwords(self):
        s_words = open("../data/stop_words.txt")
        for word in s_words.readlines():
            word = word.strip()
            self.stop_words.add(word)

    def train_data(self, cls, class_tokens):
        full_path = self.data_path + cls + self.train_path
        files = listdir(full_path)
        nr_of_docs = len(files)
        self.docs_count[cls] = nr_of_docs
        self.docs_count["_total"] += nr_of_docs
        class_tokens[cls] = []
        for each_file in files:
            text_list = self.file_to_list(full_path, each_file)
            cleaned = self.clean_up_text(text_list)

            class_tokens[cls] += cleaned  # add tokens of file to the class
            self.vocabulary = self.vocabulary | set(cleaned)  # same as vocabulary.union(cleaned)
        return class_tokens[cls]

    def file_to_list(self, path, file):
        data_set = open(path + "/" + file)
        text_list = []
        for line in data_set:
            split_paragraph = [value for value in line.split() if value != '']
            for token in split_paragraph:
                token = re.sub('\W', "", token)  # remove letters/numbers
                if len(token) > 0 and token not in self.stop_words:
                    text_list.append(token.lower())
        data_set.close()
        return text_list

    def test_data(self, cls):
        full_path = self.data_path + cls + self.test_path
        files = listdir(full_path)
        for each_file in files:
            text_list = self.file_to_list(full_path, each_file)
            cleaned = self.clean_up_text(text_list)
            cleaned = self.remove_non_existent_in_voc(cleaned)
            doc_score = self.apply_multinomial_nb(cleaned)
            self.results[cls][each_file] = doc_score

    def remove_non_existent_in_voc(self, words):
        existent = []
        for word in words:
            if word in self.vocabulary:
                existent.append(word)
        return existent

    def apply_multinomial_nb(self, doc_voc):
        score = {}
        for cls in self.classes:
            prior = self.docs_count[cls] / self.docs_count["_total"]
            score[cls] = math.log2(prior)
            for token in doc_voc:
                if token in self.cond_prob:
                    score[cls] += math.log2(self.cond_prob[token][cls])
        return score

    def clean_up_text(self, text):
        clean_text = []
        for each_word in text:
            if each_word not in self.stop_words:
                clean_text.append(each_word)
        return clean_text

    @staticmethod
    def create_word_dict(clean_text):
        word_count = {}
        for each_word in clean_text:
            if each_word not in word_count:
                word_count[each_word] = 1
            else:
                word_count[each_word] += 1
        return word_count

    def print_dict(self, dicto):
        print()
        for key in dicto:
            print("###### " + key + " ######")
            print()
            for word in sorted(dicto[key]):
                print("   " + word + ": " + str(dicto[key][word]))
            print()

    def get_len_of_class(self, cls):
        count = 0
        category = self.classes_word_count[cls]  # category meaning class here
        for word in category:
            count += category[word]
        return count

    def do_condprob(self):
        for word in self.vocabulary:
            self.cond_prob[word] = {}
            for cls in self.classes:
                self.cond_prob[word][cls] = self.calc_condprob(word, cls)

    def calc_condprob(self, word, cls):
        t_ct = self.classes_word_count[cls].get(word, 0)
        return (t_ct + 1) / (self.class_len[cls] + self.class_len["_all_words"])

    # get the class with highest score for word
    @staticmethod
    def get_winner(result):
        v = list(result.values())
        k = list(result.keys())
        return k[v.index(max(v))]

    def print_results(self, result):
        print()
        for key in result:
            print("###### " + key + " ######")
            print()
            for file in sorted(result[key]):
                print(file + ": " + self.get_winner(result[key][file]))
            print()


if __name__ == "__main__":
    classification = Classification()
    classification.init()

