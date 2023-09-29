import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import altair as alt

import matplotlib.pyplot as plt
from matplotlib import style
import altair as alt
import plost

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="upsnjp-dashboard", page_icon=":bar_chart:", layout="wide"
)
st.title("UPSNJP Dashboard")
# :bar_chart:
st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)

df = pd.read_excel("UPSNJP_HOUSEHOLD_SURVEY.xls")

# region count
region_count = df.groupby(["region"]).size().reset_index(name="count")
regDict = dict(region_count.values)
oro_count = regDict.get("Oromiya", 0)
snnp_count = regDict.get("SNNP", 0)
aa_count = regDict.get("Addis Ababa", 0)
dire_count = regDict.get("Dire Dawa", 0)
gambela_count = regDict.get("Gambella", 0)
harari_count = regDict.get("Harari", 0)
somali_count = regDict.get("Somali", 0)
total = oro_count + snnp_count + aa_count + dire_count + harari_count + somali_count


col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((8))
with col1:
    # st.image("images/rectangle.png", use_column_width="Auto")
    col1.metric("Oromiya", oro_count)
with col2:
    # st.image("images/rectangle.png", use_column_width="Auto")
    col2.metric("SNNP", snnp_count)
with col3:
    col3.metric("Addis Ababa", aa_count)
with col4:
    col4.metric("Dire Dawa", dire_count)
with col5:
    col5.metric("Gambela", gambela_count)
with col6:
    col6.metric("Harari", harari_count)
with col7:
    col7.metric("Somali", somali_count)
with col8:
    col8.metric("TOTAL", total)
# ---------------------------------------------
# df["start_date"] = pd.to_datetime(df["start_date"])

# Getting the min and max date
# startDate = pd.to_datetime(df["ID15"]).min()
# endDate = pd.to_datetime(df["ID15"]).max()


# with col1:
# date1 = pd.to_datetime(st.date_input("Start Date", startDate))

# with col2:
# date2 = pd.to_datetime(st.date_input("End Date", endDate))

# df = df[(df["ID15"] >= date1) & (df["ID15"] <= date2)].copy()


# -----------------------------------------------------------------
# Location selection sidebar

st.sidebar.header("Filter by Location: ")

# Region
region = st.sidebar.multiselect("region", df["region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["region"].isin(region)]

# Woreda
woreda = st.sidebar.multiselect("woreda", df2["woreda"].unique())
if not woreda:
    df3 = df2.copy()
else:
    df3 = df2[df2["woreda"].isin(woreda)]

# Kebele
kebele = st.sidebar.multiselect("Kebele", df3["kebele"].unique())

# Filter by location

if not region and not woreda and not kebele:
    filtered_df = df
elif not woreda and not kebele:
    filtered_df = df[df["region"].isin(region)]
elif not region and not kebele:
    filtered_df = df[df["woreda"].isin(woreda)]
elif woreda and kebele:
    filtered_df = df3[df["woreda"].isin(woreda) & df3["kebele"].isin(kebele)]
elif region and kebele:
    filtered_df = df3[df["region"].isin(region) & df3["kebele"].isin(kebele)]
elif region and woreda:
    filtered_df = df3[df["region"].isin(region) & df3["woreda"].isin(woreda)]
elif kebele:
    filtered_df = df3[df3["kebele"].isin(kebele)]
else:
    filtered_df = df3[
        df3["region"].isin(region)
        & df3["woreda"].isin(woreda)
        & df3["kebele"].isin(kebele)
    ]

# -----------------------------------------------------------------------------------#
region_exp_dic = {
    "Addis Ababa": 988,
    "Dire Dawa": 936,
    "Gambella": 377,
    "Harari": 371,
    "Oromiya": 2359,
    "SNNP": 1043,
    "Somali": 206,
}

category_df = filtered_df.groupby(by=["region"], as_index=False)["COLLECTED"].sum()

category_df["EXPECTED"] = category_df["region"].map(region_exp_dic)


col1, col2 = st.columns((2))

upsnjp_enrolled = filtered_df.groupby(by=["u1"], as_index=False)["COLLECTED"].sum()

with col1:
    st.subheader("Interviews by region")
    plost.bar_chart(
        data=category_df,
        bar="region",
        value=["COLLECTED", "EXPECTED"],
        group=True,
        width=55,
    )

with col2:
    st.subheader("UPSNJP enrolled Household")
    fig = px.pie(filtered_df, values="COLLECTED", names="u1", hole=0.5)
    fig.update_traces(text=filtered_df["u1"], textposition="outside")
    st.plotly_chart(fig, use_container_width=False)


# -----------------------------------------------------------------------------


col1, col2 = st.columns(2)
with col1:
    supervisor_df = filtered_df.groupby(by=["supervisor"], as_index=False)[
        "COLLECTED"
    ].sum()
    st.subheader("Collected data by supervisor")
    fig = px.bar(supervisor_df, x="supervisor", y="COLLECTED", template="seaborn")
    fig.update_layout(width=600)
    st.plotly_chart(fig, use_container_width=False)


with col2:
    owned_business_df = filtered_df.groupby(by=["i1_1"], as_index=False)[
        "COLLECTED"
    ].sum()
    print(owned_business_df)
    st.subheader("Household Owned Business")
    fig = px.pie(
        owned_business_df, values="COLLECTED", names="i1_1", template="plotly_dark"
    )
    fig.update_traces(text=owned_business_df["i1_1"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
