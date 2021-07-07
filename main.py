import streamlit as st
import pandas as pd
import altair as alt

from urllib.error import URLError


@st.cache
def get_UN_data():
    AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df1 = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df1.set_index("Region")

def get_BTC_data():
    AWS_BUCKET_URL = "http://crypto-price-bucket.s3-website-us-east-1.amazonaws.com"
    df3 = pd.read_csv(AWS_BUCKET_URL + "/crypto_results")
    return df3.set_index("Region")

try:
    df = get_UN_data()
    df.head(10)
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
