import streamlit as st
import streamlit_folium as sf
import folium
from streamlit_folium import folium_static
import pandas as pd
from db_connector import MySQLDatabase
import json
from sqlalchemy import Table, Column, String, Text, insert
from db_connector import db




def main():

   


    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Admin"])
    
    if page == "Home":
        display_home_page()
    elif page == "Admin":
        display_page_1()

def display_home_page():

    st.title("Geometry of the USA with Streamlit and Folium Data Reference Only")
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

   

   

    # Execute query to fetch data
    query = "SELECT id,name,type,geometry_type,population,coordinates FROM states"
    data = db.execute_query(query)

    feature_collection = {
        "type": "FeatureCollection",
        "features": []
    }

    for row in data:
        coordinate_str = row[5]
        
        try:
            coordinate_list = json.loads(coordinate_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic coordinate_str: {coordinate_str}")
            continue  # Skip this row and proceed to the next one
        
        feature = {
            "type": "Feature",
            "properties": {
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "geometry_type": row[3],
                "population":row[4]
            },
            "geometry": {
                "type": row[3],
                "coordinates": coordinate_list
            }
        }
        feature_collection["features"].append(feature)

    # Convert the GeoJSON feature collection to a string
    geojson_str = json.dumps(feature_collection)

    # # Display the GeoJSON data as a JSON string
    # st.title("GeoJSON Data")
    # st.json(geojson_str)
    
    #function for coloring based on population
    def color_based_on_population(feature):
        population = feature['properties']['population']
        if population >= 20:
            return 'green'
        elif 10 <= population < 20:
            return 'orange'
        else:
            return 'red'

    st.title("GeoJSON Data Visualization Dynamic Feature")
    map_folium = folium.Map(location=[37.090240,-95.712891], zoom_start=4)
    folium.GeoJson(
        geojson_str, 
        style_function=lambda feature: {
            'fillColor': color_based_on_population(feature),
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5'
        },
        tooltip=folium.GeoJsonTooltip(fields=['name', 'population'], labels=True, sticky=False)
    ).add_to(map_folium)
    sf.folium_static(map_folium)



def display_page_1():

    st.title("Admin")
    st.write("Data from MySQL query:")


    # LIST
    query = "SELECT id, name, type, population,geometry_type FROM states"
    data = db.execute_query(query)
    st.table(data)
    st.subheader("CRUD Operations")



    # INSERT OPERATION
    st.write("### Create Operation")
    new_id = st.text_input("ID")
    new_name = st.text_input("Name")
    new_type = st.text_input("Type")
    new_geometry_type = st.text_input("eometry Type")
    new_population = st.number_input("Population",step=1)
    new_coordinates = st.text_area("Coordinates")

    if st.button("Add New Record"):
        try:
            db.execute_insert('states',id=new_id.upper(), name=new_name, type=new_type, geometry_type=new_geometry_type,population=new_population, coordinates=new_coordinates)
            st.success("New record added successfully!")
        except Exception as e:
            st.error(f"Error adding new record: {e}")




   # UPDATE OPERATION
    def fetch_data(updated_id):
        query = f"SELECT id, name, type, geometry_type,population,coordinates FROM states WHERE id='{updated_id}'"
        result = db.execute_query(query)
        if result:
            # Convert the first row of the result into a dictionary
            data = {'id': result[0][0], 'name': result[0][1], 'type': result[0][2], 'geometry_type': result[0][3],  'population': result[0][4] , 'coordinates': result[0][5]}
            return data
        else:
            return None


    st.write("### Update Operation")
    updated_id = st.text_input("Update ID")

    # Fetch data when the ID is updated
    if updated_id:
        data = fetch_data(updated_id)
        if data:
            updated_name = st.text_input("New Name", value=data['name'])
            updated_type = st.text_input("New Type", value=data['type'])
            updated_geometry_type = st.text_input("New Geometry Type", value=data['geometry_type'])
            updated_population = st.text_input("Population Count Update", value=data['population'])
            updated_coordinate = st.text_area("New Coordinates", value=data['coordinates'])
        else:
            st.write("No data found for the given ID.")
    else:
        updated_name = st.text_input("New Name")
        updated_type = st.text_input("New Type")
        updated_geometry_type = st.text_input("New Geometry Type")
        updated_population =  st.text_input("Population Count Update")
        updated_coordinate = st.text_area("New Coordinates")

    # Update button
    if st.button("Update Record"):
        try:
            update_values = {
                'name': updated_name,
                'type': updated_type,
                'geometry_type':updated_geometry_type,
                'population':updated_population,
                'coordinates': updated_coordinate
            }
            db.execute_update('states', 'id', updated_id.upper(), update_values)
            st.success("Record updated successfully!")
        except Exception as e:
            st.error(f"Error updating record: {e}")

   
   
    #DELETE OPERATION
    st.write("### Delete Operation")
    delete_id = st.text_input("ID to delete")
    if st.button('Delete'):
        rows_deleted = db.delete_data(delete_id)
        if rows_deleted > 0:
            st.success(f"Deleted {rows_deleted} row(s) with ID {delete_id}")
        else:
            st.error("No rows were deleted. Please check the ID.")




if __name__ == '__main__':
    main()
