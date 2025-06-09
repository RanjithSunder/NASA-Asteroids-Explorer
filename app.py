import streamlit as st
import pandas as pd
import mysql.connector
from datetime import date
import plotly.express as px

# ====== PAGE SETUP ======
st.set_page_config(
    page_title="NASA Asteroids App",
    page_icon="🚀",
    layout="wide"
)

# ====== SIMPLE STYLING ======
st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .metric-box {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ====== DATABASE CONNECTION ======
def connect_to_database():
    """Connect to MySQL database - change these settings for your database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Your database host
            user="vmfg",  # Your username
            password="vmfgpwd!",  # Your password
            database="nasa"  # Your database name
        )
        return connection
    except Exception as e:
        st.error(f"Cannot connect to database: {e}")
        return None


# ====== MAIN APP TITLE ======
st.markdown('<h1 class="big-title">🚀 NASA Asteroids Explorer</h1>', unsafe_allow_html=True)

# ====== SIDEBAR MENU ======
st.sidebar.title("📋 Menu")
page_choice = st.sidebar.selectbox(
    "What would you like to explore?",
    [
        "📊 Dashboard",
        "🔍 Quick Queries",
        "🎯 Custom Search",
        "📈 Charts"
    ]
)

# ====== PAGE 1: DASHBOARD ======
if page_choice == "📊 Dashboard":
    st.header("📊 Dashboard Overview")

    # Get basic statistics from database
    conn = connect_to_database()
    if conn:
        try:
            # Create 4 columns for metrics
            col1, col2, col3, col4 = st.columns(4)

            cursor = conn.cursor()

            # Count total asteroids
            cursor.execute("SELECT COUNT(*) FROM asteroids")
            total_asteroids = cursor.fetchone()[0]

            # Count total approaches
            cursor.execute("SELECT COUNT(*) FROM close_approaches")
            total_approaches = cursor.fetchone()[0]

            # Count dangerous asteroids
            cursor.execute("SELECT COUNT(*) FROM asteroids WHERE is_potentially_hazardous_asteroid = TRUE")
            dangerous_count = cursor.fetchone()[0]

            # Find fastest speed
            cursor.execute("SELECT MAX(relative_velocity_kmph) FROM close_approaches")
            max_speed = cursor.fetchone()[0]

            # Display metrics in boxes
            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <h3>🪨 Asteroids</h3>
                    <h2>{total_asteroids:,}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <h3>🎯 Approaches</h3>
                    <h2>{total_approaches:,}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <h3>⚠️ Dangerous</h3>
                    <h2>{dangerous_count:,}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-box">
                    <h3>🚀 Max Speed</h3>
                    <h2>{max_speed:,.0f} km/h</h2>
                </div>
                """, unsafe_allow_html=True)

            cursor.close()
            conn.close()

        except Exception as e:
            st.error(f"Error getting data: {e}")

    # Information section
    st.markdown("""
    <div class="info-box">
        <h3>🌟 About This App</h3>
        <p>This app helps you explore NASA's asteroid database. You can:</p>
        <ul>
            <li>📊 View basic statistics about asteroids</li>
            <li>🔍 Run pre-made queries to find interesting data</li>
            <li>🎯 Create custom searches with filters</li>
            <li>📈 See charts and visualizations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ====== PAGE 2: QUICK QUERIES ======
elif page_choice == "🔍 Quick Queries":
    st.header("🔍 Quick Queries")
    st.write("Choose from these pre-made queries to explore the data:")

    # Simple dictionary of queries
    easy_queries = {
    "🔢 Count how many times each asteroid has approached Earth": {
        "query": """SELECT neo_reference_id, COUNT(*) AS approach_count
                    FROM close_approaches
                    WHERE orbiting_body = 'Earth'
                    GROUP BY neo_reference_id
                    ORDER BY approach_count DESC;""",
        "description": "Shows how frequently each asteroid has approached Earth"
    },

    "⚡ Average velocity of each asteroid over multiple approaches": {
        "query": """SELECT neo_reference_id, AVG(relative_velocity_kmph) AS avg_velocity_kmph
                    FROM close_approaches
                    GROUP BY neo_reference_id
                    ORDER BY avg_velocity_kmph DESC;""",
        "description": "Average speed of asteroids across all their recorded approaches"
    },

    "🚀 Top 10 fastest asteroids (based on max velocity)": {
        "query": """SELECT neo_reference_id, MAX(relative_velocity_kmph) AS max_velocity_kmph
                    FROM close_approaches
                    GROUP BY neo_reference_id
                    ORDER BY max_velocity_kmph DESC
                    LIMIT 10;""",
        "description": "The fastest recorded asteroid speeds in our database"
    },

    "⚠️ Potentially hazardous asteroids (>3 Earth approaches)": {
        "query": """SELECT a.id, a.name, COUNT(ap.neo_reference_id) AS approach_count
                    FROM asteroids a
                    JOIN close_approaches ap ON a.id = ap.neo_reference_id
                    WHERE a.is_potentially_hazardous_asteroid = TRUE
                      AND ap.orbiting_body = 'Earth' 
                    GROUP BY a.id, a.name 
                    HAVING approach_count > 3
                    ORDER BY approach_count DESC;""",
        "description": "Dangerous asteroids that have approached Earth multiple times"
    },

    "📅 Month with the most asteroid approaches": {
        "query": """SELECT MONTH(close_approach_date) AS month, COUNT(*) AS approach_count
                    FROM close_approaches
                    GROUP BY month
                    ORDER BY approach_count DESC;""",
        "description": "Seasonal patterns in asteroid approaches"
    },

    "🥇 Asteroid with the fastest ever approach speed": {
        "query": """SELECT neo_reference_id, relative_velocity_kmph AS max_velocity
                    FROM close_approaches
                    WHERE relative_velocity_kmph = (
                        SELECT MAX(relative_velocity_kmph)
                        FROM close_approaches
                    )
                    LIMIT 1;""",
        "description": "The single fastest asteroid approach on record"
    },

    "📏 Asteroids sorted by maximum estimated diameter": {
        "query": """SELECT id, name, estimated_diameter_max_km
                    FROM asteroids
                    ORDER BY estimated_diameter_max_km DESC
                    LIMIT 20;""",
        "description": "Largest asteroids by estimated maximum diameter"
    },

    "🎯 Each asteroid's closest approach to Earth": {
        "query": """SELECT a.name, ap.close_approach_date, ap.miss_distance_km
                    FROM asteroids a
                    JOIN close_approaches ap ON a.id = ap.neo_reference_id
                    JOIN (
                        SELECT neo_reference_id, MIN(miss_distance_km) AS min_miss_distance
                        FROM close_approaches
                        WHERE orbiting_body = 'Earth'
                        GROUP BY neo_reference_id
                    ) min_dist ON ap.neo_reference_id = min_dist.neo_reference_id
                               AND ap.miss_distance_km = min_dist.min_miss_distance
                    WHERE ap.orbiting_body = 'Earth'
                    ORDER BY ap.miss_distance_km ASC;""",
        "description": "The closest each asteroid has ever come to Earth"
    },

    "💨 High-speed asteroids (>50,000 km/h near Earth)": {
        "query": """SELECT DISTINCT a.name, MAX(ap.relative_velocity_kmph) as max_velocity
                    FROM asteroids a
                    JOIN close_approaches ap ON a.id = ap.neo_reference_id
                    WHERE ap.relative_velocity_kmph > 50000
                      AND ap.orbiting_body = 'Earth'
                    GROUP BY a.name
                    ORDER BY max_velocity DESC;""",
        "description": "Asteroids that approached Earth at extreme speeds"
    },

    "📊 Monthly approach statistics": {
        "query": """SELECT YEAR(close_approach_date) AS year, 
                           MONTH(close_approach_date) AS month, 
                           COUNT(*) AS approach_count
                    FROM close_approaches
                    GROUP BY year, month
                    ORDER BY year DESC, month;""",
        "description": "Approach frequency by year and month"
    },

    "🌟 Brightest asteroid (lowest magnitude)": {
        "query": """SELECT id, name, absolute_magnitude_h
                    FROM asteroids
                    ORDER BY absolute_magnitude_h ASC
                    LIMIT 10;""",
        "description": "Asteroids with the highest brightness (lowest magnitude values)"
    },

    "⚖️ Hazardous vs Non-hazardous asteroid count": {
        "query": """SELECT 
                        CASE 
                            WHEN is_potentially_hazardous_asteroid = 1 THEN 'Potentially Hazardous'
                            ELSE 'Not Hazardous'
                        END as hazard_status,
                        COUNT(*) AS count
                    FROM asteroids
                    GROUP BY is_potentially_hazardous_asteroid;""",
        "description": "Distribution of potentially hazardous vs safe asteroids"
    },

    "🌙 Asteroids closer than the Moon (<1 LD)": {
        "query": """SELECT a.name, ap.close_approach_date, ap.miss_distance_lunar
                    FROM asteroids a
                    JOIN close_approaches ap ON a.id = ap.neo_reference_id
                    WHERE ap.miss_distance_lunar < 1
                      AND ap.orbiting_body = 'Earth'
                    ORDER BY ap.miss_distance_lunar ASC;""",
        "description": "Asteroids that passed closer to Earth than the Moon's distance"
    },

    "🪐 Very close approaches (<0.05 AU)": {
        "query": """SELECT a.name, ap.close_approach_date, ap.astronomical_au
                    FROM asteroids a
                    JOIN close_approaches ap ON a.id = ap.neo_reference_id
                    WHERE ap.astronomical_au < 0.05
                      AND ap.orbiting_body = 'Earth'
                    ORDER BY ap.astronomical_au ASC;""",
        "description": "Asteroids within 0.05 Astronomical Units of Earth"
    },

    "📈 Long-term tracked asteroids (>1 year span)": {
        "query": """SELECT neo_reference_id, 
                           MIN(close_approach_date) AS first_approach, 
                           MAX(close_approach_date) AS last_approach,
                           DATEDIFF(MAX(close_approach_date), MIN(close_approach_date)) AS days_between
                    FROM close_approaches
                    GROUP BY neo_reference_id
                    HAVING days_between > 365
                    ORDER BY days_between DESC;""",
        "description": "Asteroids tracked over extended periods (more than 1 year)"
    },

    "📈 Monthly averages (distance & velocity)": {
        "query": """SELECT MONTH(close_approach_date) AS month, 
                           AVG(miss_distance_km) AS avg_miss_distance_km, 
                           AVG(relative_velocity_kmph) AS avg_velocity_kmph,
                           COUNT(*) as total_approaches
                    FROM close_approaches
                    GROUP BY month
                    ORDER BY month;""",
        "description": "Average miss distance and velocity by month of the year"
    },

    "🏔️ Large asteroids near Earth (>1 km diameter)": {
        "query": """SELECT DISTINCT a.id, a.name, a.estimated_diameter_max_km
                    FROM asteroids a
                    JOIN close_approaches ap ON a.id = ap.neo_reference_id
                    WHERE a.estimated_diameter_max_km > 1
                      AND ap.orbiting_body = 'Earth'
                    ORDER BY a.estimated_diameter_max_km DESC;""",
        "description": "Large asteroids (over 1km) that have approached Earth"
    },

    "🆕 Recent approaches (last 60 days)": {
        "query": """SELECT a.name, ap.close_approach_date, ap.miss_distance_km, ap.relative_velocity_kmph
                    FROM close_approaches ap
                    JOIN asteroids a ON ap.neo_reference_id = a.id
                    WHERE ap.close_approach_date >= CURDATE() - INTERVAL 60 DAY
                      AND ap.orbiting_body = 'Earth'
                    ORDER BY ap.close_approach_date DESC;""",
        "description": "Most recent asteroid approaches to Earth"
    },

    "📅 Weekend approaches (Sat/Sun)": {
        "query": """SELECT a.name, ap.close_approach_date, ap.miss_distance_km,
                           DAYNAME(ap.close_approach_date) as day_of_week
                    FROM close_approaches ap
                    JOIN asteroids a ON ap.neo_reference_id = a.id
                    WHERE DAYOFWEEK(ap.close_approach_date) IN (1,7)
                      AND ap.orbiting_body = 'Earth'
                    ORDER BY ap.close_approach_date DESC;""",
        "description": "Asteroid approaches that occurred on weekends"
    },

    "📐 Largest diameter uncertainty range": {
        "query": """SELECT id, name, 
                           estimated_diameter_min_km,
                           estimated_diameter_max_km,
                           (estimated_diameter_max_km - estimated_diameter_min_km) AS diameter_range
                    FROM asteroids
                    ORDER BY diameter_range DESC
                    LIMIT 10;""",
        "description": "Asteroids with the largest uncertainty in size estimates"
    },

    "🔄 Multiple approaches same day": {
        "query": """SELECT neo_reference_id, close_approach_date, COUNT(*) AS approaches_per_day
                    FROM close_approaches
                    GROUP BY neo_reference_id, close_approach_date
                    HAVING approaches_per_day > 1
                    ORDER BY approaches_per_day DESC;""",
        "description": "Asteroids with multiple recorded approaches on the same day"
    }
}

    # Let user pick a query
    selected_query = st.selectbox("Pick a query:", list(easy_queries.keys()))

    if selected_query:
        query_info = easy_queries[selected_query]

        # Show info about the query
        st.markdown(f"""
        <div class="info-box">
            <h4>{selected_query}</h4>
            <p>{query_info['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Run query button
        if st.button("🚀 Run Query"):
            conn = connect_to_database()
            if conn:
                try:
                    # Execute the SQL query
                    df = pd.read_sql(query_info['query'], conn)

                    if len(df) > 0:
                        st.success(f"Found {len(df)} results!")
                        st.dataframe(df, use_container_width=True)

                        # Download button
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download Results",
                            csv,
                            f"{selected_query.replace(' ', '_')}.csv"
                        )
                    else:
                        st.warning("No results found!")

                    conn.close()

                except Exception as e:
                    st.error(f"Query failed: {e}")

# ====== PAGE 3: CUSTOM SEARCH ======
elif page_choice == "🎯 Custom Search":
    st.header("🎯 Custom Search")
    st.write("Create your own search using these comprehensive filters:")

    # Organize filters in a nice layout
    st.markdown("### 🔧 Filter Settings")

    # Create three columns for better organization
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📅 **Date & Time**")
        start_date = st.date_input("From Date:", date(2024, 1, 1))
        end_date = st.date_input("To Date:", date(2024, 12, 31))

        st.markdown("#### ⚡ **Velocity Range**")
        velocity_range = st.slider(
            "Relative Velocity (km/h):",
            0, 200000, (0, 100000),
            step=1000,
            help="Speed of asteroid relative to Earth"
        )

    with col2:
        st.markdown("#### 🌌 **Distance Filters**")
        au_range = st.slider(
            "Astronomical Units (AU):",
            0.0, 1.0, (0.0, 0.1),
            step=0.001,
            help="1 AU = distance from Earth to Sun (~150M km)"
        )

        lunar_range = st.slider(
            "Lunar Distance (LD):",
            0.0, 20.0, (0.0, 5.0),
            step=0.1,
            help="1 LD = distance from Earth to Moon (~384,400 km)"
        )

    with col3:
        st.markdown("#### 📏 **Size Filters**")
        diameter_min = st.slider(
            "Minimum Diameter (km):",
            0.0, 5.0, 0.0,
            step=0.01,
            help="Smallest estimated diameter"
        )

        diameter_max = st.slider(
            "Maximum Diameter (km):",
            0.0, 5.0, 2.0,
            step=0.01,
            help="Largest estimated diameter"
        )

        st.markdown("#### ⚠️ **Hazard Level**")
        hazard_filter = st.selectbox(
            "Potentially Hazardous:",
            ["All Asteroids", "Only Dangerous", "Only Safe"],
            help="NASA classification based on size and orbit"
        )

    # Add a separator
    st.markdown("---")

    # Search button with better styling
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        search_button = st.button("🔍 **Search Asteroids**", use_container_width=True)

    # Execute search
    if search_button:
        conn = connect_to_database()
        if conn:
            try:
                # Build comprehensive query
                base_query = """
                SELECT DISTINCT
                    a.name as asteroid_name,
                    ap.close_approach_date,
                    ap.relative_velocity_kmph,
                    ap.astronomical_au,
                    ap.miss_distance_lunar,
                    a.estimated_diameter_min_km,
                    a.estimated_diameter_max_km,
                    CASE 
                        WHEN a.is_potentially_hazardous_asteroid = 1 THEN 'Yes' 
                        ELSE 'No' 
                    END as is_hazardous
                FROM asteroids a 
                JOIN close_approaches ap ON a.id = ap.neo_reference_id
                WHERE ap.close_approach_date BETWEEN %s AND %s
                AND ap.relative_velocity_kmph BETWEEN %s AND %s
                AND ap.astronomical_au BETWEEN %s AND %s
                AND ap.miss_distance_lunar BETWEEN %s AND %s
                AND a.estimated_diameter_min_km >= %s
                AND a.estimated_diameter_max_km <= %s
                """

                # Prepare parameters
                params = [
                    start_date, end_date,
                    velocity_range[0], velocity_range[1],
                    au_range[0], au_range[1],
                    lunar_range[0], lunar_range[1],
                    diameter_min, diameter_max
                ]

                # Add hazard filter
                if hazard_filter == "Only Dangerous":
                    base_query += " AND a.is_potentially_hazardous_asteroid = TRUE"
                elif hazard_filter == "Only Safe":
                    base_query += " AND a.is_potentially_hazardous_asteroid = FALSE"

                base_query += " ORDER BY ap.close_approach_date DESC LIMIT 200"

                # Show loading spinner
                with st.spinner("🔄 Searching asteroid database..."):
                    # Execute query
                    cursor = conn.cursor()
                    cursor.execute(base_query, params)
                    results = cursor.fetchall()

                    if results:
                        # Convert to DataFrame with nice column names
                        columns = [
                            'Asteroid Name',
                            'Approach Date',
                            'Velocity (km/h)',
                            'Distance (AU)',
                            'Distance (LD)',
                            'Min Diameter (km)',
                            'Max Diameter (km)',
                            'Potentially Hazardous'
                        ]
                        df = pd.DataFrame(results, columns=columns)

                        # Format the data for better display
                        df['Velocity (km/h)'] = df['Velocity (km/h)'].round(0).astype(int)
                        df['Distance (AU)'] = df['Distance (AU)'].round(4)
                        df['Distance (LD)'] = df['Distance (LD)'].round(2)
                        df['Min Diameter (km)'] = df['Min Diameter (km)'].round(3)
                        df['Max Diameter (km)'] = df['Max Diameter (km)'].round(3)

                        # Display results
                        st.success(f"🎯 Found {len(df)} asteroids matching your criteria!")

                        # Show summary statistics
                        st.markdown("#### 📊 **Search Results Summary:**")
                        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

                        with summary_col1:
                            st.metric("Total Found", len(df))
                        with summary_col2:
                            hazardous_count = len(df[df['Potentially Hazardous'] == 'Yes'])
                            st.metric("Hazardous", hazardous_count)
                        with summary_col3:
                            avg_velocity = df['Velocity (km/h)'].mean()
                            st.metric("Avg Velocity", f"{avg_velocity:,.0f} km/h")
                        with summary_col4:
                            min_distance = df['Distance (LD)'].min()
                            st.metric("Closest Approach", f"{min_distance:.2f} LD")

                        # Display the data table
                        st.markdown("#### 📋 **Detailed Results:**")
                        st.dataframe(df, use_container_width=True, height=400)

                        # Download options
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download Results as CSV",
                            csv,
                            f"asteroid_search_{start_date}_to_{end_date}.csv",
                            mime="text/csv"
                        )

                    else:
                        st.warning("🔍 No asteroids found matching your search criteria.")
                        st.info(
                            "💡 **Try adjusting your filters:**\n- Expand date range\n- Increase distance limits\n- Adjust velocity range\n- Check diameter settings")

                    cursor.close()
                    conn.close()

            except Exception as e:
                st.error(f"❌ Search failed: {e}")
                st.info("💡 **Tip:** Make sure your database connection is working and try simpler filter ranges.")


# ====== PAGE 4: CHARTS ======
elif page_choice == "📈 Charts":
    st.header("📈 Charts & Visualizations")

    chart_type = st.selectbox(
        "What would you like to see?",
        ["📊 Approaches by Month", "⚡ Speed Distribution", "🌙 Distance vs Speed"]
    )

    conn = connect_to_database()
    if conn:
        try:
            if chart_type == "📊 Approaches by Month":
                # Get monthly data
                query = """
                SELECT MONTH(close_approach_date) as month, COUNT(*) as count
                FROM close_approaches 
                GROUP BY MONTH(close_approach_date)
                ORDER BY month
                """
                df = pd.read_sql(query, conn)

                # Create month names
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                df['month_name'] = df['month'].apply(lambda x: months[x - 1])

                # Create bar chart
                fig = px.bar(df, x='month_name', y='count',
                             title='Asteroid Approaches by Month')
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "⚡ Speed Distribution":
                # Get speed data
                query = "SELECT relative_velocity_kmph FROM close_approaches LIMIT 1000"
                df = pd.read_sql(query, conn)

                # Create histogram
                fig = px.histogram(df, x='relative_velocity_kmph',
                                   title='Distribution of Asteroid Speeds')
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "🌙 Distance vs Speed":
                # Get distance vs speed data
                query = """
                SELECT miss_distance_lunar, relative_velocity_kmph 
                FROM close_approaches 
                WHERE miss_distance_lunar < 5 
                LIMIT 500
                """
                df = pd.read_sql(query, conn)

                # Create scatter plot
                fig = px.scatter(df, x='miss_distance_lunar', y='relative_velocity_kmph',
                                 title='Asteroid Distance vs Speed')
                st.plotly_chart(fig, use_container_width=True)

            conn.close()

        except Exception as e:
            st.error(f"Error creating chart: {e}")

# ====== FOOTER ======
st.markdown("---")
st.markdown("🚀 **NASA Asteroids Explorer** - Built with Streamlit")
st.markdown("📚 **Learning tip:** Check the code to see how each feature works!")
