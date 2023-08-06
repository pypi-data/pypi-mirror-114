""" Unitests for quickfire/clean_text.py"""
from quickfire.clean_text import TextNormalizer

def test_lowercase():
    """ Test the sentence is all lowercase after transform """
    sentence = "My Name is India"
    assert TextNormalizer.make_lowercase(sentence) == "my name is india"
    
def test_remove_punctuation():
    """ Test removing all punctuation from sentence """
    sentence = "Hello! My name is India."
    assert TextNormalizer.remove_punctuation(sentence) == "Hello My name is India"

def test_remove_numbers():
    """ Test removing all numerics from sentence """
    sentence = "My number 1 is chocolate. My number is 0123."
    assert TextNormalizer.remove_numbers(sentence) == "My number  is chocolate. My number is ."

def test_remove_stopwords():
    """ Test removing stopwords from sentence """
    sentence = "Hello and nice to meet you this is India."
    assert TextNormalizer.remove_stopwords(sentence) == ['Hello', 'nice', 'meet', 'India', '.']
