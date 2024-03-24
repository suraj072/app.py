import streamlit as st
import pandas as pd
import random
from streamlit_folium import folium_static
import folium




sample_data = pd.DataFrame({
    'Grocery': ['Apples', 'Chicken', 'Rice', 'Fish', 'Chocolate'],
    'Emission Factors (kgCO2/kg)': [0.06, 1.82, 0.16, 1.34, 0.95]
})
item_emojis = {
    'Apples': '🍎',
    'Chicken': '🍗',
    'Rice': '🍚',
    'Fish': '🐟',
    'Chocolate': '🍫'
}
def calculate_carbon_footprint(groceries):
    """Calculates the total carbon footprint for the given groceries."""
    total_footprint = 0
    for item, quantity in groceries.items():
        if item in sample_data['Grocery'].values:
            emission_factors = sample_data.loc[sample_data['Grocery'] == item, 'Emission Factors (kgCO2/kg)'].values[0]
            total_footprint += emission_factors * quantity
    return total_footprint

def suggest_adjusted_quantities(groceries, carbon_limit):
    adjusted_quantities = {}
    total_carbon_footprint = calculate_carbon_footprint(groceries)

    if total_carbon_footprint <= carbon_limit:
        return groceries  # No adjustment needed

    # Calculate a reduction factor to proportionally reduce all quantities
    reduction_factor = carbon_limit / total_carbon_footprint

    for item, quantity in groceries.items():
        # Adjust quantity randomly within 90-100% of the original quantity
        adjusted_quantity = max(0, random.uniform(0.9, 1) * quantity * reduction_factor)
        adjusted_quantities[item] = adjusted_quantity

    return adjusted_quantities



def ngo():
    
    ngo_contacts = [
        {
            "name": "Udayan Social Welfare Society",
            "phone": "9957047867",
            "location": "Dharapur",
            "purpose": "Udayan Care aims to bring sunshine into the lives of underserved sections of society that require intervention. Registered in 1994 as a Public Charitable Trust, Udayan Care works to empower vulnerable children, women, and youth, in 36 cities across 15 states of India."
        },
        {
            "name": "Brotherhood NGO",
            "phone": "7638830508",
            "location": "Kahikuchi",
            "purpose": "The Delhi Brotherhood Society (DBS) has arisen from a unique history for a powerful mission. From slum community development, to fighting illegal bonded labor, to working with the children of sex workers, to providing aid for a leprosy colony, and beyond, DBS runs a host of projects in the service of society"
        },
        {
            "name": "Gouri Sevapeeth Mission",
            "phone": "8638625715",
            "location": "Maligoan",
            "purpose": "Gouri Sevapeeth Mission: Established in 1988, Gouri Sevapeeth works in the area of Children, Disability, Disaster Management, Education & Literacy, Health & Nutrition, Labour & Employment, Rural Development & Poverty Alleviation, Urban Development & Poverty Alleviation, Vocational Training, Women’s Development & Empowerment, etc. It also provides nursing training and other women empowerment courses."
        },
        {
            "name": "Shikshalaya NGO",
            "phone": "9577600012",
            "location": "paltan bazar",
            "purpose": "Shikshalaya is an independent, co-educational day boarding school open to students from around the world. They offer a comprehensive and skill-enhancing study program developed under the guidelines of NCERT with a strong emphasis on practical learning for toddlers through senior secondary school students."
        },
    
    ]

    # Map initialization
    m = folium.Map(location=[26.1496, 91.6973], zoom_start=10)

    # Markers for NGOs near Assam Engineering College
    ngo_locations = [
        {"name": "Udayan Social Welfare Society", "location": [26.14324, 91.62424]},
        {"name": "Brotherhood NGO", "location": [26.08403, 91.59044]},
        {"name": "Gouri Sevapeeth Mission", "location": [26.15172, 91.69726]},
        {"name": "Shikshalaya NGO", "location": [26.16186, 91.72817]},
        # Add more NGO locations as needed
    ]


    # Add markers to the map
    for ngo in ngo_locations:
        folium.Marker(location=ngo["location"], popup=ngo["name"]).add_to(m)


    # Streamlit UI
    st.title("NGOs for Waste Management in Guwahati")
    st.markdown("## Map with NGO locations")

    # Render map
    folium_static(m)

    # Display contact information upon clicking markers
    selected_ngo = st.selectbox("Select NGO:", [ngo["name"] for ngo in ngo_locations])

    for ngo in ngo_contacts:
        if ngo["name"] == selected_ngo:
            st.markdown(f"### {ngo['name']}")
            st.write(f"- Phone: {ngo['phone']}")
            st.write(f"- Location: {ngo['location']}")
            st.write(f"- Purpose: {ngo['purpose']}")



    
def display_contact_card(center):
            """Display the contact card for a recycling center."""
            st.subheader(center["name"])
            st.markdown(f"**Address:** {center['address']}")
            st.markdown(f"**Phone:** {center['phone']}")
            st.markdown(f"**Hours:** {center['hours']}")
            st.markdown(f"Website")



def main():
    st.title("Grocery Carbon Footprint Calculator")

   


    # User input: grocery items and quantities
    groceries = {}
    for item in sample_data['Grocery']:
        quantity = st.number_input(f"{item_emojis[item]}Enter quantity of {item} (in kg)", min_value=0.0, value=0.0)
        groceries[item] = quantity

    # Calculate total carbon footprint
    total_carbon_footprint = calculate_carbon_footprint(groceries)

    carbon_limit = 16.515

    # Display results
    if total_carbon_footprint <= carbon_limit:
        st.markdown("#### Your Carbon footprint: " + ":green[" + str(total_carbon_footprint) + "] kgCO2e")
    else:
        st.markdown("#### Your Carbon footprint: " + ":red[" + str(total_carbon_footprint) + "] kgCO2e")

    if total_carbon_footprint > carbon_limit:
        st.warning(
            f"Warning: Carbon footprint limit exceeded! Your current footprint is {total_carbon_footprint:.2f} kgCO2e, exceeding the limit of {carbon_limit} kgCO2e.")

        # Suggest adjusted quantities
        adjusted_quantities = suggest_adjusted_quantities(groceries.copy(), carbon_limit)  # Copy to avoid modifying original dict

        st.subheader("Suggested Adjusted Quantities:")
        for item, quantity in adjusted_quantities.items():
            original_quantity = groceries[item]
            reduction = original_quantity - quantity
            st.write(f"- {item}: Adjusted quantity = {quantity:.2f} kg (originally {original_quantity:.2f} kg, reduction of {reduction:.2f} kg)")

        # Optionally allow user to confirm adjustments
        confirm_adjustment = st.checkbox("Confirm adjusted quantities?")
        if confirm_adjustment:
            groceries = adjusted_quantities
            total_carbon_footprint = calculate_carbon_footprint(groceries)
            st.success(
                f"Adjusted quantities confirmed. Your new total footprint is {total_carbon_footprint:.2f} kgCO2e.")
            
        
        
        #for map
        if 'show_data' not in st.session_state:
            st.session_state.show_data = False  # Initially set to not show data

        clicked = st.button("Show NGO's in Guwahati")

        if clicked:
            st.session_state.show_data = True  # Update state to show data

        if st.session_state.show_data:
            ngo()   
            
            
         
         
         
        # Define the recycling centers
        recycling_centers = [
            {
                "name": "MSTC Limited (Guwahati Branch)",
                "address": "Bsnl Exchange Building, Beltola Basistha Road, Guwahati, Kamrup, Assam 781038",
                "phone": "0361 222 1199",
                "hours": "Monday 09:30 - 18:00, Tuesday 09:30 - 18:00, Wednesday 09:30 - 18:00, Thursday 09:30 - 18:00, Friday 09:30 - 18:00",
                "url": "^2^"
            },
            {
                "name": "Jahidul Iron & Plastic Scrap",
                "address": "Paschim Boragaon, Miliguli Path, Guwahati, Kamrup, Assam 781011",
                "phone": "02641 222 1399",
                "hours": "Monday 09:30 - 18:00, Tuesday 09:30 - 18:00, Wednesday 09:30 - 18:00, Thursday 09:30 - 18:00, Friday 09:30 - 18:00",
                "url": "^2^"
            },
            {
                "name": "Maa Kamakhya Disposal Works Foundation",
                "address": "1 Maa Kamakhya Disposable Works, Bhetamukh Bezera, Kamrup, Assam 781101",
                "phone": "094010 22121",
                "hours": "Monday 09:30 - 18:00, Tuesday 09:30 - 18:00, Wednesday 09:30 - 18:00, Thursday 09:30 - 18:00, Friday 09:30 - 18:00",
                "url": "^2^"
            },
            
                 

        ]  
        
        
        if st.button('Show Recycling Centers'):
                for center in recycling_centers:
                    display_contact_card(center) 
            
        
            
       
            
            
    else:
        st.success(
            f"Wow! Your Carbon Footprint is excellent...   Your current footprint is {total_carbon_footprint:.2f} kgCO2e, which is within the limit of {carbon_limit} kgCO2e.")
        
        
    
   


if __name__ == "__main__":
    main()