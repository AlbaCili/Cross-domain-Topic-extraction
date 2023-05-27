from keybert import KeyBERT
import glob
import re
import nltk
import pandas as pd
from keyphrase_vectorizers import KeyphraseCountVectorizer
import numpy as np
from collections import defaultdict

path_files = 'Arts/clean_arts/*.txt' #path example
txt_files = glob.glob(path_files)

kw_model = KeyBERT()

# it sorts files based on their numbers
txt_files.sort(key=lambda var:
                        [int(x) if x.isdigit()
                         else x for x in re.findall(r'[^0-9]|[0-9]+',
                                                    var)])

cut_indeces = txt_files[:]# it used when the domain collection has more than 20 files 

fnames_keys = {} # dictionary that contains the file names as key and keywords_dict as value
len_files = {}

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
        
        keywords = kw_model.extract_keywords(read,
                                             keyphrase_ngram_range=(range1,range2),
                                             stop_words='english',
                                             top_n=top,
                                             use_mmr=True,
                                             diversity=0.8)

        for li in keywords:
            for key, percentage in li:
                keywords_dict[key]=percentage

        fnames_keys[name]= keywords_dict

############################ Keywords Data Frame  ####################################################

dataFrame =  pd.DataFrame(fnames_keys)
df = dataFrame.rename_axis('Keywords')
datatoexcel = pd.ExcelWriter(f'Testing/keywords_and_keyphrase_extraction/arts{top}Range'+.  
                             str(range1) + "_"  + str(range2)+ '.xlsx',
                             engine = "xlsxwriter") #example path
df.to_excel(datatoexcel)
datatoexcel.save()


##############################Length of the texts ####################################################

summing = sum(list(len_files.values()))

df_length = pd.DataFrame({'Files':len_files.keys(),
                           'Length':len_files.values()})

df_length = df_length.append({"Total length": summing},ignore_index = True)

df_length.index = np.arange(1,len(df_length)+1) # it starts from index 1
df_length = df_length.rename_axis('ID')

datatoexcel2 = pd.ExcelWriter('Testing/keywords_and_keyphrase_extraction/Arts_FilesLength.xlsx',
                              engine = "xlsxwriter")
df_length.to_excel(datatoexcel2)
datatoexcel2.save()
