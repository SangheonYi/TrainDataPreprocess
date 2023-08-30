import random

def get_corpus_words(corpus_path):
    corpus_words = set()
    with open(corpus_path, 'r', encoding='utf-8') as corpus_file:
        for line in corpus_file.readlines():
            corpus_words.update(line[:-1].split())
    return corpus_words

def get_random_words(corpus_words, k_size):
    random_words = set()
    population = range(len(corpus_words))
    for e in random.choices(population, k=k_size):
        random_words.add(corpus_words[e])
    return random_words

if __name__ == "__main__":
    count = 0
    corpus_lines = get_corpus_words("../CorpusPreprocess/corpus/raw_text.txt")

    for k in range(50, 100):
        for i in range(1):
            count += len(get_random_words(corpus_lines, k))
        avg_count = count // 1
        print(f"{k}th avg: {avg_count}, data size with font: {avg_count * 7}")