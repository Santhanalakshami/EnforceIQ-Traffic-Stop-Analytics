# Import necessary libraries

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from sqlalchemy import create_engine



# Function to create a database connection
def create_connection():
    try:
        # Format: postgresql+psycopg2://user:password@host:port/dbname
        engine = create_engine("postgresql+psycopg2://postgres:Regular20@localhost:5432/postgres")
        return engine
    except Exception as e:
        print(f"Error creating engine: {e}")
        return None

#Fetch data from database

df = pd.read_sql("SELECT * FROM traffic_stops", create_connection())
# Fetch data using pandas and SQLAlchemy
def fetch_data(query):
    engine = create_connection()
    if engine:
        try:
            df = pd.read_sql(query, con=engine)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()  # Return an empty DataFrame if connection fails

#Cleaning Function

def clean_data(df):
    # Drop columns where all values are NaN
    df = df.dropna(axis=1, how='all')

    # Fill missing string fields
    for col in ['driver_gender', 'driver_race', 'country_name', 'violation', 'stop_outcome', 'search_type', 'stop_duration']:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')

    # Fill missing boolean fields
    for col in ['search_conducted', 'drugs_related_stop', 'is_arrested']:
        if col in df.columns:
            df[col] = df[col].fillna(False).astype(bool)

    # Fill missing ages with median and convert to int
    if 'driver_age' in df.columns:
        df['driver_age'] = pd.to_numeric(df['driver_age'], errors='coerce')
        df['driver_age'] = df['driver_age'].fillna(df['driver_age'].median()).astype(int)

    # Format date and time columns
    if 'stop_date' in df.columns:
        df['stop_date'] = pd.to_datetime(df['stop_date'], errors='coerce')
    if 'stop_time' in df.columns:
        df['stop_time'] = pd.to_datetime(df['stop_time'], errors='coerce').dt.time

    return df

# Load data from the database and clean it
raw_df = pd.read_sql("SELECT * FROM traffic_stops", create_connection())
data = clean_data(raw_df)

# stop duration options
durations = data['stop_duration'].dropna().unique().tolist()
durations = sorted(durations) if durations else ["0-15 Min", "16-30 Min", "30+ Min"]
    
#Streamlit app
st.set_page_config(page_title="Traffic Stops Analysis", layout="wide")  # sets browser tab title

st.title(":red[🚓 EnforceIQ:Traffic Stops Analytics]")  # visible title

st.markdown("---")

#diplay full table
st.header("📒Police Logs Overview")  # subheader
query = "SELECT * FROM traffic_stops"
data = fetch_data(query)
st.dataframe(data, use_container_width=True)  # display the dataframe in the app

st.markdown("---")

st.header("📈 Key Metrics")  # subheader for statistics
col1,col2,col3,col4,col5= st.columns(5)  # create 4 columns for layout

with col1:
    total_stops = data.shape[0]  # total number of stops
    st.metric(label="🚦 Total Stops", value=total_stops)  # display total stops
with col2:
    arrest= data[data['is_arrested'] == True].shape[0]  # total arrests
    st.metric(label="🚨 Total Arrests", value=arrest)  # display total arrests
with col3:
    stop_outcomes = data['stop_outcome'].nunique()  # unique stop outcomes
    st.metric(label="📗 Unique Outcomes", value=stop_outcomes)  # display unique outcomes
with col4:
    violation_types = data['violation'].nunique()  # unique violation types
    st.metric(label="⚠️ Violation Types", value=violation_types)  # display unique violations
with col5:
    stop_outcomes = data['stop_outcome'].value_counts().idxmax()  # most common stop outcome
    st.metric(label="🏆 Top Outcome", value=stop_outcomes)  # display most common outcome

st.header("📊 Visual insights of Key Metrics")  # subtitle

total_stops = data.shape[0]
total_arrests = data[data['is_arrested'] == True].shape[0]
unique_outcomes = data['stop_outcome'].nunique()
unique_violations = data['violation'].nunique()
most_common_outcome = data['stop_outcome'].value_counts().idxmax()

# Create summary DataFrame
summary_df = pd.DataFrame({
    'Category': ['Total Stops', 'Total Arrests'],
    'Count': [total_stops, total_arrests]
})

# Violation counts for pie chart
violation_counts = data['violation'].value_counts().reset_index()
violation_counts.columns = ['Violation', 'Count']

# Create three tabs for the dashboard

tab1, tab2, tab3 = st.tabs([
    "📊 Demographic Distribution",
    "🚓 Traffic Stop Summary",
    "📛 Violation Distribution"
])

# --- TAB 1: Demographics (Now First) ---
with tab1:
    data['stop_date'] = pd.to_datetime(data['stop_date'])  # Ensure stop_date is datetime
    data['year'] = data['stop_date'].dt.year               # Extract year

    # Group by multiple categories
    demo_df = (
        data
        .groupby(['driver_gender', 'year', 'country_name', 'stop_outcome'])
        .size()
        .reset_index(name='count')
    )

    fig1 = px.bar(
        demo_df,
        x='year',
        y='count',
        color='stop_outcome',
        barmode='group',
        facet_col='driver_gender',
        facet_row='country_name',
        title='📊 Traffic Stop Outcomes by Gender, Year, and Country',
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    fig1.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of Stops',
        title_x=0.3,
        height=800
    )

    st.plotly_chart(fig1, use_container_width=True)

# --- TAB 2: Traffic Stop Summary (Bar Chart) ---
with tab2:
    fig2 = px.bar(
        summary_df, x='Category', y='Count',
        color='Category', text='Count',
        title='🚓 Summary of Traffic Stops Metrics',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig2.update_layout(title_x=0.3)
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 3: Violation Distribution (Pie Chart) ---
with tab3:
    fig3 = px.pie(
        violation_counts, names='Violation', values='Count',
        title='📛 Violation Distribution',
        color_discrete_sequence=px.colors.sequential.Greens
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")


# Show most common outcome
st.markdown(f"✅ **Most Common Stop Outcome:** `{most_common_outcome}`")

st.markdown("---")

#Query for Complete Data
st.header("📁 Detailed Records of Traffic Stops")  # subheader for detailed analysis

st.header("🔍 Medium Queries")  # subheader for simple queries

selected_query = st.selectbox(
    "Select a Query to run:",
    [
        "1. 🚘 Vehicle_Number involved in drug-related stops",
        "2. Most frequently searched vechicles",
        "3. Which driver age group had the highest arrest rate?",
        "4. Gender distribution of drivers stopped in each country",
        "5. Which race and gender combination has the highest search rate ?",
        "6. What time of day sees the most traffic stops?",
        "7. Average stop duration for different violations?",
        "8. Are stops during the night more likely to lead to arrests?",
        "9. Which violations are most associated with searches or arrests?",
        "10. Violations that are most common among younger drivers <25",
        "11. A violation that rarely results in search or arrest",
        "12. Which countries report the highest rate of drug-related stops?",
        "13. The arrest rate by country and violation",
        "14. Which country has the most stops with search conducted?"

    ])
query_map = {
    "1. 🚘 Vehicle_Number involved in drug-related stops":"select vehicle_number, drugs_related_stop  from traffic_stops where drugs_related_stop = true limit 10",
    
    "2. Most frequently searched vechicles":"select vehicle_number, count(*) as search_count from traffic_stops where search_conducted = true group by vehicle_number order by search_count desc limit 1",
    
    "3. Which driver age group had the highest arrest rate?": """
    select 
     case
    when driver_age < 18 then 'under18'
    when driver_age <= 25 then '18-25'
    when driver_age <= 35 then '26-35'
    when driver_age <= 50 then '36-50'
    when driver_age <= 65 then '51-65'
    else '65+'
  end as Age_group,
  driver_age, avg(case when is_arrested=true then 1 else 0 end) as rate_of_arrest
 from traffic_stops 
 group by driver_age 
 order by rate_of_arrest desc limit 1""",
   
    "4. Gender distribution of drivers stopped in each country": """select country_name,driver_gender,count(*) as stop_counts from traffic_stops where search_conducted = true
group by country_name, driver_gender order by country_name, stop_counts desc""",
    
    "5. Which race and gender combination has the highest search rate ?": """select driver_gender,driver_race,count(*) as stop_counts from traffic_stops where search_conducted=true group by driver_gender,driver_race
order by stop_counts desc limit 1""",
   
    "6. What time of day sees the most traffic stops?": """select 
 case 
  when extract(hour from stop_time) between 5 and 11 then 'Morning' 
  when extract(hour from stop_time) between 12 and 16 then 'Noon'
  when extract(hour from stop_time) between 17 and 20 then 'Evening'
  else 'Night'
end as time_of_day,
count(*) as stop_counts from traffic_stops where stop_time is not null group by time_of_day order by stop_counts desc limit 1;
""",
    
    "7. Average stop duration for different violations?":"""select violation,avg( case stop_duration
      when '0-15 Min' then 7.5
      when '16-30 Min' then 23
      when '30+ Min' then 35
    end
  ) as avg_stop_duration_min from traffic_stops where stop_duration is not null group by violation order by avg_stop_duration_min desc""",
    
    "8. Are stops during the night more likely to lead to arrests?": """select case when stop_time between '22:00:00' and '23:59:59' or stop_time between '00:00:00' and '05:00:00' then 'Night' else 'Day'
end as time_of_day,(cast(sum(case when stop_outcome = 'Arrest' then 1 else 0 end) as numeric) / count(*)) * 100 as arrest_percentage
from traffic_stops group by time_of_day order by time_of_day""",
   
    "9. Which violations are most associated with searches or arrests?": """select violation,count(*) as stop_counts,
(cast(sum(case when search_conducted=true or stop_outcome='Arrest' then 1 else 0 end) as numeric) / count(*)) * 100 as search_or_arrest_percent
from traffic_stops group by violation order by search_or_arrest_percent desc""",

    "10. Violations that are most common among younger drivers <25": "select violation,count(*) as common_violation_count from traffic_stops where driver_age <25 group by violation order by common_violation_count",

    "11. A violation that rarely results in search or arrest": """select violation,count(*) as stop_counts,
(cast(sum(case when search_conducted=true or stop_outcome='Arrest' then 1 else 0 end) as numeric) / count(*)) * 100 as search_or_arrest_percent
from traffic_stops group by violation order by search_or_arrest_percent asc limit 1""",
    
    "12. Which countries report the highest rate of drug-related stops?":"""select country_name,count(*) as stop_counts from traffic_stops where drugs_related_stop= true
group by country_name order by stop_counts desc""",
    
    "13. The arrest rate by country and violation": """select country_name,violation, cast(sum(case when stop_outcome='Arrest' then 1 else 0 end)as numeric) / count(*) * 100 as arrest_percentage
from traffic_stops group by violation,country_name order by arrest_percentage desc""",
   
    "14. Which country has the most stops with search conducted?":"""select country_name,count(*) as stop_counts from traffic_stops where search_conducted=true
group by country_name order by stop_counts desc limit 1"""
}
  #Show the query code with syntax highlighting
st.subheader("SQL Query Used")
st.code(query_map[selected_query], language='sql')  
if st.button("Execute Query"):
    st.snow()
    st.toast("✅ Query Executed Successfully!", icon="🎯")
    result=fetch_data(query_map[selected_query])
    if not result.empty:
        st.write(result)
    else:
        st.write("No data found for the selected query.")

st.header("📒 Complex Queries")  # subheader for advanced queries

selected_query = st.selectbox(
    "Select a Complex Query to run:",
    [

        "1. Yearly Breakdown of Stops and Arrests by Country",
        "2. Driver Violation Trends Based on Age and Race",
        "3. Time Period Analysis of Stops & Number of Stops by Year,Month, Hour of the Day",
        "4. Violations with High Search and Arrest Rates",
        "5. Driver Demographics by Country (Age, Gender and Race)",
        "6. Top 5 Violations with Highest Arrest Rates",

    ])
query_map ={
 
    "1. Yearly Breakdown of Stops and Arrests by Country": """SELECT
    stop_year,
    country_name,
    total_stops,
    total_arrests,
    -- Calculate the percentage of stops that resulted in an arrest for each country per year
    (CAST(total_arrests AS NUMERIC) * 100 / total_stops) AS arrest_rate_percent_yearly,
    -- Calculate a running total of stops per year, ordered by country name
    SUM(total_stops) OVER (PARTITION BY country_name ORDER BY stop_year) AS running_total_stops_per_year,
	SUM(total_arrests) OVER (PARTITION BY country_name ORDER BY stop_year) AS running_total_arrests_per_year
FROM
    (
        -- Subquery to get base yearly and country aggregates
        SELECT
            EXTRACT(YEAR FROM stop_date) AS stop_year,
            country_name,
            COUNT(*) AS total_stops,
            SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests
        FROM
            traffic_stops
        WHERE
            stop_date IS NOT NULL
        
        GROUP BY
            stop_year,
            country_name
    ) AS yearly_country_summary -- Alias for the subquery
ORDER BY
    stop_year ASC,
    country_name ASC;
""",
    
    "2. Driver Violation Trends Based on Age and Race":"""select
    t.driver_age,
    t.driver_race,
    t.violation,
    count(*) as violation_count,
    (cast(count(*) as numeric) * 100 / age_race_totals.total_stops_for_group) as percentage_of_group_stops
from
    traffic_stops as t
join (
    select
        driver_age,
        driver_race,
        count(*) as total_stops_for_group
    from
        traffic_stops
    where
        driver_age is not null
        and driver_race is not null
    group by
        driver_age,
        driver_race
) as age_race_totals
on
    t.driver_age = age_race_totals.driver_age
    and t.driver_race = age_race_totals.driver_race
where
    t.driver_age is not null
    and t.driver_race is not null
    and t.violation is not null
group by
    t.driver_age,
    t.driver_race,
    t.violation,
    age_race_totals.total_stops_for_group
order by
    t.driver_age asc,
    t.driver_race asc,
    percentage_of_group_stops desc""",
    
    "3. Time Period Analysis of Stops & Number of Stops by Year,Month, Hour of the Day":""" select 
    extract(year from stop_date) as stop_year,
    to_char(stop_date, 'Month') as stop_month_name,
    extract(month from stop_date) as stop_month,
    extract(hour from stop_time::time) as stop_hour,
    count(*) as total_stops
from 
    traffic_stops
where 
    stop_date is not null and stop_time is not null
group by 
    stop_year, stop_month_name, stop_month, stop_hour
order by 
    stop_year, stop_month, stop_hour""",

"4. Violations with High Search and Arrest Rates": """select
    violation,
    total_stops,
    stops_with_search,
    percentage_searched,
    stops_with_arrest,
    percentage_arrested,
    dense_rank() over (order by percentage_searched desc) as search_rate_rank,
    dense_rank() over (order by percentage_arrested desc) as arrest_rate_rank
from
    (
        select
            violation,
            count(*) as total_stops,
            count(*) filter (where search_conducted = true) as stops_with_search,
            (count(*) filter (where search_conducted = true)::numeric * 100 / count(*)) as percentage_searched,
            count(*) filter (where is_arrested = true) as stops_with_arrest,
            (count(*) filter (where is_arrested = true)::numeric * 100 / count(*)) as percentage_arrested
        from
            traffic_stops
        where
            violation is not null
        group by
            violation
    ) as violation_stats
where
    total_stops > 0
order by
    percentage_searched desc,
    percentage_arrested desc;""",
    
    "5. Driver Demographics by Country (Age, Gender and Race)": """select country_name,driver_age,driver_gender,driver_race,count(*)as stop_counts from traffic_stops
group by country_name,driver_age,driver_gender,driver_race order by country_name, stop_counts desc""",
    
    "6. Top 5 Violations with Highest Arrest Rates": """select violation, cast(sum(case when stop_outcome='Arrest' then 1 else 0 end)as numeric) / count(*) * 100 as arrest_percentage
from traffic_stops group by violation order by arrest_percentage desc""" }

#Show the query code with syntax highlighting
st.subheader("SQL Query Used")
st.code(query_map[selected_query], language='sql')
if st.button("Run Query"):
    st.snow()
    st.toast("✅ Query Executed Successfully!", icon="🎯")
    result=fetch_data(query_map[selected_query])
    if not result.empty:
        st.write(result)
    else:
        st.write("No data found for the selected query.")





st.markdown("---")
st.markdown("Built with ❤️ by EnforceIQ Team for Law Enforcement")
st.header("🔍Custom Natural Language Filter") 

st.markdown("📝 Fill in the form below to auto predict the stop outcome based on the existing data")
st.header("📝 Add new Police 👮 Log & Predict Stop Outcome and Violation 🚫🛑")

#input form for all fields
with st.form("🚦traffic_stop_form🚦"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time", step=60)
    country_name = st.text_input("Country Name")
    driver_gender = st.selectbox("Driver Gender",["M", "F"])
    driver_age = st.number_input("Driver Age", min_value=0, max_value=120, value=30)
    driver_race = st.text_input("Driver Race")
    search_conducted = st.selectbox("Was a Search Conducted", ["0", "1"])
    search_type = st.text_input("Search Type")
    drugs_related_stop = st.selectbox("Was it Drug Related Stop", ["0", "1"])
    stop_duration = st.selectbox("Stop Duration", ["0-15 Min", "16-30 Min", "30+ Min"])
    vechicle_number = st.text_input("Vehicle Number")
    timestamp= pd.Timestamp.now() # current timestamp
    submitted = st.form_submit_button("Predict Traffic🚦Stop Outcome and Violation🛑🚫")

if submitted:
    filtered_data = data[
        (data['driver_gender'] == driver_gender) &
        (data['driver_age'] == driver_age) &
        (data['search_conducted'] == int(search_conducted)) &
        (data['drugs_related_stop'] == int(drugs_related_stop)) &
        (data['stop_duration'] == stop_duration)
    ]

    st.write("Matching rows found:", len(filtered_data))
    st.dataframe(filtered_data.head())  # Preview matched data

    # Predict the Stop Outcome
    if not filtered_data.empty:
        predicted_outcome = filtered_data['stop_outcome'].mode()[0]
        predicted_violation = filtered_data['violation'].mode()[0]
    else:
        predicted_outcome = "warning"
        predicted_violation = "speeding"

# ✅ Convert gender code to full text
    gender_call = "Male" if driver_gender == "M" else "Female"

    # Natural Language Summary
    search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
    drug_text = "was drug related" if int(drugs_related_stop) else "was not drug related"

    st.markdown(f"""
        ### 🚦 Prediction Summary:
        - **Predicted Violation:** {predicted_violation}
        - **Predicted Stop Outcome:** {predicted_outcome}
        
        A {driver_age}-year-old {gender_call} driver in {country_name} was stopped at {stop_time.strftime('%I:%M %p')} on {stop_date} 
        {search_text} and the stop {drug_text}.
        Stop Duration: **{stop_duration}**
        - **Vehicle Number:** {vechicle_number}
    """)

   

#Final Touches
st.markdown("---")
# Display an image and a header
st.header("👮‍♂️🚓 EnforceIQ: Your Partner in Traffic Safety 🚦")
st.image("https://www.bnpppolice.ca/fr/assets/images/policashakinghand.gif",width=600)

st.markdown("---")

st.title("👮🚙Officer on Duty⏹️🛑🚫 Drive Safe🚘 Save Lives ❤️")

