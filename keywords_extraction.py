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
        keywords = kw_model.extract_keywords(read,
                                             keyphrase_ngram_range=(range1,range2),
                                             stop_words='english',
                                             top_n=top,
                                             use_mmr=True,
                                             diversity=0.8)

        # Using kephrase vectorizer
        #keywords_vec = kw_model.extract_keywords(read, vectorizer=KeyphraseCountVectorizer())

        #t2_stop = perf_counter()# ending of model elapsed time
        #elapsed_time2 = t2_stop - t2_start # total second of  model elapsed time

        #KeyBert_elapseTime[name] = [t2_start,t2_stop, elapsed_time2]


        for li in keywords:
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
df = dataFrame.rename_axis('Keywords')
datatoexcel = pd.ExcelWriter(f'Testing/keywords_and_keyphrase_extraction/arts{top}Range'+
                             str(range1) + "_"  + str(range2)+ '.xlsx',
                             engine = "xlsxwriter")
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

########################## Elapse time of model and code ###################################################
#
# DFelapse_time1 = pd.DataFrame({"Text": KeyBert_elapseTime.keys(),
#                             "KeyBert start elapsed time":list(el1 for el1,_,_, in KeyBert_elapseTime.values()),
#                             "KeyBert end elapsed time": list(el2 for _,el2,_, in KeyBert_elapseTime.values()),
#                             "Total seconds of model elapsed time": list(el3 for _,_,el3, in KeyBert_elapseTime.values())
#                             })
#
#
# DFelapse_time1 = DFelapse_time1.append({ "Code start elapsed time":t1_start,
#                               "Code end elapsed time":t1_stop,
#                               "Total seconds of code elapsed time": elapsed_time1},
#                              ignore_index = True)
#
#
# DFelapse_time1.index = np.arange(1,len(DFelapse_time1)+1) # it starts from index 1
# DFelapse_time1 = DFelapse_time1.rename_axis('ID')
#
# neworder = ['Text','KeyBert start elapsed time',
#             'KeyBert end elapsed time',
#             'Total seconds of model elapsed time',
#             'Code start elapsed time',
#             'Code end elapsed time',
#             'Total seconds of code elapsed time']
#
# DFelapse_time1 = DFelapse_time1.reindex(columns=neworder)
#
#
# datatoexcel3 = pd.ExcelWriter('BusiPsy/BusiPsy_results/Top10/Part2/Time/BusiPsy_ET_Top10Range'
#                               + str(range1) + "_"  + str(range2)+'.xlsx',
#                               engine = "xlsxwriter")
#
# DFelapse_time1.to_excel(datatoexcel3)
# datatoexcel3.save()


##############################################################################################################























#
# DFelapse_time1 = DFelapse_time1.drop_duplicates(subset = ["Code start elapsed time",
#                                          "Code end elapsed time",
#                                          "Total seconds of code elapsed time"],
#                                keep = 'first')










# DFelapse_time2 = pd.DataFrame({"Code start elapsed time": t1_start,
#                                "Code end elapsed time":t1_stop,
#                                "Total seconds of code elapsed time": elapsed_time1})






#
# DFelapse_time1.insert(4,"Code start elapsed time", t1_start )
# DFelapse_time1.insert(5,"Code end elapsed time", t1_stop )
# DFelapse_time1.insert(6, "Total seconds of code elapsed time",elapsed_time1)




#
#
#  #gephi_nodes[key,percentage] = name # data for node table
#                 #gephi_edges[key,percentage] = [name,'directed']
#
# nodes = pd.DataFrame({'Names': gephi_nodes.values(),
#                       'Key phrase': [k for k,per in gephi_nodes.keys()],
#                       'Percentage': [per for k,per in gephi_nodes.keys()]})
#
# nodes.index = np.arange((1,len(nodes)+1))
# nodes = nodes.rename_axis('ID')
#
# nodes_toCsv = nodes.to_csv('test_csv/Part1/antr_nodes.csv', encoding= 'utf-8')
#
# edges = pd.DataFrame({'Source': [n_file for n_file,_ in gephi_edges.values()],
#                       'Target':[k for k,per in gephi_nodes.keys()],
#                       'Type': [dir for _,dir in gephi_edges.values()],
#                       'Weight':[per for k,per in gephi_nodes.keys()]})
#
# edges_toCsv = edges.to_csv('test_csv/Part1/antr_edges.csv', encoding= 'utf-8')