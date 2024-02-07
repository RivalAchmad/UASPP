import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.grid import grid

st.set_page_config(layout="wide")

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Sarjana'
    if 'Master’s degree' in x:
        return 'Magister'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Pasca sarjana'
    return 'Di bawah sarjana'


@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "DevType", "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

    DevType_map = shorten_categories(df.DevType.value_counts(), 265)
    df['DevType'] = df['DevType'].map(DevType_map)
    df = df[df['DevType'] != 'Other']
    df = df[df['DevType'] != 'Other (please specify):']
    return df

df = load_data()

def show_explore_page():
    col1, col2, col3 = st.columns([0.1, 0.6, 0.1])

    with col1:
        st.image('salary.gif')

    with col2:
        with stylable_container(
            key="container_title",
            css_styles="""
                {
                    border: 2px solid #ccc; /* Warna dan ketebalan border */
                    background-color: rgb(212, 255, 192); /* Warna background */
                    padding: 10px; /* Jarak antara isi dan border */
                    margin-bottom: 30px;
                    text-align: center;
                }
            """
        ):

             st.title("💸    Eksplor Gaji Software Developer    💸")

    with col3:
        st.image('salary.gif')

    st.write(
        """
    ### Stack Overflow Developer Survey 2023
    """
    )

    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 2px solid #ccc; /* Warna dan ketebalan border */
                border-radius: 10px; /* Jari-jari sudut (rounded corners) */
                background-color: #ffffff; /* Warna background */
                padding: 20px; /* Jarak antara isi dan border */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Efek bayangan (shadow) */
                margin-bottom: 30px;
            }
        """
    ):

        data = df["Country"].value_counts()

        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
        ax1.axis("equal")

        st.write("""#### Banyak data dari berbagai negara""")
        my_grid = grid(1, vertical_align="bottom")
        my_grid.pyplot(fig1)
    
    col1, col2 = st.columns([0.5, 0.5], gap="small")

    with col1:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 2px solid #ccc; /* Warna dan ketebalan border */
                border-radius: 10px; /* Jari-jari sudut (rounded corners) */
                background-color: #ffffff; /* Warna background */
                padding: 20px; /* Jarak antara isi dan border */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Efek bayangan (shadow) */
                margin-bottom: 30px;
            }
        """
    ):
         st.write(
            """
         #### Rata-rata gaji per tahun berdasarkan negara (US$)
         """
         )

         data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
         my_grid = grid(1, vertical_align="bottom")
         my_grid.bar_chart(data)
    
    with col2:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 2px solid #ccc; /* Warna dan ketebalan border */
                border-radius: 10px; /* Jari-jari sudut (rounded corners) */
                background-color: #ffffff; /* Warna background */
                padding: 20px; /* Jarak antara isi dan border */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Efek bayangan (shadow) */
                margin-bottom: 30px;
            }
        """
    ):

         st.write(
            """
         #### Rata-rata gaji per tahun berdasarkan pengalaman (US$)
         """
         )

         data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
         my_grid = grid(1, vertical_align="bottom")
         my_grid.line_chart(data)

    col3, col4 = st.columns([0.5, 0.5], gap="small")

    with col3:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 2px solid #ccc; /* Warna dan ketebalan border */
                border-radius: 10px; /* Jari-jari sudut (rounded corners) */
                background-color: #ffffff; /* Warna background */
                padding: 20px; /* Jarak antara isi dan border */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Efek bayangan (shadow) */
            }
        """
    ):

         st.write(
            """
         #### Rata-rata gaji per tahun berdasarkan tingkat pendidikan (US$)
         """
         )

         data = df.groupby(["EdLevel"])["Salary"].mean().sort_values(ascending=True)
         my_grid = grid(1, vertical_align="bottom")
         my_grid.bar_chart(data)

    col1, col2 = st.columns([0.5, 0.5], gap="small")

    with col4:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 2px solid #ccc; /* Warna dan ketebalan border */
                border-radius: 10px; /* Jari-jari sudut (rounded corners) */
                background-color: #ffffff; /* Warna background */
                padding: 20px; /* Jarak antara isi dan border */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Efek bayangan (shadow) */
            }
        """
    ):

         st.write(
            """
         #### Rata-rata gaji per tahun berdasarkan jenis developer (US$)
         """
         )

         data = df.groupby(["DevType"])["Salary"].mean().sort_values(ascending=True)
         my_grid = grid(1, vertical_align="bottom")
         my_grid.bar_chart(data)