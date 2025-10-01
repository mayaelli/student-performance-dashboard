import streamlit as st
import pandas as pd
import numpy as np
import io
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import io

# -----------------------
# Page config + header
# -----------------------
st.set_page_config(page_title="Student Performance EDA Dashboard", layout="wide")
st.markdown(
    """
    <div style="text-align:center">
      <h1 style="color:#00FFB3;"> Student Performance EDA Dashboard</h1>
      <p style="color:gray; margin-top:-12px">
        Explore how lifestyle, demographics, and academics influence exam performance
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Load dataset (fixed)
# -----------------------
@st.cache_data(show_spinner=False)
def load_data(path="student-mat.csv"):
    try:
        df = pd.read_csv(path)
        if df.shape[1] == 1:  # sometimes ; separator is used
            df = pd.read_csv(path, sep=";")
        return df
    except Exception as e:
        st.error(f"❌ Failed to load dataset: {e}")
        st.stop()

df = load_data()

# -----------------------
# Sidebar Filters (with Reset + Empty Check)
# -----------------------
st.sidebar.header("🔎 Filters")

# --- Initialize defaults in session state ---
if "selected_gender" not in st.session_state and "sex" in df.columns:
    st.session_state["selected_gender"] = df["sex"].unique().tolist()

if "selected_school" not in st.session_state and "school" in df.columns:
    st.session_state["selected_school"] = df["school"].unique().tolist()

if "selected_medu" not in st.session_state and "Medu" in df.columns:
    st.session_state["selected_medu"] = sorted(df["Medu"].unique())

if "studytime_range" not in st.session_state and "studytime" in df.columns:
    st.session_state["studytime_range"] = (
        int(df["studytime"].min()),
        int(df["studytime"].max())
    )

# --- Reset Button ---
if st.sidebar.button("🔄 Reset Filters"):
    if "sex" in df.columns:
        st.session_state["selected_gender"] = df["sex"].unique().tolist()
    if "school" in df.columns:
        st.session_state["selected_school"] = df["school"].unique().tolist()
    if "Medu" in df.columns:
        st.session_state["selected_medu"] = sorted(df["Medu"].unique())
    if "studytime" in df.columns:
        st.session_state["studytime_range"] = (
            int(df["studytime"].min()),
            int(df["studytime"].max())
        )

# --- Gender filter ---
if "sex" in df.columns:
    selected_gender = st.sidebar.multiselect(
        "Filter by Gender",
        options=df["sex"].unique(),
        default=st.session_state["selected_gender"]
    )
    st.session_state["selected_gender"] = selected_gender
    df = df[df["sex"].isin(selected_gender)]

# --- School filter ---
if "school" in df.columns:
    selected_school = st.sidebar.multiselect(
        "Filter by School",
        options=df["school"].unique(),
        default=st.session_state["selected_school"]
    )
    st.session_state["selected_school"] = selected_school
    df = df[df["school"].isin(selected_school)]

# --- Parental education filter ---
if "Medu" in df.columns:
    selected_medu = st.sidebar.multiselect(
        "Mother's Education Level",
        options=sorted(df["Medu"].unique()),
        default=st.session_state["selected_medu"]
    )
    st.session_state["selected_medu"] = selected_medu
    df = df[df["Medu"].isin(selected_medu)]

# --- Studytime filter ---
if "studytime" in df.columns:
    studytime_range = st.sidebar.slider(
        "Studytime (hours/week)",
        min_value=int(df["studytime"].min()),
        max_value=int(df["studytime"].max()),
        value=st.session_state["studytime_range"]
    )
    st.session_state["studytime_range"] = studytime_range
    df = df[(df["studytime"] >= studytime_range[0]) & (df["studytime"] <= studytime_range[1])]

# --- Dataset Summary ---
st.sidebar.markdown("---")
if df.empty:
    st.sidebar.error("⚠️ No data available with the selected filters.")
else:
    st.sidebar.markdown(
        f"""
        📊 **Dataset Overview**  
        - Total Students: `{len(df)}`  
        - Columns: `{len(df.columns)}`  
        - Active Filters:  
          • Gender = {", ".join(selected_gender) if "sex" in df.columns else "N/A"}  
          • School = {", ".join(selected_school) if "school" in df.columns else "N/A"}  
          • Medu = {", ".join(map(str, selected_medu)) if "Medu" in df.columns else "N/A"}  
          • Studytime = {studytime_range[0]}–{studytime_range[1]} hrs/week  
        """
    )

# -----------------------
# Top Metrics Section (Centered)
# ----------------------

# Add 5 columns, keep the middle 3 for metrics
col0, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 1])

with col1:
    st.metric(
        label="👥 Total Students",
        value=len(df)
    )

with col2:
    if "G3" in df.columns:
        avg_g3 = round(df["G3"].mean(), 2)
        st.metric(
            label="📊 Average Final Grade (G3)",
            value=avg_g3
        )
    else:
        st.metric("📊 Average Final Grade (G3)", "N/A")

with col3:
    if "G3" in df.columns:
        pass_rate = (df["G3"] >= 10).mean() * 100  # assume passing is ≥ 10
        st.metric(
            label="✅ Pass Rate",
            value=f"{pass_rate:.1f}%"
        )
    else:
        st.metric("✅ Pass Rate", "N/A")




# -----------------------
# Tabs Layout
# -----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [" Overview", " Correlation Heatmap", " Boxplots", " Scatter Insights", " Insights Section"]
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #000000; /* pitch black */
        }
        .metric-card {
            background: linear-gradient(135deg, #2d642b, #e76d00);
            padding: 14px; 
            border-radius: 12px;
            text-align: center;
            color: #f3ff8c;
            font-weight: bold;
            box-shadow: 0px 0px 10px rgba(243,255,140,0.6);
        }
        h2, h3, h4, p, .stMarkdown {
            color: #f5f5f5 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Tab 1: Overview
# -----------------------

with tab1:
    st.markdown("## 📖 Dataset Overview")

    st.markdown("""
    The dataset `student-mat.csv` contains information about **secondary education students** in Portugal, 
    focusing on **demographic, social, and academic factors** that influence **mathematics performance**.  

    Our main goal is to explore which features impact the **final exam score (G3)** most, and what these patterns 
    reveal about **student habits, background, and outcomes**.
    """)

    # --- Metrics Row ---
    n_rows, n_cols = df.shape
    n_missing = int(df.isnull().sum().sum())
    n_duplicates = int(df.duplicated().sum())

    colA, colB, colC, colD = st.columns(4)
    colA.markdown(f"<div class='metric-card'>Rows<br>{n_rows:,}</div>", unsafe_allow_html=True)
    colB.markdown(f"<div class='metric-card'>Columns<br>{n_cols:,}</div>", unsafe_allow_html=True)
    colC.markdown(f"<div class='metric-card'>Missing<br>{n_missing:,}</div>", unsafe_allow_html=True)
    colD.markdown(f"<div class='metric-card'>Duplicates<br>{n_duplicates:,}</div>", unsafe_allow_html=True)

    # --- Data Preview ---
    st.markdown("### 🔍 Data Preview")
    rows_to_show = st.slider("Rows to display", 5, 30, 10)
    st.dataframe(df.head(rows_to_show), use_container_width=True)

    # --- Split Layout: Info + Graphs ---
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### 📑 Data Info")       
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
    
        st.markdown(
            f"""
            <div style="
                background-color:#111;
                padding:12px;
                border-radius:8px;
                font-size:12px;
                font-family: monospace;
                color:#f5f5f5;
                white-space: pre;
                line-height: 1.4;
                overflow-x: auto;
            ">{info_str}</div>
            """,
            unsafe_allow_html=True
        )

    # Explanatory note at the bottom
        st.caption(""" 
        - The dataset contains **395 student records**.  
        - There are **33 features**: **16 numeric** (e.g., age, grades, study time) and **17 categorical** (e.g., gender, school, family background).  
        - No columns contain missing values, which means the dataset is **clean and ready** for analysis.  
        - These structural details provide the foundation for deeper exploration of student demographics, lifestyle, and academic performance.
        """)

    with col2:
        st.markdown("### 📊 Key Distributions")

        # Gender distribution
        if "sex" in df.columns:
            gender_counts = df["sex"].value_counts().reset_index()
            gender_counts.columns = ["Gender", "Count"]
        
            fig1 = px.bar(
                gender_counts,
                x="Gender", y="Count", text="Count",
                color="Gender",
                color_discrete_map={
                    "F": "#f3ff8c",   # female = neon yellow-green
                    "M": "#e76d00"   # male = bright orange
                },
                title="✨ Gender Distribution"
            )
        
            fig1.update_traces(
                marker_line_color="#fff",
                marker_line_width=1.2,
                textfont=dict(color="white", size=12)
            )
            fig1.update_layout(
                height=300,  # smaller height
                plot_bgcolor="#000",
                paper_bgcolor="#000",
                font=dict(color="#f5f5f5", size=13),
                title=dict(x=0.5, xanchor="center")
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.caption("👩‍🎓👨‍🎓 Female students slightly outnumber male students in this dataset.")

        # Failures distribution
        if "failures" in df.columns:
            fail_counts = df["failures"].value_counts().reset_index()
            fail_counts.columns = ["Failures", "Count"]
        
            fig2 = px.bar(
                fail_counts.sort_values("Failures"),
                x="Failures", y="Count", text="Count",
                color="Failures",
                color_discrete_sequence=["#f3ff8c", "#d4ffcb", "#2d642b", "#e76d00"],
                title="📉 Number of Past Class Failures"
            )
        
            fig2.update_traces(textfont=dict(color="white", size=12))
            fig2.update_layout(
                height=300,  # smaller height
                plot_bgcolor="#000",
                paper_bgcolor="#000",
                font=dict(color="#f5f5f5", size=13),
                title=dict(x=0.5, xanchor="center")
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("❌ Most students reported **0 past class failures**, but a minority had multiple failures.")

   # --- Summary Stats ---
            st.markdown("### 📈 Summary Statistics")
            
            num_desc = df.describe(include=[np.number]).transpose()
            st.dataframe(num_desc, use_container_width=True)
            st.caption("""
            This table provides key **descriptive statistics** for all numeric features in the dataset.  
            It shows the **mean, standard deviation, minimum, maximum, and quartile values**.  
            These numbers help us understand the **spread and central tendency** of student-related variables, 
            such as grades (G1–G3), absences, and study time.
            """)
            


# -----------------------
# Tab 2: Correlation Heatmap
# -----------------------
with tab2:
    st.markdown("### 🔗 Correlation Heatmap")
    corr = df.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        ax=ax,
        cbar=True,
        annot_kws={"size": 6}
    )

    ax.set_xticklabels(ax.get_xticklabels(), fontsize=7, rotation=45, ha="right")
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=7)

    st.pyplot(fig, use_container_width=True)

    st.markdown("""
    ###  Interpretation
    
    - The final grade (**G3**) is **highly correlated** with the first two period grades (**G1** and **G2**), highlighting the importance of consistent performance across the school year.  
    - **Parental education** (e.g., *Medu, Fedu*) shows a **weak positive correlation** with student outcomes, suggesting that higher parental education levels may contribute indirectly to academic success.  
    - **Failures** (*failures*) demonstrate a **strong negative correlation** with G3, confirming that repeated academic struggles heavily impact final results.  
    - **Study time** (*studytime*) shows only a **modest positive effect**, implying that **quality of study may matter more than quantity**.  
    - Lifestyle factors like **alcohol consumption** (*Dalc, Walc*) are **weakly but negatively correlated**, hinting at potential long-term risks for academic consistency.  
    
    ---
     **Takeaway:**  
    While **prior grades remain the strongest predictors** of student achievement, **early identification of repeated failures** and **support for healthier lifestyle habits** could significantly improve outcomes. Socio-demographic variables (like parental education) play a smaller but still relevant role in shaping long-term academic trends.  
    """
    )


# -----------------------
# Tab 3: Boxplots
# -----------------------
with tab3:
    st.markdown("### 📦 Boxplots — Numeric Feature Distributions")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature = st.selectbox(
        "Choose a numeric feature to visualize:",
        numeric_cols,
        index=numeric_cols.index("G3") if "G3" in numeric_cols else 0
    )

    # Custom color palette (your theme)
    custom_colors = ["#f3ff8c", "#e76d00", "#2d642b"]

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(
        data=df, 
        y=feature, 
        ax=ax, 
        color=custom_colors[1],   # main accent (orange) for box
        boxprops=dict(facecolor=custom_colors[1], alpha=0.7, edgecolor="black"),
        medianprops=dict(color=custom_colors[0], linewidth=2),  # neon yellow median line
        whiskerprops=dict(color=custom_colors[2], linewidth=1.5),
        capprops=dict(color=custom_colors[2], linewidth=1.5),
        flierprops=dict(marker='o', color=custom_colors[0], markersize=5, alpha=0.8)  # outliers
    )

    # Style tweaks for white background
    ax.set_facecolor("white")
    ax.set_title(f"Distribution of {feature}", color="black", fontsize=12)
    ax.tick_params(colors="black")
    for spine in ax.spines.values():
        spine.set_color("black")

    st.pyplot(fig, use_container_width=True)

    st.markdown(
        f"""
        **Interpretation:**  
        - The boxplot shows the **spread, median, and presence of outliers** for `{feature}`.  
        - The **middle line** inside the box is the median value (highlighted in neon yellow), while the box edges show the interquartile range (IQR).  
        - Dots beyond the whiskers (in neon yellow) represent **outliers**, which may indicate unusual student behavior or special cases.  
        - For grades (`G1`, `G2`, `G3`), outliers may highlight students with exceptionally low or high scores.  
        - For other numeric features (like `absences` or `studytime`), this helps spot students whose values differ greatly from most of the class.
        """
    )


# -----------------------
# Tab 4: Scatter Insights
# -----------------------
with tab4:
    st.markdown("### 🫧 Interactive Scatter Plot")

    if "studytime" in df.columns and "G3" in df.columns:
        fig = px.scatter(
            df,
            x="studytime",
            y="G3",
            color="sex" if "sex" in df.columns else None,
            size="absences" if "absences" in df.columns else None,
            hover_data=["age", "famsize", "failures"] if "age" in df.columns else None,
            title="Studytime vs Final Grade (G3)",
            color_discrete_map={
                "F": "#f3ff8c",   # female = neon yellow-green
                "M": "#e76d00"    # male = bright orange
            },
            template="plotly_dark",
            size_max=40   # makes bubbles more visible
        )

        # Scale bubble size more clearly
        fig.update_traces(marker=dict(sizeref=2.*max(df["absences"])/40**2))

        st.plotly_chart(fig, use_container_width=True)

        # --- Insights below chart ---
        st.markdown(
            f"""
            **Insights from the Scatter Plot:**  
            - Each point represents a student, positioned by **studytime** (x-axis) and **final grade (G3)** (y-axis).  
            - Bubble **size** reflects the number of **absences**, so larger circles = students who skipped more classes.  
            - Colors indicate **gender** (female in neon yellow-green, male in bright orange).  
            - Notice how students with **higher studytime (3–4)** tend to achieve **better grades** compared to those with studytime = 1.  
            - However, **high absences** (big bubbles) often correlate with **lower grades**, even if studytime is higher.  
            - This suggests that both **study habits and class attendance** play a strong role in exam success.  
            """
        )


# -----------------------
# Tab 5: Insights Section
# -----------------------
with tab5:
    st.markdown("## 🔑 Key Questions & Insights")

    # Consistent chart background + font
    chart_props = dict(
        width=450,
        height=220,
        background="#000",  # black background
    )

    # Q1: Correlations with G3
    if "G3" in df.columns:
        st.markdown("##### Q1. Which features have the highest correlation with the final exam scores (G3)?")
        corr_sorted = df.corr(numeric_only=True)["G3"].drop("G3").sort_values(ascending=False)
        top_corr = corr_sorted.head(5).reset_index()
        top_corr.columns = ["Feature", "Correlation"]

        bars1 = alt.Chart(top_corr).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X("Correlation:Q", title="Correlation with G3"),
            y=alt.Y("Feature:N", sort="-x"),
            color=alt.Color("Correlation:Q", scale=alt.Scale(domain=[0, 1], range=["#f3ff8c", "#e76d00"])),
            tooltip=["Feature", "Correlation"]
        ).properties(**chart_props)

        st.altair_chart(bars1, use_container_width=True)
        st.markdown(
            f"""
            <div style="font-size:16px; line-height:1.5;">
            The bar chart highlights the top <b>5 features most strongly and positively correlated with final exam scores (G3)</b> <br> 
            - These variables are the ones most strongly associated with student performance. <br>
            - For example, previous grades (G1 and G2) often dominate, since early performance strongly predicts final outcomes. <br>
            - Study-related variables, such as study time or failures, may also appear, reinforcing the importance of consistent academic effort. <br>
            - <b>Interpretation:</b> These correlations suggest that past performance and study habits are crucial indicators of how students will perform in their final exam. Teachers can use this to identify at-risk students early. <br> <br>
            </div>
            """,
            unsafe_allow_html=True
        )


    # Q2: Studytime correlation
    if "studytime" in df.columns and "G3" in df.columns:
        st.markdown("##### Q2. How does study time correlate with exam performance?")
        study_corr = df["studytime"].corr(df["G3"])
        st.markdown(
            f"""
            <div style="font-size:16px; line-height:1.5;">
            Based on the heatmap graph in correlation heatmap tab, the correlation coefficient between <b>study time</b> and <b>final grades (G3)</b> is 
            <b>{study_corr:.2f}</b>.  
    
            - A positive value suggests that students who study longer tend to perform better, although the strength of the correlation varies.
            - However, if the correlation is weak, it shows that study time alone does not guarantee success, as factors like study quality, motivation, and external support also play major roles.
            - <b>Interpretation:</b> While study time helps, it is not a sole determinant of success. Effective study habits matter more than raw hours.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Q3: Boxplot insights
        st.markdown("##### Q3. What insights can you draw from the boxplot?")
        st.markdown(
            f"""
            <div style="font-size:16px; line-height:1.5;">
            Boxplots provide a compact summary of student performance distributions:
        
            - <b>Medians (middle line):</b> Shows the central tendency of exam scores.
            - <b>Spread (box size):</b> Indicates the range of "typical" performance (interquartile range). A wider box means more variation among students.
            - <b>Outliers:</b> Students who score far above or below the typical range. These cases may represent exceptional achievers or struggling students reading intervention.
              much better or worse than peers.  
            - <b>Interpretation: </b> The boxplot highlights performance consistency and reveals whether most students cluster around similar grades or if large disparities exist.\
            </div>
            """,
            unsafe_allow_html=True
        )



    # Q4: Gender impact
    if "sex" in df.columns and "G3" in df.columns:
        st.markdown("##### Q4. How does gender impact the final exam score?")
        avg_scores = df.groupby("sex")["G3"].mean().reset_index()
    
        bars2 = alt.Chart(avg_scores).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X("sex:N", title="Gender"),
            y=alt.Y("G3:Q", title="Average Final Score"),
            color=alt.Color("sex:N", scale=alt.Scale(range=["#ff2d95","#00f7ff"])),  # neon purple/pink
            tooltip=["sex", "G3"]
        ).properties(**chart_props)
    
        st.altair_chart(bars2, use_container_width=True)
    
        # ✨ Detailed Interpretation
        st.markdown(
            f"""
            <div style="font-size:16px; line-height:1.5;">
            The comparison of average <b>final exam scores (G3)</b> between male and female students 
            shows meaningful but subtle differences:
    
            - <b>Average performance: </b> One gender tends to have slightly higher scores, consistent with some educational research.
            - <b> No large gap: </b> The difference is small, suggesting that gender alone does not determine performance.
            - <b> Broader factors: </b> Study habits, family support, and attendance are stronger predictors.
            - <b> Interpretation: </b> Gender may have a modest influence, but educators should avoid stereotyping. Interventions should focus on study skills and learning support for all students.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Q5: Attendance / Absences
    if "absences" in df.columns and "G3" in df.columns:
        st.markdown("##### Q5. Do absences affect grades?")
    
        abs_corr = df["absences"].corr(df["G3"])
        
        st.markdown(
            f"<small>Correlation coefficient between absences and final grade (G3): "
            f"**{abs_corr:.2f}**</small>", 
            unsafe_allow_html=True
        )
    
        # --- Chart (dark-themed) ---
        abs_scatter = alt.Chart(df).mark_circle(size=70, opacity=0.7).encode(
            x=alt.X("absences:Q", title="Number of Absences"),
            y=alt.Y("G3:Q", title="Final Grade (G3)"),
            color=alt.Color("sex:N", scale=alt.Scale(range=["#f3ff8c", "#e76d00"])),  # palette: neon yellow-green & orange
            tooltip=["absences", "G3", "sex", "studytime"]
        ).properties(
            height=300, width=450,
            background="#000000"  # 🔥 black background
        ).configure_axis(
            grid=True,
            gridColor="#222222",   # subtle gridlines
            labelColor="#f5f5f5",  # light font
            titleColor="#f5f5f5"
        ).configure_title(
            color="#f5f5f5"
        )
    
        st.altair_chart(abs_scatter, use_container_width=True)
    
        # --- Detailed Interpretation ---
        st.markdown(
            f"""
            <div style="font-size:16px; line-height:1.5;">
            The relationship between absences and final grades (G3) provides meaningful insights:
    
            - <b>Correlation value:</b> The coefficient is **{abs_corr:.2f}**, suggesting a 
              {"moderate negative" if abs_corr < -0.3 else "weak negative" if abs_corr < 0 else "little to no"} 
              relationship between missing classes and exam performance.  
            - <b>General trend: </b> Students who attend more classes tend to perform better.
            - <b>Outliers:</b> Some students perform well despite frequent absences, showing indvidual differences in learning styles or self-study capacity.
            - <b>Interpretation:</b> Attendance is an importance behavioral factor for academic success. Schools should monitor absenteeism and provide early support to students with chronic absences.
            """,
            unsafe_allow_html=True
        )



    # Q6: Negative correlations
    if "G3" in df.columns:
        st.markdown("##### Q6. Which features are most negatively correlated with G3?")
    
        bottom_corr = corr_sorted.tail(5).reset_index()
        bottom_corr.columns = ["Feature", "Correlation"]
    
        # --- Chart (dark theme) ---
        bars3 = alt.Chart(bottom_corr).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X("Correlation:Q", title="Correlation with G3"),
            y=alt.Y("Feature:N", sort="x"),
            color=alt.Color(
                "Correlation:Q", 
                scale=alt.Scale(domain=[-1, 0], range=["#00f7ff", "#8c5ae8"])  # neon blue → purple
            ),
            tooltip=["Feature", "Correlation"]
        ).properties(
            height=300, width=500,
            background="#000000"  # 🔥 black background
        ).configure_axis(
            grid=True,
            gridColor="#222222",   # subtle grid
            labelColor="#f5f5f5",  # light font
            titleColor="#f5f5f5"
        ).configure_title(
            color="#f5f5f5"
        )
    
        st.altair_chart(bars3, use_container_width=True)
    
        # --- Interpretation ---
        st.markdown(
            f"""
            <div style="font-size:16px; line-height:1.5;">
            This chart highlights the top 5 features most negatively correlated with final exam scores.  
    
            - <b> High absences, more failures, or risky lifestyle choices </b> often appear here.
            - These factor indicate behaviors or conditions that tend to lower academic performance.
            - <b> Interpretation: </b> Negative correlates act as risk indicators. They don't directly cause low scores but signal students who may need academic intervention, counseling, or support.
            - Educators can use these insights to preventively address challenges before performance drops significantly.
            </div>
            """,
            unsafe_allow_html=True
        )


        # --- Final Summary ---
        st.markdown("---")
        st.subheader(" Summary & Key Insights")
    
        st.markdown(
            """
            ####  Key Findings
            - **Grades are cumulative**: G3 (final grade) is strongly correlated with G1 and G2, meaning consistent performance across periods is the best predictor of success.  
            - **Demographics have modest effects**: Parental education (Medu) and school attended show some influence, but weaker compared to prior grades.  
            - **Lifestyle factors matter**: Alcohol consumption (Dalc, Walc) and higher absences slightly reduce performance.  
            - **Study habits**: More study time is linked to better performance, but the effect is mild compared to previous grades.  
            - **Outliers matter**: Extreme values in grades, absences, or study time suggest special cases that may need targeted interventions.  
    
            ###  Takeaway
            Academic performance is best explained by **prior performance (G1, G2)**, with demographics and lifestyle contributing secondary effects.  
            This suggests that **early interventions** (after G1/G2) and **support for at-risk students** (absences, low Medu, high lifestyle risks) can improve outcomes.  
            """
        )
