from bs4 import BeautifulSoup
import glob
import re
from collections import defaultdict
from pandas import pandas as pd
import numpy as np


path_html = "Arts/Html_art/*.html" #example directory
html_files = glob.glob(path_html)

# it sorts files based on their numbers
html_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

def keywords_length(list) -> list :

    new_list = []

    if list==[]:
        new_list.append("The author/s did not provide this information.")

    else:
        for key in list:
            new_list.append(key)

    return new_list


nameFile_metadata = defaultdict(dict)

for file in html_files:

    metadata = []
    id = "".join((re.findall('\d+', file)))


    with open(file) as f:

        file_metadata = defaultdict(list)


        soup = BeautifulSoup(f, 'html.parser')
        title = soup.find_all('meta', attrs={'property':"og:title"})[0]['content']
        journal_title = soup.find_all('meta', attrs={'name':"citation_journal_title"})[0]['content']
        type = soup.find_all('meta', attrs={'property':"og:type"})[0]['content']
        url = soup.find_all('meta', attrs={'property':"og:url"})[0]['content']
        website = soup.find_all('meta', attrs={'property':"og:url"})[0]['content']

        keywords = [key.get('content')for key in soup.find_all('meta', attrs={'name':"citation_keywords"})]
        keywords2 = keywords_length(keywords)

        author = [key.get('content')for key in soup.find_all('meta', attrs={'name':"citation_author"})]
        institution = set([key.get('content') for key in soup.find_all('meta', attrs={'name':"citation_author_institution"})])
        date = soup.find_all('meta', attrs={'name':"citation_online_date"})[0]['content'].replace("/","-")
        full_text = soup.find_all('meta', attrs={'name':"citation_fulltext_html_url"})[0]['content']
        doi = soup.find_all('meta', attrs={'name':"citation_doi"})[0]['content']

        name_file = "art"+str(id)+"_"+date #the name abbreviation can change based on the domain this is an example

        file_metadata['Title'] = title
        file_metadata['Journal Title']= journal_title
        file_metadata["Author/s"] = ", ".join(author)
        file_metadata["Institution"] = ", ".join(institution)
        file_metadata["Date"] = date
        file_metadata['Type'] = type
        file_metadata['Keywords'] = ", ".join(keywords2)
        file_metadata["Citation full text"] = full_text
        file_metadata["Url"]= url
        file_metadata["Website"] = website
        file_metadata["Doi"] = doi

        nameFile_metadata[name_file] = file_metadata


## try to find a way to put the multiple values on a new line

df_meta = pd.DataFrame.from_dict(nameFile_metadata,orient='index')
df_meta.index = np.arange(1,len(df_meta)+1) # it starts from index 1
df_meta = df_meta.rename_axis('ID')
df_meta.insert(0, "Files", nameFile_metadata.keys())

datatoexcel = pd.ExcelWriter('Testing/webscraping/arts/metadata/Metadata_arts.xlsx', engine = "xlsxwriter")
df_meta.to_excel(datatoexcel)
datatoexcel.save()
