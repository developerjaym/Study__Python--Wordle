
class WordList:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WordList, cls).__new__(cls)
            cls.instance.populate_word_list()
        return cls.instance
    def is_word(self, word):
        return word.lower() in self._word_list  
    def populate_word_list(self):
        with open('words.txt', encoding='utf-8') as text_file:
            self._word_list = set(text_file.read().split(","))
                  