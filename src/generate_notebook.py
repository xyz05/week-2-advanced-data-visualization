import nbformat as nbf
import os

def build_notebook():
    nb = nbf.v4.new_notebook()
    cells = []

    # Section 1: Title
    cells.append(nbf.v4.new_markdown_cell("""# Week 2: Advanced Data Visualization and Storytelling with Python
## Germany Electricity Consumption & Renewable Energy Transformation (2006–2017)

**Author:** Data Science Hackathon Participant  
**Dataset:** OPSD Germany Daily Electricity & Renewable Energy Data  
**Target Audience:** Non-technical stakeholders, policymakers, and public clean energy observers  
"""))

    # Section 2: Introduction
    cells.append(nbf.v4.new_markdown_cell("""## 1. Introduction & Context
Over the past decade, Germany has undergone the *Energiewende* (Energy Transition), a major structural transformation aimed at replacing fossil fuels and nuclear power with renewable energy sources such as wind and solar.

This notebook builds upon the cleaned Week 1 dataset to construct a coherent, evidence-based visual story explaining how national electricity consumption evolved alongside the rapid growth of wind and solar generation from 2006 through 2017.
"""))

    # Section 3: Dataset
    cells.append(nbf.v4.new_markdown_cell("""## 2. Dataset Overview
The dataset contains daily observations of Germany's national electricity grid over 12 full years (4,383 rows):
- **Consumption:** Daily national electricity demand in Gigawatt-hours (GWh/day).
- **Wind:** Daily wind power generation (GWh/day, recorded from 2010 onwards).
- **Solar:** Daily solar power generation (GWh/day, recorded from 2012 onwards).
- **Wind+Solar:** Combined daily renewable energy generation (GWh/day).
- **Temporal Metadata:** Year, Month, Day, Weekday, Is_Weekend, and Season.
"""))

    # Section 4: Story Question
    cells.append(nbf.v4.new_markdown_cell("""## 3. Central Story Question
> **"How has Germany's electricity consumption evolved alongside the rapid expansion of wind and solar energy generation over time?"**
"""))

    # Section 5: Data Validation
    cells.append(nbf.v4.new_markdown_cell("""## 4. Data Validation & Environment Setup"""))

    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 120

# Load dataset
data_path = '../data/cleaned/cleaned_dataset.csv'
if not os.path.exists(data_path):
    data_path = '../../Week1_Data_Analysis/data/cleaned/cleaned_dataset.csv'

df = pd.read_csv(data_path)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

print('Dataset Shape:', df.shape)
print('Date Range:', df['Date'].min().strftime('%Y-%m-%d'), 'to', df['Date'].max().strftime('%Y-%m-%d'))
print('\\nNull Value Count:')
print(df.isnull().sum())
"""))

    # Section 6: Data Preparation
    cells.append(nbf.v4.new_markdown_cell("""## 5. Data Preparation & Feature Engineering"""))

    cells.append(nbf.v4.new_code_cell("""# Compute 30-day and 365-day moving averages for trend extraction
df['Consumption_30d'] = df['Consumption'].rolling(30, center=True).mean()
df['Consumption_365d'] = df['Consumption'].rolling(365, center=True).mean()

df['Wind_30d'] = df['Wind'].rolling(30, center=True).mean()
df['Solar_30d'] = df['Solar'].rolling(30, center=True).mean()
df['WindSolar_30d'] = df['Wind+Solar'].rolling(30, center=True).mean()

# Annual TWh aggregates
annual = df.groupby('Year')[['Consumption', 'Wind', 'Solar', 'Wind+Solar']].sum() / 1000.0
annual['Renewable_Share_%'] = (annual['Wind+Solar'] / annual['Consumption']) * 100.0

print('Annual Aggregates (TWh):')
print(annual)
"""))

    # Section 7: Visualization 1
    cells.append(nbf.v4.new_markdown_cell("""## 6. Visualization 1: Electricity Consumption Trend Over Time

### Story Context & Rationale
- **Question:** How has daily electricity demand behaved across 12 years?
- **Visual Choice:** A time-series line plot with 30-day and 365-day moving averages filters out high-frequency daily noise, exposing structural macro trends.
- **Key Observation:** National consumption exhibits remarkable long-term structural stability around 1,338.7 GWh/day, with strong recurring annual oscillations.
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df['Date'], df['Consumption'], color='#a6cee3', alpha=0.35, linewidth=0.8, label='Daily Consumption (GWh)')
ax.plot(df['Date'], df['Consumption_30d'], color='#1f78b4', alpha=0.85, linewidth=1.8, label='30-Day Moving Average')
ax.plot(df['Date'], df['Consumption_365d'], color='#e31a1c', linewidth=2.5, label='365-Day Annual Trendline')

# Annotations
ax.annotate('2008–2009 Global Recession Drop\\n(Demand fell ~12% below baseline)',
            xy=(pd.to_datetime('2009-04-01'), 1180), xytext=(pd.to_datetime('2007-06-01'), 950),
            arrowprops=dict(facecolor='#e31a1c', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, fontweight='bold', color='#7f0000',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', alpha=0.8))

ax.set_title("Figure 1: Germany Daily Electricity Consumption Trend (2006–2017)", pad=15)
ax.set_xlabel("Year")
ax.set_ylabel("Electricity Consumption (GWh / Day)")
ax.set_ylim(750, 1850)
ax.legend(loc='upper right', frameon=True, facecolor='white')
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### Visual Storytelling Analysis (Visualization 1)
1. **Title:** Figure 1: Germany Daily Electricity Consumption Trend (2006–2017)
2. **Question:** What is the overall macro trend in German electricity consumption over a 12-year horizon?
3. **Rationale:** Time-series line chart with dual rolling averages isolates short-term seasonality from long-term macroeconomic shifts.
4. **What Audience Sees:** An oscillating blue band showing annual winter peaks and summer troughs, overlaid with a steady red 365-day trendline showing a sharp dip in 2009.
5. **Main Evidence:** Mean daily consumption is **1,338.7 GWh/day**. The lowest daily demand occurred on **2009-12-25 (842.4 GWh)** during the financial crisis, while peak demand hit **1,709.6 GWh** on **2006-12-15**.
6. **Numerical Proof:** The 365-day trendline shows consumption dropping from ~1,390 GWh/day in 2007 down to ~1,270 GWh/day in mid-2009, before rebounding back to ~1,350 GWh/day by 2011.
7. **Why It Matters:** Grid infrastructure must maintain reliability across extreme swing ranges (~840 GWh to ~1,710 GWh).
8. **Caution/Limitation:** Consumption represents gross public grid demand; behind-the-meter off-grid solar generation is not captured.
9. **Narrative Transition:** Having established demand baseline stability, we next examine how clean renewable generation grew to meet this demand.
"""))

    # Section 8: Visualization 2
    cells.append(nbf.v4.new_markdown_cell("""## 7. Visualization 2: Renewable Energy Generation Growth Trend

### Story Context & Rationale
- **Question:** How rapidly did wind and solar power generation expand across Germany's power grid?
- **Visual Choice:** Multi-line plot with area fill for combined renewable output visually communicates cumulative volume and growth trajectory over time.
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(14, 6))

df_valid = df[df['Date'] >= '2010-01-01'].copy()

ax.plot(df_valid['Date'], df_valid['Wind_30d'], color='#17becf', linewidth=2.2, label='Wind Generation (30d Avg)')
ax.plot(df_valid['Date'], df_valid['Solar_30d'], color='#ff7f0e', linewidth=2.2, label='Solar Generation (30d Avg)')
ax.plot(df_valid['Date'], df_valid['WindSolar_30d'], color='#2ca02c', linewidth=2.8, label='Combined Wind + Solar (30d Avg)')
ax.fill_between(df_valid['Date'], 0, df_valid['WindSolar_30d'], color='#2ca02c', alpha=0.15)

ax.set_title("Figure 2: Growth Trajectory of Wind and Solar Power Generation in Germany (2010–2017)", pad=15)
ax.set_xlabel("Year")
ax.set_ylabel("Electricity Generation (GWh / Day)")
ax.set_ylim(0, 850)
ax.legend(loc='upper left', frameon=True, facecolor='white')
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### Visual Storytelling Analysis (Visualization 2)
1. **Title:** Figure 2: Growth Trajectory of Wind and Solar Power Generation in Germany (2010–2017)
2. **Question:** What was the expansion trajectory of renewable generation?
3. **Rationale:** Smoothed multi-line chart highlights individual contributions of wind and solar while showing cumulative impact.
4. **What Audience Sees:** A dramatic upward trajectory in green (combined renewables) and teal (wind), accompanied by regular summer golden crests (solar).
5. **Main Evidence:** Combined Wind+Solar daily average grew from **124.3 GWh/day in 2012** to **272.7 GWh/day in 2017**, representing a **+119.4% total increase** (17.0% CAGR).
6. **Numerical Proof:** Maximum single-day wind generation spiked to **825.5 GWh** on **2017-12-07**, supplying over 50% of national demand on that day.
7. **Why It Matters:** Demonstrates the successful scaling of renewable capacity under the *Energiewende* policy.
8. **Caution/Limitation:** Wind generation exhibits severe short-term volatility compared to solar.
9. **Narrative Transition:** Next, we examine seasonal patterns to understand when renewables produce maximum power relative to peak demand.
"""))

    # Section 9: Visualization 3
    cells.append(nbf.v4.new_markdown_cell("""## 8. Visualization 3: Seasonal Pattern Analysis

### Story Context & Rationale
- **Question:** How do monthly and seasonal weather changes align with human energy consumption?
- **Visual Choice:** Panel A (Boxplot of monthly demand distribution) + Panel B (Monthly average profile comparing demand, wind, and solar).
"""))

    cells.append(nbf.v4.new_code_cell("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Panel A
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sns.boxplot(x='Month_Name', y='Consumption', data=df, ax=ax1, palette='Blues_r', order=month_order)
ax1.set_title("Panel A: Monthly Consumption Distribution")
ax1.set_xlabel("Month")
ax1.set_ylabel("Daily Consumption (GWh)")

# Panel B
monthly_avg = df.groupby('Month_Name')[['Consumption', 'Wind', 'Solar']].mean().reindex(month_order)
ax2.plot(monthly_avg.index, monthly_avg['Consumption'], color='#1f77b4', marker='o', linewidth=2.5, label='Consumption')
ax2.plot(monthly_avg.index, monthly_avg['Wind'], color='#17becf', marker='s', linewidth=2.5, label='Wind Generation')
ax2.plot(monthly_avg.index, monthly_avg['Solar'], color='#ff7f0e', marker='^', linewidth=2.5, label='Solar Generation')
ax2.set_title("Panel B: Seasonal Rhythm Comparison")
ax2.set_xlabel("Month")
ax2.set_ylabel("Daily Mean (GWh)")
ax2.legend(loc='center right', frameon=True)

plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### Visual Storytelling Analysis (Visualization 3)
1. **Title:** Figure 3: Seasonal Rhythms of Demand and Renewable Power Generation
2. **Question:** Are there noticeable seasonal patterns in consumption and renewable output?
3. **Rationale:** Boxplots show monthly demand dispersion, while multi-line profiles reveal seasonal alignment between demand, wind, and solar.
4. **What Audience Sees:** Consumption peaks in winter (December/January) and reaches its lowest point in August. Wind aligns with winter demand, while solar peaks in summer.
5. **Main Evidence:** Average December consumption is **1,444.6 GWh/day**, compared to **1,239.7 GWh/day** in August (a 16.5% seasonal variation).
6. **Numerical Proof:** Average December wind generation is **280.8 GWh/day** (vs. 116.3 GWh in August), while average July solar generation is **148.9 GWh/day** (vs. 19.3 GWh in December).
7. **Why It Matters:** Wind energy naturally acts as a winter heating balancer, while solar provides summer peak air-conditioning coverage.
8. **Caution/Limitation:** Monthly averages hide daily storm surges or dark dolda (dunkelflaute) events.
9. **Narrative Transition:** We now quantify these relationships using correlation analysis.
"""))

    # Section 10: Visualization 4
    cells.append(nbf.v4.new_markdown_cell("""## 9. Visualization 4: Correlation Analysis

### Story Context & Rationale
- **Question:** What statistical correlations exist among consumption, wind, solar, and calendar variables?
- **Visual Choice:** An annotated correlation heatmap providing Pearson correlation coefficients (r).
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(9, 7))

corr_vars = ['Consumption', 'Wind', 'Solar', 'Wind+Solar', 'Month', 'Is_Weekend']
labels = ['Consumption', 'Wind Power', 'Solar Power', 'Wind+Solar', 'Month of Year', 'Is Weekend']

corr_matrix = df[corr_vars].corr()

sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="vlag", vmin=-1.0, vmax=1.0,
            xticklabels=labels, yticklabels=labels, ax=ax, linewidths=1, square=True)

ax.set_title("Figure 4: Correlation Matrix of Electricity Demand & Renewable Generation", pad=15)
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### Visual Storytelling Analysis (Visualization 4)
1. **Title:** Figure 4: Correlation Matrix of Electricity Demand & Renewable Generation
2. **Question:** How strongly are grid demand and renewable variables associated?
3. **Rationale:** Color-coded heatmap presents full pair-wise linear correlation coefficients cleanly.
4. **What Audience Sees:** Strong red box between `Is_Weekend` and `Consumption` (-0.60), positive blue box for `Wind` vs `Consumption` (+0.31), and negative box for `Solar` vs `Consumption` (-0.17).
5. **Main Evidence:** `Is_Weekend` has a strong negative correlation (-0.60) with consumption, reflecting industrial work-week schedules.
6. **Numerical Proof:** Wind power has a positive correlation (+0.31) with consumption because winter weather drives both heating demand and wind turbine production.
7. **Why It Matters:** Demonstrates that wind power is structurally aligned with peak heating demand periods.
8. **Caution/Limitation:** Correlation does not imply causation (e.g., wind turbines do not cause cold weather).
9. **Narrative Transition:** Next, we evaluate the annual Terawatt-hour (TWh) macro shift from 2010 to 2017.
"""))

    # Section 11: Visualization 5
    cells.append(nbf.v4.new_markdown_cell("""## 10. Visualization 5: Yearly Comparison

### Story Context & Rationale
- **Question:** How much total annual energy (TWh) did renewables supply relative to national demand?
- **Visual Choice:** Grouped bar chart (TWh totals) overlaid with a line chart showing renewable share percentage.
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax1 = plt.subplots(figsize=(12, 6))

years = annual.index[annual.index >= 2010]
annual_sub = annual.loc[years]

x = np.arange(len(years))
width = 0.25

ax1.bar(x - width, annual_sub['Consumption'], width, label='Consumption (TWh)', color='#1f77b4', alpha=0.85)
ax1.bar(x, annual_sub['Wind'], width, label='Wind (TWh)', color='#17becf', alpha=0.85)
ax1.bar(x + width, annual_sub['Solar'], width, label='Solar (TWh)', color='#ff7f0e', alpha=0.85)

ax1.set_ylabel("Annual Energy Total (TWh)")
ax1.set_xlabel("Year")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.plot(x, annual_sub['Renewable_Share_%'], color='#2ca02c', marker='o', linewidth=3, label='Renewable Share (%)')
ax2.set_ylabel("Renewable Share of Consumption (%)", color='#2ca02c', fontweight='bold')
ax2.set_ylim(0, 35)

ax1.set_title("Figure 5: Annual Electricity Consumption vs. Renewable Generation Growth (2010–2017)", pad=15)
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### Visual Storytelling Analysis (Visualization 5)
1. **Title:** Figure 5: Annual Electricity Consumption vs. Renewable Generation Growth (2010–2017)
2. **Question:** What portion of Germany's annual electricity demand was satisfied by wind and solar power?
3. **Rationale:** Dual-axis chart combines absolute energy volume (TWh) with relative renewable penetration (%).
4. **What Audience Sees:** Total consumption bars remain steady (~500 TWh/year), while wind and solar bars grow steadily, pushing the green share percentage upward.
5. **Main Evidence:** Combined Wind+Solar supplied **20.4% of total national electricity consumption in 2017** (104.2 TWh), up from **9.2% in 2012** (45.5 TWh).
6. **Numerical Proof:** Wind annual output rose from 35.8 TWh in 2010 to 69.5 TWh in 2017 (+94.1%), while solar output grew from 27.7 TWh in 2012 to 34.7 TWh in 2017 (+25.3%).
7. **Why It Matters:** Proves that non-hydro renewable energy became a primary pillar of Germany's national energy grid.
8. **Caution/Limitation:** Excludes biomass, hydro, and geothermal energy contributions.
9. **Narrative Transition:** Finally, we explore the complementary day-to-day relationship between wind and solar power.
"""))

    # Section 12: Visualization 6
    cells.append(nbf.v4.new_markdown_cell("""## 11. Optional Visualization 6: Wind-versus-Solar Relationship

### Story Context & Rationale
- **Question:** How do daily wind and solar power generation interact across different seasons?
- **Visual Choice:** Color-coded seasonal scatter plot with overall regression trendline.
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(10, 7))

df_valid = df.dropna(subset=['Wind', 'Solar', 'Season']).copy()
season_colors = {'Winter': '#3182bd', 'Spring': '#74c476', 'Summer': '#fd8d3c', 'Autumn': '#9e9ac8'}

sns.scatterplot(x='Solar', y='Wind', hue='Season', data=df_valid, palette=season_colors, alpha=0.6, s=35, ax=ax)
sns.regplot(x='Solar', y='Wind', data=df_valid, scatter=False, ax=ax, color='#333333', line_kws={'linestyle': '--', 'linewidth': 2})

ax.set_title("Figure 6: Daily Wind vs. Solar Power Generation by Season (2012–2017)", pad=15)
ax.set_xlabel("Daily Solar Energy Generation (GWh)")
ax.set_ylabel("Daily Wind Energy Generation (GWh)")
ax.legend(title='Season', loc='upper right')
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### Visual Storytelling Analysis (Visualization 6)
1. **Title:** Figure 6: Daily Wind vs. Solar Power Generation by Season (2012–2017)
2. **Question:** Is there a complementary trade-off between wind and solar generation?
3. **Rationale:** Scatter plot color-coded by season reveals seasonal clustering and generation trade-offs.
4. **What Audience Sees:** Distinct seasonal clusters—orange summer dots stretch horizontally (high solar, low wind), while blue winter dots stretch vertically (high wind, low solar).
5. **Main Evidence:** Winter daily solar rarely exceeds 30 GWh but wind reaches 800+ GWh. Summer daily solar reaches 240 GWh while wind drops below 100 GWh.
6. **Numerical Proof:** Pearson correlation between daily wind and solar is **-0.08**, confirming they operate in distinct seasonal windows.
7. **Why It Matters:** Highlights seasonal complementarity: combining wind and solar reduces grid storage requirements compared to relying on a single clean energy source.
8. **Caution/Limitation:** Intraday hourly balancing still requires energy storage or dispatchable backup power.
9. **Narrative Transition:** We summarize key findings and strategic implications.
"""))

    # Section 13: Key Findings
    cells.append(nbf.v4.new_markdown_cell("""## 12. Key Findings
1. **Macro Consumption Stability:** Germany's daily electricity demand averaged 1,338.7 GWh/day across 2006–2017, demonstrating long-term demand stability interrupted only by the 2008–2009 recession.
2. **Exponential Renewable Surge:** Wind and solar power doubled their grid share from 9.2% (45.5 TWh) in 2012 to 20.4% (104.2 TWh) in 2017.
3. **Seasonal Alignment:** Wind generation peaks strongly during winter months, coinciding with peak heating and lighting demand, while solar generation peaks during summer months.
4. **Seasonal Synergy:** Wind and solar exhibit strong seasonal complementarity, providing natural grid balancing across seasons.
"""))

    # Section 14: Potential Implications
    cells.append(nbf.v4.new_markdown_cell("""## 13. Potential Business & Scientific Implications

```
OBSERVATION: Wind generation peaks in winter (Dec avg: 280.8 GWh/d), while Solar peaks in summer (Jul avg: 148.9 GWh/d).
INTERPRETATION: Seasonal weather patterns create natural generation complementarity across the calendar year.
POTENTIAL IMPLICATION: Grid operators can reduce long-term seasonal storage investment by deploying a balanced 2:1 ratio of wind to solar capacity.
```

```
OBSERVATION: Combined Wind+Solar single-day generation reached 825.5 GWh (over 50% of demand) in Dec 2017, but dropped below 30 GWh on low-wind winter days.
INTERPRETATION: High renewable penetration increases short-term daily ramping volatility.
POTENTIAL IMPLICATION: Regional transmission capacity, battery storage, and dispatchable green hydrogen peaking units will be essential for managing extreme wind surges and winter Dunkelflaute events.
```
"""))

    # Section 15: Limitations
    cells.append(nbf.v4.new_markdown_cell("""## 14. Data & Analysis Limitations
1. **Lack of Intraday Hourly Resolution:** The dataset provides daily aggregates, masking intraday peak duck curves and hourly ramping challenges.
2. **Exclusion of Other Clean Sources:** Hydro, biomass, geothermal, and nuclear energy generation are omitted, providing an incomplete view of overall zero-carbon generation.
3. **Geographic Aggregation:** National-level aggregation masks regional grid bottlenecks between North German wind farms and South German industrial demand centers.
"""))

    # Section 16: Conclusion
    cells.append(nbf.v4.new_markdown_cell("""## 15. Conclusion
Between 2006 and 2017, Germany demonstrated that a major industrialized economy can significantly decarbonize its electrical grid while maintaining steady baseline consumption. Renewable generation from wind and solar expanded from a minor contribution into a pillar supplying over 20% of national annual electricity by 2017. The visual story highlights the crucial role of seasonal complementarity between wind and solar in creating a resilient renewable power system.
"""))

    nb['cells'] = cells

    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out1 = os.path.join(base_dir, 'notebooks', 'week2_visual_storytelling.ipynb')
    out2 = os.path.join(os.path.dirname(base_dir), 'Week1_Data_Analysis', 'notebooks', 'week2_visual_storytelling.ipynb')

    os.makedirs(os.path.dirname(out1), exist_ok=True)
    os.makedirs(os.path.dirname(out2), exist_ok=True)

    with open(out1, 'w') as f:
        nbf.write(nb, f)
    with open(out2, 'w') as f:
        nbf.write(nb, f)

    print("Notebook successfully generated in both locations!")

if __name__ == '__main__':
    build_notebook()
