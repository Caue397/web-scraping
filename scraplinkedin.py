import time
from dateutil.relativedelta import relativedelta
from _datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class scrap_linkedin:
    def __init__(self):
        self.url = 'https://www.linkedin.com/jobs/search?keywords=Servi%C3%A7os%20De%20Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&position=1&pageNum=0'
        self.option = Options()
        self.option.add_argument("-start-maximized")
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get(self.url)
        time.sleep(3)
        self.code_execution_time = f"{datetime.now().strftime('%d/%m/%Y')} {datetime.now().hour}:{datetime.now().minute}"
        self.element = self.driver.find_element("xpath", "//div[@class='base-serp-page']//div[@class='base-serp-page__content']")
        self.html_content = self.element.get_attribute('outerHTML')
        self.soup = BeautifulSoup(self.html_content, "html.parser")
        self.list_jobs = self.soup.find_all("div", attrs={"class": "base-card"})
        self.job_num = 1
        self.cont = 0
        self.jobs = []

    def dateFormat(self, stringDate):
        words = stringDate.split()
        num_date = int(words[1])
        date = datetime.now()
        for word in words:
            if "semanas" in word or "semana" in word:
                date = datetime.now() - timedelta(weeks=num_date)
            elif "mêses" in word or "mês" in word:
                date = datetime.now() - relativedelta(months=num_date)
            elif "horas" in word or "hora" in word:
                date = datetime.now() - timedelta(hours=num_date)
        return date.strftime("%d/%m/%Y")

    def scrap(self):
        try:
            while self.job_num <= len(self.list_jobs):
                    time.sleep(3)
                    self.element = self.driver.find_element("xpath", "//div[@class='base-serp-page']//div[@class='base-serp-page__content']")
                    self.html_content = self.element.get_attribute('outerHTML')
                    self.soup = BeautifulSoup(self.html_content, "html.parser")
                    self.list_jobs = self.soup.find_all("div", attrs={"class": "base-card"})
                    self.job_info = self.soup.find("section", attrs={"class": "two-pane-serp-page__detail-view"})
                    self.top_card = self.job_info.find("div", attrs={"class": "top-card-layout__card relative p-2 papabear:p-details-container-padding"})
                    self.extra_infos = self.top_card.find_all("div", attrs={"class": "topcard__flavor-row"})
                    self.job_details = self.soup.find("div", attrs={"class", "decorated-job-posting__details"})
                    self.job_url = self.list_jobs[self.cont].find("a", attrs={"class": "base-card__full-link"})
                    self.job_name = self.list_jobs[self.cont].find("h3").get_text().strip()
                    self.company_name = self.list_jobs[self.cont].find("h4").get_text().strip()
                    self.company_url = self.list_jobs[self.cont].find("a", attrs={"class", "hidden-nested-link"})
                    self.headquarter_location = self.list_jobs[self.cont].find("span", attrs={"class", "job-search-card__location"}).get_text().strip()
                    self.description_job = self.job_details.find("ul", attrs={"class": "description__job-criteria-list"})
                    self.contract_model = self.description_job.select("li")[1].select("span")[0].text.strip()
                    self.experience_level = self.description_job.select("li")[0].select("span")[0].text.strip()
                    self.string_job_date = self.extra_infos[1].find("span").get_text().strip()
                    self.job_date = self.dateFormat(self.string_job_date)
                    try:
                        self.num_candidates = self.extra_infos[1].find("figcaption").get_text().strip()
                    except:
                        self.num_candidates = self.extra_infos[1].find("span", attrs={"class", "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).get_text().strip()
                    self.job_num += 1
                    self.cont += 1
                    self.list_item = f'//ul[@class="jobs-search__results-list"]//li[{self.job_num}]'
                    self.driver.find_element("xpath", self.list_item).click()
                    self.jobs.append({"URL da vaga": self.job_url["href"],
                                 "Nome da vaga": self.job_name,
                                 "Nome da empresa": self.company_name,
                                 "URL da empresa": self.company_url["href"],
                                 "Modelo de contrato": self.contract_model,
                                 "Nivel de experiencia": self.experience_level,
                                 "Número de candidatos": self.num_candidates,
                                 "Local da sede": self.headquarter_location,
                                 "Data da postagem da vaga": self.job_date,
                                 "Horario da realizaçao do Scraping": self.code_execution_time
                                 })
        except:
            self.terminalFeedback()
            self.convertToCsv()

    def terminalFeedback(self):
        print('\033[32m' + 'Scraping realizado com sucesso!!' + '\033[0;0m')
        print(self.jobs)

    def convertToCsv(self):
        self.df = pd.DataFrame(self.jobs, columns=["URL da vaga", "Nome da vaga", "Nome da empresa", "URL da empresa", "Modelo de contrato", "Nivel de experiencia", "Número de candidatos", "Local da sede", "Data da postagem da vaga", "Horario da realizaçao do Scraping"])
        self.df.to_csv('scrap.csv', sep=';', index=False)

scraper = scrap_linkedin()
scraper.scrap()





