# Student Performance Dashboard

This project is an interactive **Streamlit dashboard** designed to analyze and visualize the **Student Performance Dataset (student-mat.csv)**.  
It provides educators, researchers, and students with an accessible platform to explore academic performance trends, correlations, and insights.

---

## Features

###  Data Filtering
- Apply filters by **gender**, **parental education**, **school**, and **study time** to focus on specific subsets of the dataset.

###  Key Metrics
- Displays **total number of students**, **average final grade**, and **pass rate** at the top of the dashboard.

###  Exploratory Visualizations
- Correlation **heatmap** to highlight relationships between variables.  
- **Boxplots** to visualize the spread, median, and outliers of selected features.  
- **Bar charts** and other visualizations for categorical and numerical features.

###  Insights Section
- Summarized interpretations for each visualization, providing meaningful takeaways on student performance patterns.

###  User-Friendly Layout
- Organized using **tabs, sidebars, and metrics** to resemble a professional dashboard.

---

## Dataset

The dataset used is **student-mat.csv**, which contains academic and demographic details of students.  
It includes attributes such as:

- **Gender (sex)**
- **Study time (studytime)**
- **Mother's education level (Medu)**
- **School (school)**
- **Grades (G1, G2, G3)**
- **Lifestyle factors** (e.g., alcohol consumption, absences)

---

## Installation

Clone this repository:

```bash
git clone https://github.com/YOUR_USERNAME/student-performance-dashboard.git
cd student-performance-dashboard
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```
Run the Streamlit app:
```bash
streamlit run streamlit-version.py
```

## Usage
* Use the sidebar filters to narrow down the dataset by selected criteria.
* Navigate through the tabs to view summary metrics, visualizations, and insights.

* Interpret the results to better understand how demographic, lifestyle, and academic factors influence student performance.

## Project Goals
This project was developed to practice Exploratory Data Analysis (EDA) and dashboard creation using Streamlit.
It demonstrates how interactive data applications can make statistical insights more accessible and actionable for educators and decision-makers.
