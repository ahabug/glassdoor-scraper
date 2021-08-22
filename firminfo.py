import json
import logging.config
import time
from multiprocessing.pool import ThreadPool

import pandas as pd
from selenium import webdriver

import csv

CSV_FILE_PATH = './company_list.csv'
df = pd.read_csv(CSV_FILE_PATH)

with open('secret.json') as file:
    d = json.loads(file.read())
    username = d['username']
    password = d['password']

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

logger.addHandler(ch)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d :%(filename)s(%(process)d) - %(message)s')
ch.setFormatter(formatter)
logging.getLogger('selenium').setLevel(logging.CRITICAL)

start_from_base = True
failed_company = []


def save2csv(data_list):
    df = pd.DataFrame(data_list)
    with open('info.csv', 'a', encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=df.columns)
        for data in data_list:
            writer.writerow(data)
            # logger.info(data)


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    chrome = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
    return chrome


def sign_in(driver):
    logger.info(f'Signing in to {username}')
    try:
        email_field = driver.find_element_by_name('userEmail')
        password_field = driver.find_element_by_name('userPassword')
        submit_btn = driver.find_element_by_xpath('//button[@type="submit"]')

        email_field.send_keys(username)
        password_field.send_keys(password)
        submit_btn.click()
        time.sleep(1)
    except:
        logger.info('failed to sign in')


def detect_sign(driver):
    logger.info('detecing sign-in button')
    try:
        if 'Sign' in driver.find_element_by_name('hardsell py-xl').text:
            logger.info('find sign-in button')
            sign = driver.find_element_by_xpath('//a[@class="link ml-xxsm"]')
            sign.click()
            sign_in(driver)
    except:
        logger.info('no button')
        pass


def no_reviews():
    return False
    # Todo: Find a company without reviews to test on


def extract_from_page(driver, company_ticker, company_url, x):
    res = {}
    res["No."] = x
    res["name"] = company_ticker
    res["url"] = company_url
    res["English_total"] = driver.find_element_by_xpath(
        '//h2[@class="css-ntu5m7 col-6 my-0"]//strong[1]').text.replace(',', '')
    res["Total"] = driver.find_element_by_xpath(
        '//h2[@class="css-ntu5m7 col-6 my-0"]//strong[2]').text.replace(',', '')
    res["CE0_name"] = driver.find_element_by_xpath(
        '//div[@class="donut-text d-lg-table-cell pt-sm pt-lg-0 pl-lg-sm"]/div[1]').text
    res["CEO_num"] = driver.find_element_by_xpath('//div[@class="numCEORatings"]').text.replace(
        ' Ratings', '').replace(',', '')
    pros_area = driver.find_element_by_xpath(
        '//div[@class="common__EIReviewHighlightsStyles__prosContainerStyles p-std mb-md"]')
    try:
        res["Pros1_text"] = pros_area.find_element_by_xpath('//li[1]/p/span[1]').text
    except:
        res["Pros1_text"] = ''
    try:
        res["Pros1_color"] = pros_area.find_element_by_xpath('//li[1]/p/span[1]/a').text
    except:
        res["Pros1_color"] = ''
    try:
        res["Pros1_num"] = pros_area.find_element_by_xpath('//li[1]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Pros1_num"] = ''
    try:
        res["Pros2_text"] = pros_area.find_element_by_xpath('//li[2]/p/span[1]').text
    except:
        res["Pros2_text"] = ''
    try:
        res["Pros2_color"] = pros_area.find_element_by_xpath('//li[2]/p/span[1]/a').text
    except:
        res["Pros2_color"] = ''
    try:
        res["Pros2_num"] = pros_area.find_element_by_xpath('//li[2]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Pros2_num"] = ''
    try:
        res["Pros3_text"] = pros_area.find_element_by_xpath('//li[3]/p/span[1]').text
    except:
        res["Pros3_text"] = ''
    try:
        res["Pros3_color"] = pros_area.find_element_by_xpath('//li[3]/p/span[1]/a').text
    except:
        res["Pros3_color"] = ''
    try:
        res["Pros3_num"] = pros_area.find_element_by_xpath('//li[3]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Pros3_num"] = ''
    try:
        res["Pros4_text"] = pros_area.find_element_by_xpath('//li[4]/p/span[1]').text
    except:
        res["Pros4_text"] = ''
    try:
        res["Pros4_color"] = pros_area.find_element_by_xpath('//li[4]/p/span[1]/a').text
    except:
        res["Pros4_color"] = ''
    try:
        res["Pros4_num"] = pros_area.find_element_by_xpath('//li[4]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Pros4_num"] = ''
    try:
        res["Pros5_text"] = pros_area.find_element_by_xpath('//li[5]/p/span[1]').text
    except:
        res["Pros5_text"] = ''
    try:
        res["Pros5_color"] = pros_area.find_element_by_xpath('//li[5]/p/span[1]/a').text
    except:
        res["Pros5_color"] = ''
    try:
        res["Pros5_num"] = pros_area.find_element_by_xpath('//li[5]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Pros5_num"] = ''

    cons_area = driver.find_element_by_xpath(
        '//div[@class="common__EIReviewHighlightsStyles__consContainerStyles p-std"]')
    try:
        res["Cons1_text"] = cons_area.find_element_by_xpath('//li[1]/p/span[1]').text
    except:
        res["Cons1_text"] = ''
    try:
        res["Cons1_color"] = cons_area.find_element_by_xpath('//li[1]/p/span[1]/a').text
    except:
        res["Cons1_color"] = ''
    try:
        res["Cons1_num"] = cons_area.find_element_by_xpath('//li[1]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Cons1_num"] = ''
    try:
        res["Cons2_text"] = cons_area.find_element_by_xpath('//li[2]/p/span[1]').text
    except:
        res["Cons2_text"] = ''
    try:
        res["Cons2_color"] = cons_area.find_element_by_xpath('//li[2]/p/span[1]/a').text
    except:
        res["Cons2_color"] = ''
    try:
        res["Cons2_num"] = cons_area.find_element_by_xpath('//li[2]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Cons2_num"] = ''
    try:
        res["Cons3_text"] = cons_area.find_element_by_xpath('//li[3]/p/span[1]').text
    except:
        res["Cons3_text"] = ''
    try:
        res["Cons3_color"] = cons_area.find_element_by_xpath('//li[3]/p/span[1]/a').text
    except:
        res["Cons3_color"] = ''
    try:
        res["Cons3_num"] = cons_area.find_element_by_xpath('//li[3]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Cons3_num"] = ''
    try:
        res["Cons4_text"] = cons_area.find_element_by_xpath('//li[4]/p/span[1]').text
    except:
        res["Cons4_text"] = ''
    try:
        res["Cons4_color"] = cons_area.find_element_by_xpath('//li[4]/p/span[1]/a').text
    except:
        res["Cons4_color"] = ''
    try:
        res["Cons4_num"] = cons_area.find_element_by_xpath('//li[4]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Cons4_num"] = ''
    try:
        res["Cons5_text"] = cons_area.find_element_by_xpath('//li[5]/p/span[1]').text
    except:
        res["Cons5_text"] = ''
    try:
        res["Cons5_color"] = cons_area.find_element_by_xpath('//li[5]/p/span[1]/a').text
    except:
        res["Cons5_color"] = ''
    try:
        res["Cons5_num"] = cons_area.find_element_by_xpath('//li[5]/p/span[2]').text.replace(' reviews)', '').replace(
            '(in ', '')
    except:
        res["Cons5_num"] = ''

    # score = driver.find_element_by_xpath('//div[@class="v2__EIReviewsRatingsStylesV2__ratingInfo"]')
    # score.click()
    # # overall
    # try:
    #     button = driver.find_element_by_xpath('//span[@class="eiRatingTrends__RatingTrendsStyle__overallRatingNum"]')
    #     button.click()
    #     res["Overall"] = button.text
    # except:
    #     res["Overall"] = ''
    # try:
    #     res["5star_overall"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["5star_overall"] = ''
    # try:
    #     res["4star_overall"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["4star_overall"] = ''
    # try:
    #     res["3star_overall"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["3star_overall"] = ''
    # try:
    #     res["2star_overall"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["2star_overall"] = ''
    # try:
    #     res["1star_overall"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["1star_overall"] = ''
    # # culture
    # try:
    #     button = driver.find_element_by_xpath(
    #         '//div[@class="row mx-0 mt-std"]//div[@class="mb"]/div[2]/div[@class="col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum"]')
    #     button.click()
    #     res["Culture_values"] = button.text
    # except:
    #     res["Culture_values"] = ''
    # try:
    #     res["5star_culture_values"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["5star_culture_values"] = ''
    # try:
    #     res["4star_culture_values"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["4star_culture_values"] = ''
    # try:
    #     res["3star_culture_values"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["3star_culture_values"] = ''
    # try:
    #     res["2star_culture_values"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["2star_culture_values"] = ''
    # try:
    #     res["1star_culture_values"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["1star_culture_values"] = ''
    # # diveristy
    # try:
    #     button = driver.find_element_by_xpath(
    #         '//div[@class="row mx-0 mt-std"]//div[@class="mb"]/div[3]/div[@class="col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum"]')
    #     button.click()
    #     res["Diversity_inclusion"] = button.text
    # except:
    #     res["Diversity_inclusion"] = ''
    # try:
    #     res["5star_diversity_inclusion"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["5star_diversity_inclusion"] = ''
    # try:
    #     res["4star_diversity_inclusion"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["4star_diversity_inclusion"] = ''
    # try:
    #     res["3star_diversity_inclusion"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["3star_diversity_inclusion"] = ''
    # try:
    #     res["2star_diversity_inclusion"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["2star_diversity_inclusion"] = ''
    # try:
    #     res["1star_diversity_inclusion"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["1star_diversity_inclusion"] = ''
    # # work life
    # try:
    #     button = driver.find_element_by_xpath(
    #         '//div[@class="row mx-0 mt-std"]//div[@class="mb"]/div[4]/div[@class="col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum"]')
    #     button.click()
    #     res["Worklife_balance"] = button.text
    # except:
    #     res["Worklife_balance"] = ''
    # try:
    #     res["5star_worklife_balance"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["5star_worklife_balance"] = ''
    # try:
    #     res["4star_worklife_balance"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["4star_worklife_balance"] = ''
    # try:
    #     res["3star_worklife_balance"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["3star_worklife_balance"] = ''
    # try:
    #     res["2star_worklife_balance"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["2star_worklife_balance"] = ''
    # try:
    #     res["1star_worklife_balance"] = driver.find_element_by_xpath(
    #         '//span[@class="barTable"]//span[1]').get_attribute('style')
    # except:
    #     res["1star_worklife_balance"] = ''
    # # senior
    # try:
    #     button = driver.find_element_by_xpath(
    #         '//div[@class="row mx-0 mt-std"]//div[@class="mb"]/div[5]/div[@class="col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum"]')
    #     button.click()
    #     res["Senior_management"] = button.text
    # except:
    #     res["Senior_management"] = ''
    # try:
    #     res["5star_senior_mgmt"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["5star_senior_mgmt"] = ''
    # try:
    #     res["4star_senior_mgmt"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["4star_senior_mgmt"] = ''
    # try:
    #     res["3star_senior_mgmt"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["3star_senior_mgmt"] = ''
    # try:
    #     res["2star_senior_mgmt"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["2star_senior_mgmt"] = ''
    # try:
    #     res["1star_senior_mgmt"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["1star_senior_mgmt"] = ''
    # # Compensation_benefits
    # try:
    #     button = driver.find_element_by_xpath(
    #         '//div[@class="row mx-0 mt-std"]//div[@class="mb"]/div[6]/div[@class="col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum"]')
    #     button.click()
    #     res["Compensation_benefits"] = button.text
    # except:
    #     res["Compensation_benefits"] = ''
    # try:
    #     res["5star_comp_benefit"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["5star_comp_benefit"] = ''
    # try:
    #     res["4star_comp_benefit"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["4star_comp_benefit"] = ''
    # try:
    #     res["3star_comp_benefit"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["3star_comp_benefit"] = ''
    # try:
    #     res["2star_comp_benefit"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["2star_comp_benefit"] = ''
    # try:
    #     res["1star_comp_benefit"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["1star_comp_benefit"] = ''
    # # Career_opportunities
    # try:
    #     button = driver.find_element_by_xpath(
    #         '//div[@class="row mx-0 mt-std"]//div[@class="mb"]/div[7]/div[@class="col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum"]')
    #     button.click()
    #     res["Career_opportunities"] = button.text
    # except:
    #     res["Career_opportunities"] = ''
    # try:
    #     res["5star_career_oppo"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["5star_career_oppo"] = ''
    # try:
    #     res["4star_career_oppo"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["4star_career_oppo"] = ''
    # try:
    #     res["3star_career_oppo"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["3star_career_oppo"] = ''
    # try:
    #     res["2star_career_oppo"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["2star_career_oppo"] = ''
    # try:
    #     res["1star_career_oppo"] = driver.find_element_by_xpath('//span[@class="barTable"]//span[1]').get_attribute(
    #         'style')
    # except:
    #     res["1star_career_oppo"] = ''
    logger.info(res)
    return res


def main(x):
    driver = get_driver()
    company_ticker = df.iat[x, 1]
    company_url = df.iat[x, 2]
    driver.get(company_url)
    time.sleep(10)
    logger.info(f'{x} thread: Now we are scraping infos of {company_ticker}')
    more_info = driver.find_element_by_xpath('//span[@class="SVGInline d-flex ml-sm link"]')
    more_info.click()
    info_dict = extract_from_page(driver, company_ticker, company_url, x)
    save2csv([info_dict])
    logger.info(f'"{x}" thread: Writing {company_ticker}.')
    driver.quit()


def get_company_list():
    return [i for i in range(len(df))]


if __name__ == '__main__':
    # main(4)
    start_time_main = time.time()
    pool = ThreadPool(4)
    pool.map_async(main, get_company_list())
    pool.close()
    pool.join()
    failed_company = pd.DataFrame(failed_company)
    failed_company.to_csv('failed_company.csv', index=False)
    end_time_main = time.time()
    logger.info(f'Finished in {(end_time_main - start_time_main) / 60} minutes')
