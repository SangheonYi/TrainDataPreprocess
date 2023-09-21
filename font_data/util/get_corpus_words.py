def get_corpus_words(corpus_path):
    corpus_words = dict(
        kor=[],
        eng=[]
    )
    with open(corpus_path, 'r', encoding='utf-8') as corpus_file:
        for line_idx, line in enumerate(corpus_file):
            lang = 'kor' if line_idx % 2 == 0 else 'eng'
            corpus_words[lang] += line[:-1].split()
            max_words = 2000000
            if len(corpus_words['kor']) > max_words and len(corpus_words['eng']) > max_words:
                break
    return corpus_words

def get_valid_n_pair(corpus_word_list:list, n:int, support_char_set:set):
    valid_words = []
    half_n = n / 2
    for corpus_word in corpus_word_list:
        if len(valid_words) < half_n and set(corpus_word).issubset(support_char_set):
            valid_words.append(corpus_word)    
    return valid_words

if __name__ == "__main__":
    count = 0
    corpus_words = get_corpus_words("../../CorpusPreprocess/corpus/raw_text.txt")
    support_set = set(['한', '의료단체는', '연방법원에', '보건부', '지침', '취소를', '요구하는', '소송을', '제기하기도', '했다.'])
    support_set |= set(['A', 'medical', 'group', 'has', 'even', 'filed', 'a', 'federal', 'court', 'lawsuit'])
    print(support_set)
    for k, v in corpus_words.items():
        print(get_valid_n_pair(v, 3, support_set))
        print(k, v[:1])