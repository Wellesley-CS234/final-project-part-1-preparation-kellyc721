import streamlit as st
import pandas as pd
1
# Title
st.title("Climate Change Engagement in the United States during Summers 2023-2025")
st.markdown("---")

# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st10_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:
    df = st.session_state['student_data']['st10_df']
    
    # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
        **Data Description:** This dataset contains **Wikipedia pageview data of climate change-related articles** in the United States during Summers 2023, 2024, and 2025, which have experienced heat waves and are recorded as the three hottest summers in the US. 
        
        **Question:** How have the **three hottest summers** in the US (Summers 2023, 2024, 2025) impacted **climate change (CC) interest**?
         
        **Interaction:** Use the selection box below to choose a specific year and view the CC Wikipedia engagement as measured by pageview metrics for that summer.
    """)
    st.markdown("---")
    
    # --- Analysis Controls (Moved from Sidebar to Main Page) ---
    selected_year = st.selectbox(
        "Select Summer Year",
        options = ["All Years"] + list(sorted(df["year"].unique()))
    )   

    if selected_year == "All Years":
        df_summer = df
    else:
        df_summer = df[df["year"] == selected_year]

    #Streamlit-native line chart 
    if df_summer.empty:
        st.info(f"No pageview data found for the selected year to analyze.")
    else:
        st.subheader(f"CC Engagement by Wikipedia Pageviews")

        col1, col2 = st.columns(2)

        #Summer pageview counts
        total_views = df_summer.groupby('month')["views"].sum()
        with col1:
            if selected_year == "All Years":
                st.metric(
                    label="Total Pageviews Analyzed for Summers 2023-2025", 
                    value=total_views.sum()
                )
            else:
                st.metric(
                    label=f"Total Pageviews Analyzed for Summer {selected_year}", 
                    value=total_views.sum()
                )
            st.dataframe(total_views.to_frame(), use_container_width=True)
        #Average Daily Views Line Chart
        with col2:
            avg_views = df_summer["views"].mean()
            st.metric(
                label="Average Daily Pageviews", 
                value=f"{avg_views:,.0f}"
            )
        #prepare data 
        df_summer["month_day"] = pd.to_datetime(df_summer["date"]).dt.strftime("%m-%d")
        if selected_year == "All Years":
            chart_data = df_summer.pivot(
            index="month_day",
            columns="year",
            values="views"
            )
            st.line_chart(chart_data, height=400, width='stretch')
        else:
            chart_data = (
            df_summer
            .set_index("month_day")["views"]
            .rename(str(selected_year))
            )
            st.subheader(f"Daily Pageviews Trend for Summer {selected_year}")
            st.line_chart(chart_data, height=400, width='stretch')
