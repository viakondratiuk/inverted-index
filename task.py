import random
import string
from jellyfish import jaro_similarity
import time


def generate_data(l, n):
    return [' '.join(''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6))) for _ in range(n)) for _ in
            range(l)]


def create_ngrams(n, data):
    ngrams_list = []
    for line in data:
        ngrams = []
        for word in line.split():
            for i in range(len(word) - n + 1):
                ngrams.append(word[i:i + n])
        ngrams_list.append(ngrams)
    return ngrams_list


def create_inverted_index(ngrams):
    index = {}
    for i, ngram_list in enumerate(ngrams, start=1):
        for ngram in ngram_list:
            if ngram not in index:
                index[ngram] = [i]
            else:
                index[ngram].append(i)
    return index


def bruteforce_compare(data, names):
    results = []
    for d in data:
        row = []
        for name in names:
            row.append(jaro_similarity(d, name))
        results.append(row)
    return results


def inverted_index_compare(data, names, n):
    data_ngrams = create_ngrams(n, data)
    names_ngrams = create_ngrams(n, names)
    index = create_inverted_index(data_ngrams)
    results = []

    for name_ngrams in names_ngrams:
        row = []
        for data_str in data:
            max_distance = 0
            for ngram in name_ngrams:
                if ngram in index:
                    for data_index in index[ngram]:
                        distance = jaro_similarity(data[data_index - 1], data_str)
                        max_distance = max(max_distance, distance)
            row.append(max_distance)
        results.append(row)
    return results


def benchmark_bruteforce(data, names):
    start_time = time.time()
    bruteforce_compare(data, names)
    end_time = time.time()
    return end_time - start_time


def benchmark_inverted_index(data, names, n):
    start_time = time.time()
    inverted_index_compare(data, names, n)
    end_time = time.time()
    return end_time - start_time


def run_benchmarks(l, n, names, ngram_length):
    data = generate_data(l, n)
    print(f"Data size: {len(data)} items")

    bf_time = benchmark_bruteforce(data, names)
    print(f"Bruteforce approach took {bf_time:.4f} seconds")

    ii_time = benchmark_inverted_index(data, names, ngram_length)
    print(f"Inverted index approach took {ii_time:.4f} seconds")


if __name__ == "__main__":
    l = 100
    n = 5
    names = ["example", "benchmark", "test"]
    ngram_length = 2

    # Run benchmarks
    run_benchmarks(l, n, names, ngram_length)