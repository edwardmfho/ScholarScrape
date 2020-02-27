# This script is to scrape article title and author names from Google Scholar. 

from selenium import webdriver
import time
import json


class ScholarBot():

    def __init__(self):
        self.driver  = webdriver.Chrome()


    def search(self):


        self.driver.get('https://scholar.google.com/scholar?hl=en&as_sdt=0,5&q=%222019-nCov%22&scisbd=1')
        time.sleep(5)

        page_counter = 1
        
        
        article = {}

        

        while True:
            time.sleep(5)
            try:
                next_btn = self.driver.find_element_by_xpath('//*[@id="gs_n"]/center/table/tbody/tr/td[12]/a/span')
                cur_paper_ls = self.driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_ri", " " ))]')
                print('Scraping page {}'.format(page_counter))
                for paper in cur_paper_ls:
                    title_temp = paper.find_element_by_css_selector('h3').text
                    author_temp = paper.find_element_by_css_selector('div.gs_a').text.encode('utf-8')
                    author_temp = unicode(author_temp, 'ascii', 'ignore')

                    article[title_temp] = [author_temp]

                print('Finish scrapping this page, attempt to scrap the next page')

                page_counter += 1
                next_btn.click()
            except:
                print("No more next page.")
                break
            
        f = open('article.json', 'r+')        
        d = ([{'title': k, 'author': v} for k,v in article.items()])
        json.dumps(d, f)
        f.close

    def output_web(self):
        with open('article.json') as handle:
            f = json.loads(handle.read())
            d = {"article":[{'title':key,"authors":value} for key,value in f.items()]}
            df = pd.DataFrame(d['article'])
            web = df.to_html()
            with open('article.html', 'w') as foo:
                foo.write(web)



if __name__ == '__main__':
    bot = ScholarBot()
    bot.search()
    bot.output_web()