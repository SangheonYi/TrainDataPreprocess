import random

def get_corpus_lines(corpus_path):
    with open(corpus_path, 'r', encoding='utf-8') as corpus_file:
        corpus_lines = corpus_file.readlines()
    return corpus_lines

def get_random_words(corpus_lines, k_size):
    random_words = set()
    population = range(len(corpus_lines) // 2)
    for remain in [0, 1]:
        for e in random.choices(population, k=k_size):
            corpus_line = corpus_lines[e * 2 + remain]
            random_words = random_words.union(corpus_line.split())
    return random_words

if __name__ == "__main__":
    count = 0
    corpus_lines = get_corpus_lines("../CorpusPreprocess/corpus/raw_text.txt")

    for k in range(50, 100):
        for i in range(1):
            count += len(get_random_words(corpus_lines, k))
        avg_count = count // 1
        print(f"{k}th avg: {avg_count}, data size with font: {avg_count * 7}")