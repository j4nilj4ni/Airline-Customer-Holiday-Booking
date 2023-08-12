import streamlit as st
import pickle
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import pandas as pd

def lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


st.set_page_config(page_title="Airline Prediction App",
                   page_icon=":airplane:", layout="wide")


# Navigation
selected = option_menu(
    menu_title=None,
    menu_icon='cast',
    default_index=0,
    options=['Data Description', 'Prediction'],
    icons=['book', 'airplane'],
    orientation='horizontal'

)


# Description
if selected == 'Data Description':
    st.title("Welcome to Airline Customer Holiday Booking :airplane:")
    left_column, right_column = st.columns(2)
    lottie = lottieurl(
        "https://lottie.host/304bce08-fcd6-4211-bb21-0d219bcf66ec/ghvL9pmyOK.json")
    
    with left_column:
        
        st.write(
            "**Unveiling Customer Preferences and Booking Patterns in the Airline Holiday Indus**")
        st.subheader("About Dataset")
        st.write("This dataset provides comprehensive information about customers' preferences and behaviors related to airline holiday bookings. With detailed attributes covering various aspects of the booking process, this dataset is ideal for analyzing and understanding customer choices and patterns in the airline industry.")

        st.write("Potential analyses and applications include:")

        st.write(
            "1. Identifying factors influencing successful holiday bookings and improving conversion rates.")
        st.write("2. Evaluating the impact of different services (e.g., in-flight meals, extra baggage allowance) on customers' booking decisions.")
        st.write(
            "3. Assessing the relationship between booking lead time and customer choices.")
        st.write(
            "4. Analyzing the popularity of various routes and flight schedules.")
        st.write(
            "5. Investigating the influence of booking channels on customer behavior.")
        st.write(
            "6. Predicting the likelihood of a successful holiday booking based on customer characteristics.")
        st.write("7. With its comprehensive range of attributes, this dataset presents an excellent opportunity for data scientists, researchers, and analysts to gain insights into customer behavior within the airline industry.")

    with right_column:
        st_lottie(lottie, height=500, key="airline_booking")

    st.write('---')
    st.subheader("Data Details")
    data = pd.DataFrame([
    {
        'Feature': 'num_passengers',
        'Description': 'The number of passengers associated with each booking'
    },
    {
        'Feature': 'sales_channel',
        'Description': 'How customer reached our website'
    },
    {
        'Feature': 'trip_type',
        'Description': 'Specifies whether the booking is for One Way or Round Trip'
    },
    {
        'Feature': 'purchase_lead',
        'Description': 'The duration between the booking date and the date of travel'
    },
    {
        'Feature': 'lenght_of_stay',
        'Description': 'The duration of the holiday stay'
    },
    {
        'Feature': 'flight_hour',
        'Description': 'Specifies the hour of the flight'
    },
    {
        'Feature': 'flight_day',
        'Description': 'Indicates the day of the week for the flight'
    },
    {
        'Feature': 'booking_origin',
        'Description': 'Describes the source of the booking i.e. Country'
    },
    {
        'Feature': 'extra_baggage',
        'Description': 'Indicates whether the customer expressed a desire for extra baggage allowance'
    },
    {
        'Feature': 'preferred_seat',
        'Description': 'The seat or location that individuals have chosen as their preferred option'
    },
    {
        'Feature': 'flight_meals',
        'Description': 'Indicates whether the customer expressed a desire for a meal during the flight'
    },
    {
        'Feature': 'flight_duration',
        'Description': 'Total duration of the flight'
    },
    {
        'Feature': 'booking_complete',
        'Description': 'Indicates whether the customer successfully booked a holiday or not'
    }
])

    st.table(data)


# Prediction
if selected == 'Prediction':

    pickle_in = open('pipe.pkl', 'rb')
    pipe = pickle.load(pickle_in)
    df_pickle_in = open('airline.pkl', 'rb')
    airline_df = pickle.load(df_pickle_in)

    st.title("Airline Customer Holiday Booking Prediction :airplane:")

    passengers = st.number_input(
        "Enter a number of passengers", min_value=0, max_value=9)
    sales = st.selectbox("Sales Channel", ['Internet', 'Mobile'])
    trip = st.selectbox("Trip Type", airline_df['trip_type'].unique())
    purchase_lead = st.number_input("Purchase Lead", min_value=0)
    length_of_stay = st.number_input("Length of Stay", min_value=0)
    flight_hour = st.number_input("Flight Hour", min_value=0, max_value=24)
    flight_day = st.selectbox("Flight Day", airline_df['flight_day'].unique())

    booking_origin = st.selectbox(
        "Booking Origin", airline_df['booking_origin'].unique())

    baggage = st.selectbox("Want Extra Baggage", ['No', 'Yes'])
    seat = st.selectbox("Want Preferred Seat", ['No', 'Yes'])
    flight_meals = st.selectbox("Flight Meals", ['No', 'Yes'])
    flight_duration = st.number_input(
        "Flight Duration", min_value=4.5, max_value=10.0)

    if st.button('Predict Booking'):

        if sales == 'Internet':
            sales = 0
        else:
            sales = 1

        if baggage == 'Yes':
            baggage = 1
        else:
            baggage = 0

        if seat == 'Yes':
            seat = 1
        else:
            seat = 0

        if flight_meals == 'Yes':
            flight_meals = 1
        else:
            flight_meals = 0

        query = [[passengers, sales, trip, purchase_lead,
                  length_of_stay, flight_hour, flight_day, booking_origin,
                  baggage, seat, flight_meals,
                  flight_duration]]

        if pipe.predict(query)[0] == 0:
            st.success('Booking Completed :white_check_mark:')
        else:
            st.error("Booking Pending :clock330:")
