import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillBoardScraper:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        pass

    def get_saturdays(self):
        self.start_date = datetime.date(2018, 9, 15)
        self.end_date = datetime.date(2023, 12, 20)

        current_date = self.start_date
        saturdays = []

        while current_date <= self.end_date:
            if current_date.weekday() == 5:
                saturdays.append(current_date.strftime('%Y-%m-%d'))
            current_date += datetime.timedelta(days=1)

        return saturdays
    
    def get_entries(self, date: str) -> list:
        """
        Returns a list of entries of *Billboard 100* for a given date.

        ### Args
            date (YYYY-MM-DD): The date to get entries for
        """
        self.driver.get(f"https://www.billboard.com/charts/hot-100/{date}")
        chart = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chart-results-list"))
        )
        records_title = self.driver.find_element_by_css_selector("h3.lrv-u-margin-r-150")
        records_title_excluding_first = chart.find_elements_by_css_selector("h3.u-max-width-330")
        records_artist = chart.find_elements_by_css_selector("span.u-max-width-330")
        entries = []
        for i in range(len(records_title_excluding_first) + 1):
            if i == 0:
                entries.append([i+1, records_title.text, records_artist[i].text])
            else: 
                entries.append([i+1, records_title_excluding_first[i-1].text, records_artist[i].text])

        return entries
            
    def save_entries(self, entries, date):
        """
        Saves entries to a csv file

        Args:
            entries (list): List of entries to save
            date (YYYY-MM-DD): Date of the entries
        """
        df = pd.DataFrame(entries, columns=['rank', 'title', 'artist'])
        df.to_csv(f"data/{date}.csv", index=False)
    
    def run(self):
        saturdays = self.get_saturdays()
        for saturday in saturdays:
            entries = self.get_entries(saturday)
            self.save_entries(entries, saturday)
        self.driver.quit()

if __name__ == "__main__":
    scraper = BillBoardScraper()
    scraper.run()
