from os import listdir

if __name__ == "__main__":
    categories_word_count = {}
    data_path = "../data/"
    train_path = "/train"
    categories = ["sport", "politik", "wirtschaft"]
    docs_count = {"_total": 0}

    def init():
        for cat in categories:
            category = parse_data(cat)
            categories_word_count[cat] = create_word_dict(category)
        print_dict(categories_word_count)
        print(docs_count)

    def parse_data(cat):
        full_path = data_path + cat + train_path
        files = listdir(full_path)
        nr_of_docs = len(files)
        docs_count[cat] = nr_of_docs
        docs_count["_total"] += nr_of_docs
        for each_file in files:
            data_set = open(full_path + "/" + each_file)
            text_list = []
            for each_paragraph in data_set.readlines():
                split_paragraph = [value for value in each_paragraph.split() if value != '']
                for each_word in split_paragraph:
                    text_list.append(each_word)
            cleaned = clean_up_text(text_list)
            data_set.close()
            return cleaned

    def clean_up_text(text):
        clean_text = []
        for each_word in text:
            symbols = "!@$%&*()_-+[]{}:\"<>?.,;/='"
            for s in range(0, len(symbols)):
                each_word = each_word.replace(symbols[s], "")
            if len(each_word) > 0:
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
            for word in dict[key]:
                print("   " + word + ": " + str(dict[key][word]))
            print()

    init()