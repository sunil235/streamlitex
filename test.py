import pandas as pd


def get_BTC_data():
    AWS_BUCKET_URL = "http://crypto-price-bucket.s3-website-us-east-1.amazonaws.com"
    df3 = pd.read_csv(AWS_BUCKET_URL + "/crypto_results")
    return df3


try:
    df = get_BTC_data()
    df.head(10)

except Exception as e:
    print(e)
