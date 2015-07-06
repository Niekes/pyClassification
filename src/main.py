from os import listdir
import math

if __name__ == "__main__":
    stop_words = set()
    classes_word_count = {}
    vocabulary = {}
    cond_prob = {}
    data_path = "../data/"
    train_path = "/train"
    test_path = "/test"
    classes = ["sport", "politik", "wirtschaft"]
    docs_count = {"_total": 0}
    results = {}

    def init():
        init_stopwords()
        vocabulary["_all_words"] = set()
        for cls in classes:
            category = train_data(cls)
            classes_word_count[cls] = create_word_dict(category)
        do_condprob()

        for cls in classes:
            results[cls] = {}
            test_data(cls)

        print_dict(classes_word_count)

    def init_stopwords():
        s_words = open("../data/stop_words.txt")
        for word in s_words.readlines():
            word = word.strip()
            stop_words.add(word)
            stop_words.add(word.title())
            stop_words.add(word.upper())

    def test_data(cls):
        full_path = data_path + cls + test_path
        files = listdir(full_path)
        for each_file in files:
            data_set = open(full_path + "/" + each_file)
            text_list = []
            for each_paragraph in data_set.readlines():
                split_paragraph = [value for value in each_paragraph.split() if value != '']
                text_list += split_paragraph
            cleaned = clean_up_text(text_list)
            cleaned = remove_non_existent_in_voc(cleaned)
            doc_score = apply_multinomial_nb(cleaned)
            results[cls][each_file] = doc_score
        return results

    def remove_non_existent_in_voc(words):
        existent = []
        voc = vocabulary["_all_words"]
        for word in words:
            if word in voc:
                existent.append(word)
        return existent

    def apply_multinomial_nb(doc_voc):
        score = {}
        for cls in classes:
            prior = docs_count[cls] / docs_count["_total"]
            score[cls] = math.log2(prior)
            for token in doc_voc:
                if token in cond_prob:
                    score[cls] += math.log2(cond_prob[token][cls])
        return score

    def train_data(cls):
        full_path = data_path + cls + train_path
        files = listdir(full_path)
        nr_of_docs = len(files)
        docs_count[cls] = nr_of_docs
        docs_count["_total"] += nr_of_docs
        for each_file in files:
            data_set = open(full_path + "/" + each_file)
            text_list = []
            for each_paragraph in data_set.readlines():
                split_paragraph = [value for value in each_paragraph.split() if value != '']
                text_list += split_paragraph
            cleaned = clean_up_text(text_list)

            vocabulary[cls] = cleaned
            vocabulary["_all_words"] = vocabulary["_all_words"] | set(cleaned)

            data_set.close()
            return cleaned

    def clean_up_text(text):
        clean_text = []
        for each_word in text:
            symbols = "!@$%&*()_-+[]{}:\"<>?.,;/='"
            for s in range(0, len(symbols)):
                each_word = each_word.replace(symbols[s], "")
            if len(each_word) > 0 and each_word not in stop_words:
                clean_text.append(each_word)
        return clean_text

    def create_word_dict(clean_text):
        word_count = {}
        for each_word in clean_text:
            if each_word not in word_count:
                word_count[each_word] = 1
            else:
                word_count[each_word] += 1
        return word_count

    def print_dict(dict):
        print()
        for key in dict:
            print("###### " + key + " ######")
            print()
            for word in sorted(dict[key]):
                print("   " + word + ": " + str(dict[key][word]))
            print()

    def get_len_of_class(cls):
        count = 0
        category = classes_word_count[cls]
        for word in category:
            count += category[word]
        return count

    def do_condprob():
        for word in vocabulary["_all_words"]:
            cond_prob[word] = {}
            for cat in classes:
                cond_prob[word][cat] = calc_condprob(word, cat)
        return cond_prob

    def calc_condprob(word, cls):
        t_ct = classes_word_count[cls].get(word, 0)
        return (t_ct + 1) / (get_len_of_class(cls) + len(vocabulary["_all_words"]))

    init()