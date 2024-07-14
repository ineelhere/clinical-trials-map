import requests
import pandas as pd
import folium
import folium.plugins as plugins

def myfunc(condition, location):
    url = f"https://clinicaltrials.gov/api/v2/studies?format=json&query.cond={condition}&query.locn={location}"
    
    response = requests.get(url)
    studies = response.json().get('studies', [])
    
    if len(studies) != 0:
        all_locations = []
        for study in studies:
            locations = study.get('protocolSection', {}).get('contactsLocationsModule', {}).get('locations', [])
            for location in locations:
                location['NCTId'] = study.get('protocolSection', {}).get('identificationModule', {}).get('nctId')
            all_locations.extend(locations)
        
        df_locations = pd.DataFrame(all_locations)
        data = {
            'geoPoints': df_locations["geoPoint"].tolist(),
            'NCTid': df_locations["NCTId"].tolist(),
            'facility': df_locations["facility"].tolist()
        }
        df = pd.DataFrame(data)
        df = df.dropna(subset=['geoPoints'])
        df['facility'].fillna("0", inplace=True)

        if not df.empty:
            center_lat = df['geoPoints'].iloc[0]['lat']
            center_lon = df['geoPoints'].iloc[0]['lon']
            m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

            marker_cluster = plugins.MarkerCluster().add_to(m)
            folium.plugins.Fullscreen(
                position="topright",
                title="Expand me",
                title_cancel="Exit me",
                force_separate_button=True,
            ).add_to(m)
            for _, row in df.iterrows():
                coords = [row['geoPoints']['lat'], row['geoPoints']['lon']]
                tooltip = row['NCTid']
                if row['facility'].isdigit():
                    popup = "Facility Name not Available"
                else:
                    popup = f"NCT ID: {row['NCTid']}\n\nFacility name: {row['facility']}"
                folium.Marker(location=coords, tooltip=tooltip, popup=popup).add_to(marker_cluster)

            folium.LayerControl().add_to(m)

            return m
        else:
            st.error("No valid locations found in the data.")
            return None

    else:
        return None
