import streamlit as st
import pickle


pickle_in = open('pipe.pkl', 'rb')
pipe = pickle.load(pickle_in)
df_pickle_in = open('airline.pkl','rb')
airline_df = pickle.load(df_pickle_in)



st.title("Airline Customer Holiday Booking Prediction :airplane:")

passengers = st.number_input(
    "Enter a number of passengers", min_value=0, max_value=9)
sales = st.selectbox("Sales Channel", ['Internet', 'Mobile'])
trip = st.selectbox("Trip Type", airline_df['trip_type'].unique())
purchase_lead = st.number_input("Purchase Lead", min_value=0)
length_of_stay = st.number_input("Length of Stay", min_value=0)
flight_hour = st.number_input("Flight Hour", min_value=0, max_value=24)
flight_day = st.selectbox("Flight Day",airline_df['flight_day'].unique())


booking_origin = st.selectbox("Booking Origin", airline_df['booking_origin'].unique())

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

    


    query = [[passengers, sales, trip,purchase_lead,
                    length_of_stay, flight_hour, flight_day, booking_origin,
                    baggage, seat, flight_meals,
                    flight_duration]]
    
   
    if pipe.predict(query)[0] == 0:
        st.title("Booking Completed")
    else:
        st.title("Booking Pending")

