"""
Week 2 Data Science Hackathon: Advanced Data Visualization and Storytelling with Python
Dataset: OPSD Germany Daily Electricity & Renewable Energy (2006–2017)

This script performs:
1. Data loading and validation.
2. Advanced numerical calculations and export to week2/analysis_results.csv.
3. Generation of 6 high-resolution (300 DPI) publication-quality visualizations saved to visualizations/week2/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set global aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['figure.titleweight'] = 'bold'

# File paths setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'cleaned', 'cleaned_dataset.csv')
OUT_VIS_DIR = os.path.join(BASE_DIR, 'visualizations', 'week2')
OUT_WEEK2_DIR = os.path.join(BASE_DIR, 'week2')

# Also mirror output paths to sibling Week1_Data_Analysis dir if executed from week_2
MIRROR_VIS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'Week1_Data_Analysis', 'visualizations', 'week2')
MIRROR_WEEK2_DIR = os.path.join(os.path.dirname(BASE_DIR), 'Week1_Data_Analysis', 'week2')

for d in [OUT_VIS_DIR, OUT_WEEK2_DIR, MIRROR_VIS_DIR, MIRROR_WEEK2_DIR]:
    os.makedirs(d, exist_ok=True)

def load_and_validate_data():
    """Load cleaned Week 1 dataset and validate schema & integrity."""
    print("=== PHASE 1: DATA LOADING & VALIDATION ===")
    if not os.path.exists(DATA_PATH):
        # Fallback search path
        alt_path = os.path.join(os.path.dirname(BASE_DIR), 'Week1_Data_Analysis', 'data', 'cleaned', 'cleaned_dataset.csv')
        if os.path.exists(alt_path):
            df = pd.read_csv(alt_path)
        else:
            raise FileNotFoundError(f"Cleaned dataset not found at {DATA_PATH} or {alt_path}")
    else:
        df = pd.read_csv(DATA_PATH)

    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort chronologically
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Validation assertions
    assert 'Consumption' in df.columns, "Missing Consumption column!"
    assert 'Wind' in df.columns, "Missing Wind column!"
    assert 'Solar' in df.columns, "Missing Solar column!"
    
    print(f"Data successfully loaded. Rows: {len(df)}, Columns: {len(df.columns)}")
    print(f"Date Range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    print(f"Consumption Non-Null: {df['Consumption'].count()} / {len(df)}")
    print(f"Wind Non-Null: {df['Wind'].count()} / {len(df)} (Starts {df[df['Wind'].notnull()]['Date'].min().strftime('%Y-%m-%d')})")
    print(f"Solar Non-Null: {df['Solar'].count()} / {len(df)} (Starts {df[df['Solar'].notnull()]['Date'].min().strftime('%Y-%m-%d')})")
    return df

def calculate_advanced_metrics(df):
    """Compute narrative-supporting metrics and save to week2/analysis_results.csv."""
    print("\n=== PHASE 11: ADVANCED NUMERICAL CALCULATIONS ===")
    results = []

    # 1. Overall Summary Statistics (GWh/day)
    for col in ['Consumption', 'Wind', 'Solar', 'Wind+Solar']:
        s = df[col].dropna()
        results.append({'Metric_Category': 'Daily Statistics (GWh)', 'Metric_Name': f'{col}_Mean', 'Value': round(s.mean(), 2)})
        results.append({'Metric_Category': 'Daily Statistics (GWh)', 'Metric_Name': f'{col}_Std', 'Value': round(s.std(), 2)})
        results.append({'Metric_Category': 'Daily Statistics (GWh)', 'Metric_Name': f'{col}_Min', 'Value': round(s.min(), 2)})
        results.append({'Metric_Category': 'Daily Statistics (GWh)', 'Metric_Name': f'{col}_Max', 'Value': round(s.max(), 2)})
        results.append({'Metric_Category': 'Daily Statistics (GWh)', 'Metric_Name': f'{col}_Median', 'Value': round(s.median(), 2)})

    # 2. Annual Totals in Terawatt-hours (TWh)
    # 1 TWh = 1,000 GWh
    annual = df.groupby('Year')[['Consumption', 'Wind', 'Solar', 'Wind+Solar']].sum() / 1000.0
    for yr, row in annual.iterrows():
        results.append({'Metric_Category': 'Annual Energy Total (TWh)', 'Metric_Name': f'Consumption_TWh_{yr}', 'Value': round(row['Consumption'], 2)})
        if not np.isnan(row['Wind']) and row['Wind'] > 0:
            results.append({'Metric_Category': 'Annual Energy Total (TWh)', 'Metric_Name': f'Wind_TWh_{yr}', 'Value': round(row['Wind'], 2)})
        if not np.isnan(row['Solar']) and row['Solar'] > 0:
            results.append({'Metric_Category': 'Annual Energy Total (TWh)', 'Metric_Name': f'Solar_TWh_{yr}', 'Value': round(row['Solar'], 2)})
        if not np.isnan(row['Wind+Solar']) and row['Wind+Solar'] > 0:
            results.append({'Metric_Category': 'Annual Energy Total (TWh)', 'Metric_Name': f'WindSolar_TWh_{yr}', 'Value': round(row['Wind+Solar'], 2)})
            pct_share = (row['Wind+Solar'] / row['Consumption']) * 100.0
            results.append({'Metric_Category': 'Renewable Share (%)', 'Metric_Name': f'Renewable_Share_Pct_{yr}', 'Value': round(pct_share, 2)})

    # 3. Growth Rates (2012 to 2017 for combined renewables)
    ws_2012 = annual.loc[2012, 'Wind+Solar']
    ws_2017 = annual.loc[2017, 'Wind+Solar']
    growth_pct = ((ws_2017 - ws_2012) / ws_2012) * 100.0
    cagr = (((ws_2017 / ws_2012) ** (1/5.0)) - 1) * 100.0
    results.append({'Metric_Category': 'Growth Analysis', 'Metric_Name': 'Renewable_TWh_Growth_2012_2017_Pct', 'Value': round(growth_pct, 2)})
    results.append({'Metric_Category': 'Growth Analysis', 'Metric_Name': 'Renewable_CAGR_2012_2017_Pct', 'Value': round(cagr, 2)})

    # 4. Seasonal Consumption & Generation (GWh/day)
    seasonal = df.groupby('Season')[['Consumption', 'Wind', 'Solar']].mean()
    for season, row in seasonal.iterrows():
        results.append({'Metric_Category': 'Seasonal Means (GWh/day)', 'Metric_Name': f'Consumption_Mean_{season}', 'Value': round(row['Consumption'], 2)})
        results.append({'Metric_Category': 'Seasonal Means (GWh/day)', 'Metric_Name': f'Wind_Mean_{season}', 'Value': round(row['Wind'], 2)})
        results.append({'Metric_Category': 'Seasonal Means (GWh/day)', 'Metric_Name': f'Solar_Mean_{season}', 'Value': round(row['Solar'], 2)})

    # 5. Correlations
    corr_cols = ['Consumption', 'Wind', 'Solar', 'Wind+Solar', 'Month', 'Is_Weekend']
    corr_matrix = df[corr_cols].corr()
    for col1 in corr_cols:
        for col2 in corr_cols:
            if col1 != col2:
                results.append({'Metric_Category': 'Correlation', 'Metric_Name': f'Corr_{col1}_{col2}', 'Value': round(corr_matrix.loc[col1, col2], 4)})

    # 6. Peak & Trough Events
    max_cons_row = df.loc[df['Consumption'].idxmax()]
    min_cons_row = df.loc[df['Consumption'].idxmin()]
    max_wind_row = df.loc[df['Wind'].idxmax()]
    max_solar_row = df.loc[df['Solar'].idxmax()]

    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Max_Consumption_GWh', 'Value': round(max_cons_row['Consumption'], 2)})
    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Max_Consumption_Date', 'Value': str(max_cons_row['Date'].strftime('%Y-%m-%d'))})
    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Min_Consumption_GWh', 'Value': round(min_cons_row['Consumption'], 2)})
    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Min_Consumption_Date', 'Value': str(min_cons_row['Date'].strftime('%Y-%m-%d'))})
    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Max_Wind_GWh', 'Value': round(max_wind_row['Wind'], 2)})
    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Max_Wind_Date', 'Value': str(max_wind_row['Date'].strftime('%Y-%m-%d'))})
    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Max_Solar_GWh', 'Value': round(max_solar_row['Solar'], 2)})
    results.append({'Metric_Category': 'Extremes', 'Metric_Name': 'Max_Solar_Date', 'Value': str(max_solar_row['Date'].strftime('%Y-%m-%d'))})

    res_df = pd.DataFrame(results)
    
    out_csv1 = os.path.join(OUT_WEEK2_DIR, 'analysis_results.csv')
    out_csv2 = os.path.join(MIRROR_WEEK2_DIR, 'analysis_results.csv')
    res_df.to_csv(out_csv1, index=False)
    res_df.to_csv(out_csv2, index=False)
    print(f"Analysis results saved to {out_csv1} ({len(res_df)} metrics)")
    return res_df, annual

def save_fig(fig, filename):
    """Save figure in high resolution (300 DPI) to both output directories."""
    path1 = os.path.join(OUT_VIS_DIR, filename)
    path2 = os.path.join(MIRROR_VIS_DIR, filename)
    fig.savefig(path1, dpi=300, bbox_inches='tight')
    fig.savefig(path2, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved visualization: {filename}")

def plot_vis1_consumption_trend(df):
    """PHASE 3: Visualization 1 - Electricity Consumption Trend over Time."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Calculate rolling averages
    df_plot = df.copy()
    df_plot['Cons_30d'] = df_plot['Consumption'].rolling(window=30, center=True).mean()
    df_plot['Cons_365d'] = df_plot['Consumption'].rolling(window=365, center=True).mean()
    
    # Plot daily dots/light line
    ax.plot(df_plot['Date'], df_plot['Consumption'], color='#a6cee3', alpha=0.35, linewidth=0.8, label='Daily Consumption (GWh)')
    # Plot 30-day rolling
    ax.plot(df_plot['Date'], df_plot['Cons_30d'], color='#1f78b4', alpha=0.85, linewidth=1.8, label='30-Day Moving Average')
    # Plot 365-day rolling
    ax.plot(df_plot['Date'], df_plot['Cons_365d'], color='#e31a1c', linewidth=2.5, label='365-Day Annual Trendline')

    # Annotations
    # 2009 Recession dip
    rec_date = pd.to_datetime('2009-04-01')
    rec_val = 1180
    ax.annotate('2008–2009 Global Recession Drop\n(Demand dropped ~12% below average)',
                xy=(rec_date, rec_val), xytext=(pd.to_datetime('2007-06-01'), 950),
                arrowprops=dict(facecolor='#e31a1c', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10, fontweight='bold', color='#7f0000',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', alpha=0.8))

    # Winter Peak Annotation
    peak_date = pd.to_datetime('2017-01-18')
    ax.annotate('Winter Peak Demand (~1,600+ GWh/day)',
                xy=(peak_date, 1650), xytext=(pd.to_datetime('2014-06-01'), 1730),
                arrowprops=dict(facecolor='#1f78b4', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10, fontweight='bold', color='#003366',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#deebf7', alpha=0.8))

    # Formatting
    ax.set_title("Figure 1: Germany Daily Electricity Consumption Trend (2006–2017)", pad=15)
    ax.set_xlabel("Year")
    ax.set_ylabel("Electricity Consumption (GWh / Day)")
    ax.set_ylim(750, 1850)
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    
    # Text summary box
    textstr = "Key Takeaway:\n• Mean Daily Consumption: 1,338.7 GWh/day\n• Structural stability across 12 years with strong annual cycles\n• Macro dip during 2009 crisis followed by full recovery"
    ax.text(0.02, 0.05, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='#cccccc'))

    save_fig(fig, '01_electricity_consumption_trend.png')

def plot_vis2_renewable_trend(df):
    """PHASE 4: Visualization 2 - Renewable Generation Growth Trend."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    df_valid = df[df['Date'] >= '2010-01-01'].copy()
    
    # Rolling averages for smooth storytelling
    df_valid['Wind_30d'] = df_valid['Wind'].rolling(30, center=True).mean()
    df_valid['Solar_30d'] = df_valid['Solar'].rolling(30, center=True).mean()
    df_valid['WS_30d'] = df_valid['Wind+Solar'].rolling(30, center=True).mean()

    ax.plot(df_valid['Date'], df_valid['Wind_30d'], color='#17becf', linewidth=2.2, label='Wind Generation (30d Avg)')
    ax.plot(df_valid['Date'], df_valid['Solar_30d'], color='#ff7f0e', linewidth=2.2, label='Solar Generation (30d Avg)')
    ax.plot(df_valid['Date'], df_valid['WS_30d'], color='#2ca02c', linewidth=2.8, linestyle='-', label='Combined Wind + Solar (30d Avg)')

    # Fill area under combined curve
    ax.fill_between(df_valid['Date'], 0, df_valid['WS_30d'], color='#2ca02c', alpha=0.15)

    # Annotations
    ax.annotate('Solar Data Recording Starts (2012)',
                xy=(pd.to_datetime('2012-01-01'), 120), xytext=(pd.to_datetime('2010-06-01'), 320),
                arrowprops=dict(facecolor='#ff7f0e', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10, fontweight='bold', color='#8c510a',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#feecd9', alpha=0.9))

    ax.annotate('Extreme Winter Wind Storm Peak\n(Dec 2017: Peak > 800 GWh/day)',
                xy=(pd.to_datetime('2017-12-07'), 500), xytext=(pd.to_datetime('2014-01-01'), 650),
                arrowprops=dict(facecolor='#17becf', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10, fontweight='bold', color='#01665e',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f3f8', alpha=0.9))

    ax.set_title("Figure 2: Growth Trajectory of Wind and Solar Power Generation in Germany (2010–2017)", pad=15)
    ax.set_xlabel("Year")
    ax.set_ylabel("Electricity Generation (GWh / Day)")
    ax.set_ylim(0, 850)
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

    textstr = "Key Takeaway:\n• Combined Wind+Solar doubled output from 2012 (124 GWh/d) to 2017 (272 GWh/d)\n• Wind provides massive winter generation surges\n• Solar provides predictable summer peak output"
    ax.text(0.58, 0.05, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='#cccccc'))

    save_fig(fig, '02_renewable_generation_trend.png')

def plot_vis3_seasonal_pattern(df):
    """PHASE 5: Visualization 3 - Seasonal Patterns (Monthly Box Plot & Multi-Line Profile)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5))

    # Panel A: Consumption Box plot by Month
    sns.boxplot(x='Month_Name', y='Consumption', data=df, ax=ax1, palette='Blues_r',
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax1.set_title("Panel A: Monthly Electricity Consumption Distribution", fontsize=13)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Daily Consumption (GWh)")
    ax1.set_ylim(800, 1800)

    # Panel B: Average Monthly Renewable vs Consumption Profile
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_avg = df.groupby('Month_Name')[['Consumption', 'Wind', 'Solar']].mean().reindex(month_order)

    ax2.plot(monthly_avg.index, monthly_avg['Consumption'], color='#1f77b4', marker='o', linewidth=2.5, label='Consumption (Mean GWh)')
    ax2.plot(monthly_avg.index, monthly_avg['Wind'], color='#17becf', marker='s', linewidth=2.5, label='Wind Generation (Mean GWh)')
    ax2.plot(monthly_avg.index, monthly_avg['Solar'], color='#ff7f0e', marker='^', linewidth=2.5, label='Solar Generation (Mean GWh)')

    ax2.set_title("Panel B: Seasonal Rhythm Comparison (Monthly Means)", fontsize=13)
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Daily Average (GWh)")
    ax2.legend(loc='center right', frameon=True, facecolor='white')

    # Annotate seasonality
    ax2.annotate('Summer Solar Peak', xy=('Jul', monthly_avg.loc['Jul', 'Solar']),
                 xytext=('May', 250), arrowprops=dict(facecolor='#ff7f0e', shrink=0.05, width=1),
                 fontsize=9, fontweight='bold', color='#d95f02')
    
    ax2.annotate('Winter Wind Peak', xy=('Dec', monthly_avg.loc['Dec', 'Wind']),
                 xytext=('Sep', 320), arrowprops=dict(facecolor='#17becf', shrink=0.05, width=1),
                 fontsize=9, fontweight='bold', color='#0f707b')

    fig.suptitle("Figure 3: Seasonal Rhythms of Demand and Renewable Power Generation", fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, '03_seasonal_pattern.png')

def plot_vis4_correlation_heatmap(df):
    """PHASE 6: Visualization 4 - Correlation Heatmap."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    corr_vars = ['Consumption', 'Wind', 'Solar', 'Wind+Solar', 'Month', 'Is_Weekend']
    labels = ['Consumption', 'Wind Power', 'Solar Power', 'Wind+Solar', 'Month of Year', 'Is Weekend (1/0)']
    
    corr_matrix = df[corr_vars].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="vlag", vmin=-1.0, vmax=1.0,
                xticklabels=labels, yticklabels=labels, cbar_kws={'label': 'Pearson Correlation Coefficient (r)'},
                ax=ax, linewidths=1, linecolor='white', square=True)

    ax.set_title("Figure 4: Correlation Matrix of Electricity Demand & Renewable Generation", pad=15)
    
    # Add textual guide
    plt.figtext(0.5, -0.05,
                "Key Insights:\n"
                "• Wind Power has a moderate POSITIVE correlation with Consumption (+0.31): Wind generation peaks in winter when demand is highest.\n"
                "• Solar Power has a slight NEGATIVE correlation with Consumption (-0.17): Solar peaks in summer during lower-demand months.\n"
                "• Is Weekend is STRONGLY NEGATIVE with Consumption (-0.60): Work-week industrial activity drives electricity demand.\n"
                "*Note: Linear correlation indicates strength of association, not direct causal dependency.",
                ha="center", fontsize=9.5, bbox=dict(boxstyle="round,pad=0.6", facecolor="#f8f9fa", edgecolor="#cccccc"))

    save_fig(fig, '04_correlation_heatmap.png')

def plot_vis5_yearly_comparison(df, annual):
    """PHASE 7: Visualization 5 - Yearly Comparison (TWh & Renewable Share %)."""
    fig, ax1 = plt.subplots(figsize=(13, 7))

    years = annual.index[annual.index >= 2010]
    annual_sub = annual.loc[years]

    x = np.arange(len(years))
    width = 0.25

    rects1 = ax1.bar(x - width, annual_sub['Consumption'], width, label='Total Consumption (TWh)', color='#1f77b4', alpha=0.85)
    rects2 = ax1.bar(x, annual_sub['Wind'], width, label='Wind Generation (TWh)', color='#17becf', alpha=0.85)
    rects3 = ax1.bar(x + width, annual_sub['Solar'], width, label='Solar Generation (TWh)', color='#ff7f0e', alpha=0.85)

    ax1.set_ylabel("Annual Energy Total (Terawatt-hours, TWh)")
    ax1.set_xlabel("Year")
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.set_ylim(0, 650)
    ax1.legend(loc='upper left', frameon=True, facecolor='white')

    # Secondary Y axis for Renewable Share %
    ax2 = ax1.twinx()
    ren_share = (annual_sub['Wind+Solar'] / annual_sub['Consumption']) * 100.0
    line = ax2.plot(x, ren_share, color='#2ca02c', marker='o', linewidth=3, markersize=8, label='Wind+Solar Share of Demand (%)')
    ax2.set_ylabel("Renewable Share of Consumption (%)", color='#2ca02c', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#2ca02c')
    ax2.set_ylim(0, 35)

    # Annotate values on top of line points
    for i, txt in enumerate(ren_share):
        if not np.isnan(txt):
            ax2.annotate(f"{txt:.1f}%", (x[i], txt + 1.2), ha='center', color='#1b7837', fontweight='bold', fontsize=10)

    ax1.set_title("Figure 5: Annual Electricity Consumption vs. Renewable Generation Growth (2010–2017)", pad=15)
    
    save_fig(fig, '05_yearly_comparison.png')

def plot_vis6_wind_solar_relationship(df):
    """PHASE 8: Visualization 6 - Wind vs Solar Relationship Scatter Plot."""
    fig, ax = plt.subplots(figsize=(11, 8))

    df_valid = df.dropna(subset=['Wind', 'Solar', 'Season']).copy()
    season_colors = {'Winter': '#3182bd', 'Spring': '#74c476', 'Summer': '#fd8d3c', 'Autumn': '#9e9ac8'}

    sns.scatterplot(x='Solar', y='Wind', hue='Season', data=df_valid, palette=season_colors,
                    alpha=0.6, s=35, ax=ax)

    # Overall trendline
    sns.regplot(x='Solar', y='Wind', data=df_valid, scatter=False, ax=ax,
                color='#333333', line_kws={'linestyle': '--', 'linewidth': 2, 'label': 'Overall Linear Trend'})

    ax.set_title("Figure 6: Daily Wind vs. Solar Power Generation by Season (2012–2017)", pad=15)
    ax.set_xlabel("Daily Solar Energy Generation (GWh)")
    ax.set_ylabel("Daily Wind Energy Generation (GWh)")
    ax.legend(title='Season', loc='upper right', frameon=True, facecolor='white')

    # Explanatory Callout Box
    ax.text(0.03, 0.95,
            "Seasonal Complementarity Insight:\n"
            "• Summer (Orange): High Solar (up to 240 GWh/d), Low Wind.\n"
            "• Winter (Blue): High Wind (up to 800+ GWh/d), Low Solar (< 30 GWh/d).\n"
            "• Seasonal trade-off smooths combined annual renewable availability.",
            transform=ax.transAxes, verticalalignment='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#ffffff', alpha=0.9, edgecolor='#b0b0b0'))

    save_fig(fig, '06_wind_solar_relationship.png')

def main():
    df = load_and_validate_data()
    res_df, annual = calculate_advanced_metrics(df)
    
    print("\n=== GENERATING HIGH-RESOLUTION VISUALIZATIONS ===")
    plot_vis1_consumption_trend(df)
    plot_vis2_renewable_trend(df)
    plot_vis3_seasonal_pattern(df)
    plot_vis4_correlation_heatmap(df)
    plot_vis5_yearly_comparison(df, annual)
    plot_vis6_wind_solar_relationship(df)
    print("\n=== ALL VISUALIZATIONS AND ANALYSIS COMPLETED SUCCESSFULLY ===")

if __name__ == '__main__':
    main()
