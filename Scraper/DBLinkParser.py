from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from fractions import Fraction
import re
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Takes in a txt file of links from the CT database and parses their signal values into an excel file')

    parser.add_argument('-f', '--file', dest='file_path', required=True, help='Path to the file')
    parser.add_argument('-n', '--number', dest='number', type=int, help='Numbers of links to be parsed, default to all if not specified')
    args = parser.parse_args()
    file_path = args.file_path
    number = args.number

    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)

    if number is None:
        number = line_count
    elif (number <= 0) or (number > line_count):
        raise ValueError("number must be between 1 and the number of lines the file, inclusive, by default it's the line count of the file")

    links = []

    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):
            if idx >= number:
                break
            links.append(line.strip())

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    driver.get(links[0])
    sleep(10)
    signals = driver.find_elements(by=By.CLASS_NAME, value="signal-title")

    #column names for the dataframe and excel file
    signal_names = ['Name']
    for signal in signals:
        signal_names.append(signal.text.strip())

    #a list of lists to populate the dataframe and excel file
    data_rows = []
    for link in links:
        driver.get(link)
        sleep(10)
        data_row = [driver.find_element(by=By.ID, value="span-34-4566").text.strip()]
        values = driver.find_elements(by=By.CLASS_NAME, value="total-j-bar")
        #only starting from 8: because there are some bars not defined as j bars, otherwise we would need to start later than 8
        for value in values[8:]:
            raw_value = value.text
            if raw_value == '':
                raw_value = '0'
            data_row.append(float(Fraction(raw_value)))
        data_rows.append(data_row)

    df = pd.DataFrame(data_rows, columns=signal_names)
    df.to_excel('CTDBSignalData.xlsx')

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print("Error: ", e)
