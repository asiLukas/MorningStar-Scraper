from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from sys import exit
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(800, 800))
# display.start()

def main():
    token = input('Zadej společnost(AAPL, GE, TSLA...) nebo enter pro ukončení: ')
    if token == '':
        exit()
    url = f'http://financials.morningstar.com/valuation/price-ratio.html?t={token}&region=usa&culture=en-US'

    try:
        driver_options = Options()
        driver_options.add_argument('--headless')
        driver = webdriver.Chrome(options=driver_options)
        # driver = webdriver.Chrome()
        driver.get(url)
        sleep(3)
    except:
        print('STARA VERZE GOOGLE DRIVERU')
        exit()


    price_earnings = driver.find_element_by_xpath('//*[@id="currentValuationTable"]/tbody/tr[2]/td[1]').get_attribute('innerHTML').replace('.', ',')
    price_book = driver.find_element_by_xpath('//*[@id="currentValuationTable"]/tbody/tr[4]/td[1]').get_attribute('innerHTML').replace('.', ',')
    price_sales = driver.find_element_by_xpath('//*[@id="currentValuationTable"]/tbody/tr[6]/td[1]').get_attribute('innerHTML').replace('.', ',')
    price_cash_flow = driver.find_element_by_xpath('//*[@id="currentValuationTable"]/tbody/tr[8]/td[1]').get_attribute('innerHTML').replace('.', ',')
    dividend_yield = driver.find_element_by_xpath('//*[@id="currentValuationTable"]/tbody/tr[10]/td[1]').get_attribute('innerHTML').replace('.', ',')
    peg_ratio = driver.find_element_by_xpath('//*[@id="forwardValuationTable"]/tbody/tr[4]/td[2]').get_attribute('innerHTML').replace('.', ',')
    cash_return = driver.find_element_by_xpath('//*[@id="yeldChart"]/div/div[7]').get_attribute('innerHTML').replace('.', ',')

    url = f'http://financials.morningstar.com/ratios/r.html?t={token}&region=usa&culture=en-US'
    driver.get(url)
    sleep(3)

    revenue = driver.find_element_by_xpath('//*[@id="tab-cashflow"]/table/tbody/tr[8]/td[11]').get_attribute('innerHTML').replace('.', ',')
    operating_margin = driver.find_element_by_xpath('//*[@id="financials"]/table/tbody/tr[8]/td[11]').get_attribute('innerHTML').replace('.', ',')
    roe = driver.find_element_by_xpath('//*[@id="tab-profitability"]/table[2]/tbody/tr[12]/td[11]').get_attribute('innerHTML').replace('.', ',')
    roi = driver.find_element_by_xpath('//*[@id="tab-profitability"]/table[2]/tbody/tr[14]/td[11]').get_attribute('innerHTML').replace('.', ',')

    current_ratio = driver.find_element_by_xpath('//*[@id="tab-financial"]/table[2]/tbody/tr[2]/td[11]').get_attribute('innerHTML').replace('.', ',')
    debt_equity = driver.find_element_by_xpath('//*[@id="tab-financial"]/table[2]/tbody/tr[8]/td[11]').get_attribute('innerHTML').replace('.', ',')
    R3 = driver.find_element_by_xpath('//*[@id="financials"]/table/tbody/tr[10]/td[8]').get_attribute('innerHTML')
    R2 = driver.find_element_by_xpath('//*[@id="financials"]/table/tbody/tr[10]/td[9]').get_attribute('innerHTML')
    R1 = driver.find_element_by_xpath('//*[@id="financials"]/table/tbody/tr[10]/td[10]').get_attribute('innerHTML')
    TTM = driver.find_element_by_xpath('//*[@id="financials"]/table/tbody/tr[10]/td[11]').get_attribute('innerHTML')

    with open('data/data_' + token + '.txt', 'w') as f:
        f.write('Ticker; date; P/E; P/B; P/S; P/CF; Div %; PEG; Cash return; Free CF/Revenue %; Operating Margin; ROE; ROI; Current Ratio; Debt/Equity\n; R-3; R-2; R-1; TTM')
        f.write(f'{token} ;{datetime.now().strftime("%Y/%m/%d")}; {price_earnings}; {price_book}; {price_sales}; {price_cash_flow}; {dividend_yield}; {peg_ratio}; {cash_return}; {revenue}; {operating_margin}; {roe}; {roi}; {current_ratio}; {debt_equity}; {R3}; {R2}; {R1}; {TTM}')
        print('\n\n----------------------------------------------------')
        print('Ticker; date; P/E; P/B; P/S; P/CF; Div %; PEG; Cash return; Free CF/Revenue %; Operating Margin; ROE; ROI; Current Ratio; Debt/Equity; R-3; R-2; R-1; TTM')
        print(f'{token} ;{datetime.now().strftime("%Y/%m/%d")}; {price_earnings}; {price_book}; {price_sales}; {price_cash_flow}; {dividend_yield}; {peg_ratio}; {cash_return}; {revenue}; {operating_margin}; {roe}; {roi}; {current_ratio}; {debt_equity}; {R3}; {R2}; {R1}; {TTM}')

    print('----------------------------------------------------\n\n')
    main()


main()
