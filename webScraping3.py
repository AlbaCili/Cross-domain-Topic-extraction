from bs4 import BeautifulSoup
import glob
import re



if __name__=="__main__":
    pass


path_html = "Arts/Html_art/*.html"
html_files = glob.glob(path_html)

# it sorts files based on their numbers
html_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

cut_indeces = html_files[:]


for file in html_files:

    article = []
    id = "".join((re.findall('\d+', file)))

    with open(file) as f:

        soup = BeautifulSoup(f, 'html.parser')
        section = soup.find_all('section',attrs={'class':'article-section__content'})
        abstract = soup.find_all('div', attrs={'class': 'abstract-group'})
        date = soup.find_all('meta', attrs={'name':"citation_online_date"})[0]['content'].replace("/","-")

        for ab in abstract:
            ab_paragraph = ab.find("p") # finding the paragraph
            article.append(ab_paragraph.get_text())

        for element in section:

             if element != element.find("section", attrs={'class': 'article-section__inline-figure'}):
                 text = element.get_text()

                 if "CONFLICT OF INTEREST" in text:
                     pass

                 else: article.append(text)


        with open('Testing/webscraping/arts/art'+str(id)+"_"+date+'.txt','w') as fi:
             fi.writelines(" ".join(article))



















