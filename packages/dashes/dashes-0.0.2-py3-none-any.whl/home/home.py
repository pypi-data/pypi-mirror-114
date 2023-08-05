import streamlit as st
from PIL import Image as imging
from dashes.background.background import set_png_as_page_bg
def main():
    img = imging.open("x.jpeg")
    st.image(img,width=1000)
    # set_png_as_page_bg('covid2.png')
    st.title("Covid-19 DASHBOARD")
    txt = """
    This web application will serve to analyze, visualize, the spread of Covid-19.
    Coronavirus disease 2019 (COVID-19) is a contagious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2).
    The first known case was identified in Wuhan, China, in December 2019.
    The disease has since spread worldwide, leading to an ongoing pandemic.
    """
    st.write(txt)
    st.markdown('Symptoms')
    st.markdown(("* Respiratory symptoms\n""* Fever\n""* Cough\n""* Shortness of breath\n"))
    st.markdown("Vaccines")
    st.markdown("Track [here](https://www.raps.org/news-and-articles/news-articles/2020/3/covid-19-vaccine-tracker)")