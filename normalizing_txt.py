import nltk
import glob
import re


files = "Arts/Txt_arts/*.txt" #example path
txt_files = glob.glob(files)

txt_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
cut_indeces = txt_files[:]


for file in cut_indeces:
    index = file.rfind("/")+1
    name = file[index:]

    full_name = "clean_"+name
    cleaned =[]

    with open(file, encoding='utf-8', mode='r') as f:
        replace = " ".join(f).replace("\n","").replace("\xa0","")
        replace2 = " ".join(word.replace("*","")for word in nltk.word_tokenize(replace))

        with open('Testing/normalization/'+full_name,'w') as fi:  #example path
            fi.writelines(replace2)



