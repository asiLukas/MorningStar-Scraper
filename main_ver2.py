
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from sys import exit


def connect(url):
    try:
        driver_options = Options()
        driver_options.add_argument('--headless')
        driver = webdriver.Chrome(options=driver_options)
        # driver = webdriver.Chrome()
        driver.get(url)

        return driver
    except:
        print('stara verze / nenainstalovany chrome driver')
        exit()

def get_ticker(token):
    if ',' in token:
        token = token.split(', ')
    else:
        token = token.split()

    return token

def get_data(start, file_url, ticker, price_earnings, price_book, price_sales, price_cash_flow, dividend_yield, peg_ratio, cash_return, revenue, operating_margin, roe, roi, current_ratio, debt_equity, R3, R2, R1, TTM, count):
    date_now = datetime.now().strftime("%Y/%m/%d")
    output_head = 'Ticker; date; P/E; P/B; P/S; P/CF; Div %; PEG; Cash return; Free CF/Revenue %; Operating Margin; ROE; ROI; Current Ratio; Debt/Equity; R-3; R-2; R-1; TTM\n'
    output = f'{ticker if not file_url else ticker[0][ticker[0].index("=")+1: ticker[0].index("&")]}; {date_now}; {price_earnings}; {price_book}; {price_sales}; {price_cash_flow}; {dividend_yield}; {peg_ratio}; {cash_return}; {revenue}; {operating_margin}; {roe}; {roi}; {current_ratio}; {debt_equity}; {R3}; {R2}; {R1}; {TTM}\n'

    if count == 0 and start: # remove previous lines and append the head
        print('\n\n----------------------------------------------------')
        print(output_head)
        print(output)
        with open('data/data' + '.txt', 'w') as f:
            f.write(output_head)
            f.write(output)

    else: # continue without head
        print(output)
        with open('data/data' + '.txt', 'a') as f:
            f.write(output)

    # print('----------------------------------------------------\n')

def get_links(path, filename):
    with open(path + filename, 'r') as f:
        links = f.readlines()
        for link in range(len(links)):
            links[link] = (links[link].replace('\n', ''), links[link].replace('\n', '').replace('ratios', 'valuation').replace('r.html', 'price-ratio.html'))

    # print(links)
    return links


def main(start):
    file_urls = False
    token = input('Zadej ticker nebo enter pro ukončení | nebo "a" pro načtení z data/adresy.txt: ')
    if token == '':
        exit()
    elif token == 'a' or token == 'A':
        tokens = get_links('data/', 'adresy.txt')
        file_urls = True
    else:
        tokens = get_ticker(token)

    for token in range(len(tokens)):
        try:
            if file_urls:
                url = tokens[token][1]
                # print(url)
            else:
                url = f'http://financials.morningstar.com/valuation/price-ratio.html?t={tokens[token]}&region=usa&culture=en-US'
            driver = connect(url)
            delay = 3
            price_earnings = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="currentValuationTable"]/tbody/tr[2]/td[1]'))).get_attribute('innerHTML').replace('.', ',')
            price_book = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="currentValuationTable"]/tbody/tr[4]/td[1]'))).get_attribute('innerHTML').replace('.', ',')
            price_sales = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="currentValuationTable"]/tbody/tr[6]/td[1]'))).get_attribute('innerHTML').replace('.', ',')
            price_cash_flow = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="currentValuationTable"]/tbody/tr[8]/td[1]'))).get_attribute('innerHTML').replace('.', ',')
            dividend_yield = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="currentValuationTable"]/tbody/tr[10]/td[1]'))).get_attribute('innerHTML').replace('.', ',')
            peg_ratio = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="forwardValuationTable"]/tbody/tr[4]/td[2]'))).get_attribute('innerHTML').replace('.', ',')
            cash_return = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yeldChart"]/div/div[7]'))).get_attribute('innerHTML').replace('.', ',')

            if file_urls:
                url = tokens[token][0]
            else:
                url = f'http://financials.morningstar.com/ratios/r.html?t={tokens[token]}&region=usa&culture=en-US'
            driver.get(url)

            revenue = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-cashflow"]/table/tbody/tr[8]/td[11]'))).get_attribute('innerHTML').replace('.', ',')
            operating_margin = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="financials"]/table/tbody/tr[8]/td[11]'))).get_attribute('innerHTML').replace('.', ',')
            roe = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-profitability"]/table[2]/tbody/tr[12]/td[11]'))).get_attribute('innerHTML').replace('.', ',')
            roi = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-profitability"]/table[2]/tbody/tr[14]/td[11]'))).get_attribute('innerHTML').replace('.', ',')

            current_ratio = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-financial"]/table[2]/tbody/tr[2]/td[11]'))).get_attribute('innerHTML').replace('.', ',')
            debt_equity = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-financial"]/table[2]/tbody/tr[8]/td[11]'))).get_attribute('innerHTML').replace('.', ',')
            R3 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="financials"]/table/tbody/tr[10]/td[8]'))).get_attribute('innerHTML').replace('.', ',')
            R2 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="financials"]/table/tbody/tr[10]/td[9]'))).get_attribute('innerHTML').replace('.', ',')
            R1 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="financials"]/table/tbody/tr[10]/td[10]'))).get_attribute('innerHTML').replace('.', ',')
            TTM = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="financials"]/table/tbody/tr[10]/td[11]'))).get_attribute('innerHTML').replace('.', ',')
        except TimeoutException:
            print('hlupa stranka, nekdy nacte nekdy nenacte \n--------------------------------------------------')
            exit()

        get_data(start, file_urls, tokens[token], price_earnings, price_book, price_sales, price_cash_flow, dividend_yield, peg_ratio, cash_return, revenue, operating_margin, roe, roi, current_ratio, debt_equity, R3, R2, R1, TTM, token)

    main(False)

main(True)
