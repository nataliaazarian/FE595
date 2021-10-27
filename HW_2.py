import requests
import pandas as pd
from bs4 import BeautifulSoup

def co_detail_extract(num_co=50):
    
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

    df = pd.DataFrame({"Company_Name":[], "Company_Purpose":[]})

    files = glob.glob("data/*.csv")
    for file in files:
        try:
            tempdf = pd.read_csv(file)
        except:
            tempdf = pd.read_csv(file, sep="\t")
        
        try:
            tempdf.columns = df.columns
        except:
            tempdf.drop("Unnamed: 0", axis=1, inplace=True)
            tempdf.columns = df.columns

        df = df.append(tempdf, ignore_index=True)

    return df


def perform_nlp(df):
    
    sid = SentimentIntensityAnalyzer()

    df["Sentiment"] = df["Company_Purpose"].apply(lambda x: sid.polarity_scores(x)['compound'])

    df.sort_values("Sentiment", ascending=False, inplace=True)

    print(df.head())
    print(df.tail())
    df.to_csv("output.csv", index=False)
    return df



if __name__ == '__main__':

    # print(combine_files())
    perform_nlp(combine_files())
    # perform_nlp(combine_files())
    # print(pd.read_csv("data/fake_company.csv", sep="\t"))

# if __name__ == '__main__':
#     co_detail_extract()