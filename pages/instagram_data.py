
import streamlit as st
import pandas as pd
from logics.load_data import instagram_data_load
from logics.config import SECRETS

def main():
    st.title("Instagram Data Analysis")
    
    # Add your Instagram analysis code here
    st.write("Welcome to the Instagram Data Dashboard!")

if __name__ == "__main__":
    main()
