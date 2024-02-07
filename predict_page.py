import streamlit as st
import pickle
import numpy as np
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.grid import grid

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

dec_tree_reg_loaded = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_devtype = data["le_devtype"]

def show_predict_page():

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

    st.write("""### Kami membutuhkan beberapa infomasi untuk memprediksi gaji""")

    countries = (
        "Australia",
        "Brazil",
        "Canada",
        "Denmark",
        "France",
        "Germany",
        "India",
        "Israel",
        "Italy",
        "Netherlands",
        "Norway",
        "Poland",
        "Spain",
        "Sweden",
        "Switzerland",
        "United Kingdom of Great Britain and Northern Ireland",
        "United States of America",
    )

    education = (
        "Di bawah sarjana",
        "Sarjana",
        "Magister",
        "Pasca sarjana",
    )

    devtype = (
        "Academic researcher",
        "Cloud infrastructure engineer",
        "Data or business analyst",
        "Data scientist or machine learning specialist",
        "DevOps specialist",
        "Developer, back-end",
        "Developer, desktop or enterprise applications",
        "Developer, embedded applications or devices",
        "Developer, front-end",
        "Developer, full-stack",
        "Developer, game or graphics",
        "Developer, mobile",
        "Engineer, data",
        "Engineering manager",
        "Research & Development role",
        "Senior Executive (C-Suite, VP, etc.)",
    )

    country = st.selectbox("Negara", countries)
    education = st.selectbox("Tingkat Pendidikan", education)
    devtype = st.selectbox("Jenis Developer", devtype)

    expericence = st.slider("Pengalaman (Tahun)", 0, 50, 3)

    ok = st.button("Prediksi Gaji")
    if ok:
        X = np.array([[country, education, expericence, devtype]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X[:, 3] = le_devtype.transform(X[:,3])
        X = X.astype(float)

        salary = dec_tree_reg_loaded.predict(X)
        rupiah = salary*15710
        st.subheader(f"Perkiraan gaji pertahun adalah ${salary[0]:,.02f}")
        st.subheader(f"Dalam Rupiah = Rp{rupiah[0]:,.02f} (Kurs: 15.707,00)")
