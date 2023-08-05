import streamlit as st
from dashes.background.background import set_png_as_page_bg

def main():
    set_png_as_page_bg('x.png')
    st.title("About")
    st.balloons()
    st.info(
        """
        This app is maintained by Arohan. You can learn more about me at
        https://sites.google.com/view/arohan/.
        """
)