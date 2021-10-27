import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

os.chdir(r'C:\Users\Nazarilla\OneDrive\Documents\Academic\Stevens Institute\FinTech\Git Projects\FE595')

def detail_extract(num_co=50):
    
    # Create blank dataframe for select company information
    co_info = pd.DataFrame({"Name":[], "Purpose":[]})
    
    ## Check status code -- MOVE THIS WITHIN WHILE LOOP
    #resp.status_code
    
    i = 0
    
    while i < num_co:
        # Connect to site
        resp = requests.get("http://3.85.131.173:8000/random_company")

        # Create "soup" of html in a single string before splitting components
        soup = BeautifulSoup(resp.content, "lxml")

        # Find list of company details, prefaced by <li> and followed by </li>, in html
        html_dump = soup.find_all("li")

        # Separate field name from description for text within <li> </li> as dictionary
        co_detail = {i.decode_contents().split(":")[0].strip():i.decode_contents().split(":")[1].strip() for i in html_dump}

        # Add select company information to dataframe
        co_info = co_info.append(pd.DataFrame({"Name":[co_detail["Name"]], "Purpose":[co_detail["Purpose"]]}), ignore_index=True)

        i += 1

    # Export select company information to csv
    co_info.to_csv("company_info.csv", index=False)
    
    return co_info


def combine_files():

    df = pd.DataFrame({"Name":[], "Purpose":[]})
    
    subdf_1 = pd.read_csv('Companies.csv', names=["Name", "Purpose"])
    subdf_2 = pd.read_csv('name_purpose_pairs.csv', names=["Name", "Purpose"])
    subdf_3 = pd.read_csv('fake_company.csv', sep='\t', usecols=["Name", "Purpose"])
    subdf_4 = pd.read_csv('company_info.csv')

    df = pd.concat([subdf_1, subdf_2, subdf_3, subdf_4], ignore_index=True)

    return df


def perform_nlp(df):
    
    sia = SentimentIntensityAnalyzer()

    df["Sentiment"] = df["Purpose"].apply(lambda x: sia.polarity_scores(x)['compound'])

    df.sort_values("Sentiment", ascending=False, inplace=True)

    print(df.head())
    print(df.tail())
    df.to_csv("output.csv", index=False)
    return df

if __name__ == '__main__':
    detail_extract(num_co=50)

if __name__ == '__main__':

    # print(combine_files())
    perform_nlp(combine_files())
    # perform_nlp(combine_files())
    # print(pd.read_csv("data/fake_company.csv", sep="\t"))