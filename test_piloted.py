from piloted import bruteforce_compare, benchmark_function
from piloted import create_ngrams, create_inverted_index, jaro_distance

def test_create_ngrams():
    data = ["hello world", "goodbye world"]
    ngrams = create_ngrams(2, data)
    assert len(ngrams) == len(data)
    assert all(isinstance(i, list) for i in ngrams)
    assert "he" in ngrams[0][0]

def test_create_inverted_index():
    data = ["hello world", "goodbye world"]
    ngrams = create_ngrams(2, data)
    index = create_inverted_index(ngrams)
    assert len(index) > 0
    assert all(isinstance(i, list) for i in index.values())
    assert "he" in index
    assert index["he"] == [(0, 0)]

def test_jaro_distance():
    assert jaro_distance("hello", "hello") == 1.0
    assert jaro_distance("hello", "hillo") == 0.87

def test_bruteforce_compare():
    data = ["hello world", "goodbye world"]
    names = ["hello", "world"]
    results = bruteforce_compare(data, names)
    assert len(results) > 0
    assert all(isinstance(i, tuple) and len(i) == 3 for i in results)

def test_benchmark_function():
    def dummy_func(x):
        return x * x

    avg_time = benchmark_function(dummy_func, args=(10,), iterations=100)
    assert isinstance(avg_time, float)