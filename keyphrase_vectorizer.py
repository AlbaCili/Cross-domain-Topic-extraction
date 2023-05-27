from keybert import KeyBERT
import glob
import re
import nltk
import pandas as pd
from keyphrase_vectorizers import KeyphraseCountVectorizer
import numpy as np
from time import perf_counter
from collections import defaultdict


if __name__=="__main__":
    pass

#t1_start = perf_counter()# starting elapse time of code

path_files = 'Arts/clean_arts/*.txt'
txt_files = glob.glob(path_files)

kw_model = KeyBERT()

# it sorts files based on their numbers
txt_files.sort(key=lambda var:
[int(x) if x.isdigit()
 else x for x in re.findall(r'[^0-9]|[0-9]+',
                            var)])

cut_indeces = txt_files[:]

fnames_keys = {} # dictionary that contains the file names as key and keywords_dict as value
len_files = {}
#KeyBert_elapseTime = defaultdict(list)

range1 = 2
range2 = 2
part = 1
top = 5

for file in cut_indeces:
    with open(file, encoding='utf-8', mode='r') as f:
        read = f.readlines()
        length = len(nltk.word_tokenize(str(read)))

        index = file.rfind("clean")+6
        end = file.find(".txt")
        name = file[index:end]
        len_files[name] = length


        keywords_dict = {}# keywords as keys and percentage as values

        #NOTE: you could write a function which takes a string as argument and if the str == "keybert"
        # then the model will be selected for the keywords extraction
        # else str == "vectorizer" then vectorizer will extract the keywords

        #t2_start = perf_counter()# starting of model elapsed time


        # Using kephrase vectorizer
        keyphrase_vec = kw_model.extract_keywords(read, vectorizer=KeyphraseCountVectorizer())

        #t2_stop = perf_counter()# ending of model elapsed time
        #elapsed_time2 = t2_stop - t2_start # total second of  model elapsed time

        #KeyBert_elapseTime[name] = [t2_start,t2_stop, elapsed_time2]


        for li in keyphrase_vec:
            for key, percentage in li:
                keywords_dict[key]=percentage

        fnames_keys[name]= keywords_dict
#print(list(el3 for _,_,el3, in KeyBert_elapseTime.values()))


#t1_stop = perf_counter()# ending of code elapsed time

#elapsed_time1 = t1_stop - t1_start # total seconds of elapsed time


#
# print(t1_start,t1_stop)
# print(elapsed_time1)
# print(t2_start,t2_stop)
# print(elapsed_time2)


############################ Keyphrases Data Frame  ####################################################

dataFrame =  pd.DataFrame(fnames_keys)
df = dataFrame.rename_axis('Keyphrases')
datatoexcel = pd.ExcelWriter(f'Testing/keywords_and_keyphrase_extraction/arts_vec{top}Range'+
                             str(range1) + "_"  + str(range2)+ '.xlsx',
                             engine = "xlsxwriter")
df.to_excel(datatoexcel)
datatoexcel.save()


##############################Length of the texts ####################################################
