import pandas as pd
import openpyxl
import numpy as np
import glob
import re
from nltk.text import Text
import nltk
from collections import defaultdict
from nltk.util import everygrams
import string
from nltk.corpus import stopwords
import os

if __name__=="__main__":
    pass

stripping = string.punctuation

length1 = 5
length2 = 5
part = 2

top = 10

pardir = os.path.dirname(__file__)

#print(pardir)

path_txt = os.path.join(pardir, "Arts/clean_arts/*.txt") # this function joins multiple paths
txt_files = glob.glob(path_txt)
# it sorts files based on their numbers
txt_files.sort(key=lambda var:[int(x) if x.isdigit()
                               else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

print(txt_files)

#excel_file = os.path.join(pardir, f"Anthropology/Anthropology_results/Top{top}/Part{part}/Anth_Top{top}_Range{length1}_{length2}.xlsx")

#Remember you have to check one file at a time.
excel_file = os.path.join(pardir, f"BusiPsy/BusiPsy_results/Top{top}/Part{part}/BusiPsy_Top{top}Range{length1}_{length2}.xlsx")

#excel_file = os.path.join(pardir, "BusiPsy_results/BusiPsy_vectorizer.xlsx")
excel_file = glob.glob(excel_file)
#excel_file.sort(key=lambda var:[int(x) if x.isdigit()
                                #else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
print(excel_file)

dictionary = {}

def excel_to_dict(excel_file_path, top):

    for excel in excel_file_path:

        new_list = []
        index = 0

        read = pd.read_excel(excel)
        headers = read.columns[1:].tolist() # retrieving the headers name  starting from
        keyphrases = read.iloc[:,0].tolist() # getting first column anf putting it into a list

        new_list = [keyphrases[x:x+top] for x in range(0, len(keyphrases),top)]

        if len(headers) == len(new_list):

            for top5_or_10 in new_list:

                dictionary[headers[index]] = top5_or_10 # can be either top 5 or top 10
                index +=1

        else: print("length does not correspond")

    return(dictionary)



def normilizing_file(file):

    tokens = nltk.word_tokenize(" ".join(file))
    lower = (word.lower() for word in tokens)
    strip = (w.strip(stripping) for w in lower)
    replace = (w for w in strip if w!= "")
    remove_stop = [w for w in replace if w not in stopwords.words('english')]

    return remove_stop


def getting_context(list, id):

    left = id-10
    right = id+10

# these conditions help to identify if the keyphrase id goes out of bounderies
# if that is the case it will try to "fix" the index and create non-empty list

    if left < 0:
        new_left = id-5
        #print(new_left)
        if new_left < 0:
            return list[id-3:right]
        else: return list[new_left:right]

    else: return list[left:right]
    #return list[id-10:id+10]


excel_dict = excel_to_dict(excel_file,top)


concordances = {} #### Make it a dictionary, it will be easier
print(excel_dict)

for file in txt_files:

    with open(file) as f:

        index = file.rfind("clean")+6
        end = file.find(".txt")
        name = file[index:end]

        cleaning = normilizing_file(f)
        every = set(everygrams(cleaning, min_len=length1, max_len=length2))
        ngram_dict = {}

        for i in range(length1, length2+1): # the range(2,2) function  will not count 2, but if we put  if we put a +1 it will count to 2
            ngram_dict[i] = nltk.ngrams(cleaning, i) # it will normalize it and divide by the length
        #print(ngram_dict.values())
        for key, val in dictionary.items():
            #print(key,val)
            for keyphrase in val:

                gram = tuple(keyphrase.split(" "))
                len_gram = len(gram)
                print(gram)
                if gram in every:

                    index = None
                    for i, candidate_gram in enumerate(ngram_dict[len_gram]):
                        if candidate_gram == gram:
                            index = i
                            break

                    if index is None:
                        #print(index)
                        continue

                    context = getting_context(cleaning, index)
                    #print(context)
                    concordances[key,name," ".join(gram)] = " ".join(context)





if len(concordances) == 0:
    pass

# The name of the file has to be referred  to the context taken from the .txt files
#The first domain name (e.g., Arts_...) refers to the domain context
#The section of the name "..._Top5_Part1_Range_2_2_CD_Business_Psychology.txt" refers to the
# Excel file of the business psychology domain of top 5 candidates of range (2,2).
# The part1 refers to the subdivision of the results obtained from keyword extraction, namely part 1
#and part 2
# if the excel files are divided in parts,
# remember to specify which part needs to be specified in the path
else:
    out_path = os.path.join(pardir, f'Testing/cross-domain/Arts_CD_Business_Psychology/Arts_context/Arts_'
    f'Top{top}'
    f'Part{part}'
    f'Range_{length1}_{length2}_CD_BusiPsy.txt')

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(os.path.join(pardir, f'Testing/cross-domain/Arts_CD_Business_Psychology/Arts_context/Arts_'
    f'Top{top}'
    f'Part{part}'
    f'Range_{length1}_{length2}_CD_BusiPsy.txt'), 'w') as txt:
        for key, value in concordances.items():
            txt.write('%s:%s\n' % (key, value))


print(concordances)












