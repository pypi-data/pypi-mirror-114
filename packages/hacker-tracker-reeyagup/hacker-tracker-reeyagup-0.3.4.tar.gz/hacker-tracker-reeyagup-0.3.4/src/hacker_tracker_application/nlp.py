import nltk
import spacy
from nltk.corpus import wordnet
from spacytextblob.spacytextblob import SpacyTextBlob
import time
import platform
import os, glob, os.path, shutil, tempfile


nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

def get_polarity(text): #returs a number, if negative, then mood is sad, if positive

    doc = nlp(text)

    for span in doc.sents:

        #print(span.text, span._.polarity, span._.subjectivity)

        return span._.polarity


def nlp_func(text):
    pos_synonyms = []
    neu_synonyms = []
    neg_synonyms = []

    # NLP analysis of single-line text
    #doc = nlp(text) 
    
    doc = list(nlp.pipe([text]))
    emotional_words = dict()

    for word in doc: 
        #captures the emotional words
        for assessment in word._.assessments:
           tmp = assessment[0]
           polarity = assessment[1]
           for emotional_word in tmp:
               emotional_words[str(emotional_word)] = float(polarity)

    #[(word, polarity)]
    #print(emotional_words)

    for x in emotional_words:
        if x in emotional_words:
            if(emotional_words[x] > 0):
                    pos_synonyms.append(str(x))
                    for syn in wordnet.synsets(str(x)):
                        for lm in syn.lemmas():
                            #if lm.name()in pos_synonyms :
                            # adds the snonym(s) to the synonyms list
                            pos_synonyms.append(lm.name())
            elif(emotional_words[x] < 0):
                    neg_synonyms.append(str(x))
                    for syn in wordnet.synsets(str(x)):
                        for lm in syn.lemmas():
                            #if lm.name()in pos_synonyms :
                            # adds the snonym(s) to the synonyms list
                            neg_synonyms.append(lm.name())
                #returns the synonyms of the emotional word(s)
            elif(emotional_words[x] == 0):
                    neu_synonyms.append(str(x))
                    for syn in wordnet.synsets(str(x)):
                        for lm in syn.lemmas():
                            #if lm.name()in pos_synonyms :
                            # adds the snonym(s) to the synonyms list
                            neu_synonyms.append(lm.name())
                #returns the synonyms of the emotional word(s)
            
        
        # print("positive: ")           
        # print(set(pos_synonyms))
    
        # print("negative")
        # print(set(neg_synonyms))

        # print("neutral: ")           
        # print(set(neu_synonyms))

        NLP_Words = []
        NLP_Words.append(pos_synonyms)
        NLP_Words.append(neg_synonyms)
        NLP_Words.append(neu_synonyms)

        return NLP_Words

if __name__ == "__main__":
    
    #nlp_input = input("Enter nlp result: ")
    nlp_input = "I am forced into speech because men of science have refused to follow my advice without knowing why. It is altogether against my will that I tell my reasons for opposing this contemplated invasion of the antarctic - with its vast fossil hunt and its wholesale boring and melting of the ancient ice caps. And I am the more reluctant because my warning may be in vain. Doubt of the real facts, as I must reveal them, is inevitable; yet, if I suppressed what will seem extravagant and incredible, there would be nothing left. The hitherto withheld photographs, both ordinary and aerial, will count in my favor, for they are damnably vivid and graphic. Still, they will be doubted because of the great lengths to which clever fakery can be carried. The ink drawings, of course, will be jeered at as obvious impostures, notwithstanding a strangeness of technique which art experts ought to remark and puzzle over. In the end I must rely on the judgment and standing of the few scientific leaders who have, on the one hand, sufficient independence of thought to weigh my data on its own hideously convincing merits or in the light of certain primordial and highly baffling myth cycles; and on the other hand, sufficient influence to deter the exploring world in general from any rash and over-ambitious program in the region of those mountains of madness. It is an unfortunate fact that relatively obscure men like myself and my associates, connected only with a small university, have little chance of making an impression where matters of a wildly bizarre or highly controversial nature are concerned. It is further against us that we are not, in the strictest sense, specialists in the fields which came primarily to be concerned. As a geologist, my object in leading the Miskatonic University Expedition was wholly that of securing deep-level specimens of rock and soil from various parts of the antarctic continent, aided by the remarkable drill devised by Professor Frank H. Pabodie of our engineering department. I had no wish to be a pioneer in any other field than this, but I did hope that the use of this new mechanical appliance at different points along previously explored paths would bring to light materials of a sort hitherto unreached by the ordinary methods of collection. Pabodie’s drilling apparatus, as the public already knows from our reports, was unique and radical in its lightness, portability, and capacity to combine the ordinary artesian drill principle with the principle of the small circular rock drill in "

    start_time = time.time()
    print(nlp_func(nlp_input)) #old function
    print("")
    print("Perfomance Aspect:")
    print("polarity: " , get_polarity(nlp_input))
    end_time = time.time()
    cpu_time = time.thread_time()
    print("Time taken using nlp_func: ", cpu_time)



