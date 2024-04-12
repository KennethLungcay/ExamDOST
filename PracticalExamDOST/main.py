import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

def main():
   
    
    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Admin"])
    
    if page == "Home":
        display_home_page()
    elif page == "Admin":
        display_page_1()
 

def display_home_page():

    st.title("Geometry of the USA with Streamlit and Folium")
    geojson_filepath = 'us-states.json'
    m = folium.Map(location=[37.090240,-95.712891], zoom_start=4)
    
    # Add GeoJson layer to the map
    geojson = folium.GeoJson(
        geojson_filepath,
        name='geojson',
        tooltip=folium.GeoJsonTooltip(fields=['name'], labels=True, sticky=False),
        style_function=lambda feature: {'fillColor': 'green' if feature['properties']['name'] == 'Minnesota' else 'blue', 'color': 'black', 'weight': 1}
    ).add_to(m)

    # Add the map to Streamlit
    folium_static(m)

def display_page_1():
    # Sample data
    data = {
        'Name': ['John', 'Alice', 'Bob'],
        'Age': [30, 25, 35],
        'Location': ['New York', 'Paris', 'London']
    }

    df = pd.DataFrame(data)

    # Function to generate HTML button
    def get_button_html(label):
        return f'<button>{label}</button>'

    # Add buttons to the DataFrame
    df['Actions'] = df.apply(lambda row: get_button_html('Update') + " " + get_button_html('Edit'), axis=1)

    # Displaying the table using st.write() with HTML formatting
    st.write('<h2>Custom Table</h2>', unsafe_allow_html=True)
    st.write(df.to_html(escape=False), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
