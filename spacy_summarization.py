import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from heapq import nlargest

# stopwords = list(STOP_WORDS)

nlp = spacy.load('en')

def text_summarizer(document):
    stopwords = list(STOP_WORDS)
    docx = nlp(document)

    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    # Sentence Tokens
    sentence_list = [sentence for sentence in docx.sents]

    [w.text.lower() for t in sentence_list for w in t]

    # Sentence Score via comparrng each word with sentence
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    # print(sentence_scores)

    ### Find Top N sentences with Largest score

    summarized_sentences = nlargest(1, sentence_scores, key=sentence_scores.get)

    # print(summarized_sentences)

    final_sentences = [w.text for w in summarized_sentences]

    summary = ' '.join(final_sentences)

    return summary
    
    


