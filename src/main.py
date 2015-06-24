import operator

if __name__ == "__main__":
    def init():
        dataSet = open( "../data/sport/train/s001.txt" );
        textArray = []
        for each_paragraph in dataSet.readlines():
            splited_paragraph = [value for value in each_paragraph.split() if value != '']
            for each_word in splited_paragraph:
                textArray.append(each_word)
        clean_up_text(textArray)
        dataSet.close()

    def clean_up_text(text):
        clean_text = []
        for each_word in text:
            symbols = "!@$%&*()_-+[]{}:\"<>?.,;/='"
            for s in range(0, len(symbols)):
                each_word = each_word.replace(symbols[s], "")
            if len(each_word) > 0:
                clean_text.append(each_word)
        create_word_dict(clean_text)

    def create_word_dict(clean_text):
        word_count = {}
        for each_word in clean_text:
            if each_word not in word_count:
                word_count[each_word] = 1
            else:
                word_count[each_word] += 1
        print(word_count)
    init()