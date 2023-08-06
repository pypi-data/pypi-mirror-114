""" This script cleans text """
import argparse
import string

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk import download


download('wordnet')
download('stopwords')
download('punkt')


class TextNormalizer:
    
    def __init__(self, text: list):
        self.text = text
        
    def clean_text(self):
        self.text = TextNormalizer.make_lowercase(self.text)
        self.text = TextNormalizer.remove_punctuation(self.text)
        self.text = TextNormalizer.remove_numbers(self.text)
        self.text = TextNormalizer.remove_stopwords(self.text)
        
    @staticmethod
    def make_lowercase(sentence: str):
        """ Make the sentence lower case """
        return sentence.lower()
    
    @staticmethod
    def remove_punctuation(sentence: str):
        """ Remove punctuation from sentence """
        for punctuation in string.punctuation:
            sentence = sentence.replace(punctuation, '') 
        return sentence
    
    @staticmethod
    def remove_numbers(sentence: str):
        """ Remove numbers from sentence """
        return ''.join(word for word in sentence if not word.isdigit())
    
    @staticmethod
    def remove_stopwords(sentence: str):
        """ Remove stopwords """
        stop_words = set(stopwords.words('english')) 
        word_tokens = word_tokenize(sentence) 
        
        return [w for w in word_tokens if not w in stop_words] 


if __name__ == "__main__":
    description = 'clean_up_sentence'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--text',
                        help='test sentence',
                        required=True)
    args = parser.parse_args()

    text_normalizer = TextNormalizer(text=args.text)
    text_normalizer.clean_text()
    print(f"\nUpdated text:\n--> {text_normalizer.text}")