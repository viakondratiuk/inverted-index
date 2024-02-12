import random
import string
import time

from jellyfish import jaro_similarity


def generate_data(list_length: int, words_num: int) -> list[str]:
    data = [None] * list_length
    for i in range(list_length):
        data[i] = ' '.join(
            ''.join(random.choice("acdefghi") for _ in range(random.choice([3, 4, 5]))) for _ in
            range(words_num))
    return data


def create_ngrams(ngram_length: int, data: list[str]) -> list[list[(str, int)]]:
    ngram_list = []
    for line in data:
        ngrams = []
        for (w, word) in enumerate(line.split()):
            for i in range(len(word) - ngram_length + 1):
                ngrams.append((word[i:i + ngram_length], w))
        ngram_list.append(ngrams)
    return ngram_list


def create_inverted_index(ngram: list[list[(str, int)]]) -> dict[str, list[(int, int)]]:
    index = {}
    for (i, ngram_list) in enumerate(ngram):
        for (ngram, word) in ngram_list:
            if ngram in index:
                index[ngram].append((i, word))
            else:
                index[ngram] = [(i, word)]
    return index


def jaro_distance(s1: str, s2: str) -> float:
    return round(jaro_similarity(s1, s2), 2)


def bruteforce_compare(data: list[str], names: list[str]) -> list[list[(str, str, float)]]:
    results = []
    for data_str in data:
        data_words = data_str.split()  # Split the string into words
        for name_str in names:
            name_words = name_str.split()  # Split the string into words
            for d_word in data_words:
                for n_word in name_words:
                    distance = jaro_distance(d_word, n_word)
                    if distance > 0.5:
                        results.append((d_word, n_word, distance))
    return results

def inverted_index_compare(data: list[list[(str, int)]], names: list[list[(str, int)]], index: dict[str, list[(int, int)]]) -> list[list[(str, str, float)]]:
    results = []
    for (i, name_ngram) in enumerate(names):
        for (ngram, word) in name_ngram:
            if ngram in index:
                for (data_index, data_word) in index[ngram]:
                    distance = jaro_distance(data[data_index][1].split()[data_word], names[i][1].split()[word])
                    if distance > 0.5:
                        results.append((data[data_index][1].split()[data_word], names[i][1].split()[word], distance))
    return results


def benchmark_function(func, args, kwargs={}, iterations=10):
    total_time = 0
    for _ in range(iterations):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        total_time += (end_time - start_time)
    avg_time = total_time / iterations
    return avg_time


if __name__ == "__main__":    
    data = generate_data(3, 5) + ["hello world"]
    print("data:", data)
    print("=" * 10)
    data_ngram = create_ngrams(2, data)
    print("data_ngram:", data_ngram)
    print("=" * 10)
    names = generate_data(2, 2) + ["hello world"]
    print("names:", names)
    print("=" * 10)
    names_ngram = create_ngrams(2, names)
    print("names_ngram:", names_ngram)
    print("=" * 10)
    ii = create_inverted_index(data_ngram)
    print("ii:", ii)
    print("=" * 10)
    # bf_compare = bruteforce_compare(data, names)
    # print("bf_compare:", bf_compare)
    # print("=" * 10)
    # start_time = time.time()
    # average_execution_time = benchmark_function(bruteforce_compare, args=(data, names), iterations=100)
    # end_time = time.time()
    # print("total_execution_time:", end_time - start_time)
    # print("average_execution_time:", average_execution_time)
    inverted_result = inverted_index_compare(data_ngram, names_ngram, ii)
    print("inverted_result:", inverted_result)