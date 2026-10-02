# Week 2 Data Story Plan: Germany Electricity Consumption & Renewable Energy Transformation (2006–2017)

## 1. Central Story Question
"How has Germany's daily electricity consumption evolved alongside the rapid growth of wind and solar renewable energy generation over the twelve-year period from 2006 to 2017?"

## 2. Target Audience
- **Primary Audience:** Non-technical stakeholders, policymakers, clean energy advocates, and the general public.
- **Visual Design Strategy:** Clean layout, intuitive color encoding (Blue for Consumption, Teal for Wind, Amber for Solar), explicit annotations for key historical events and seasonal shifts, high-resolution formatting, and zero statistical jargon.

## 3. Narrative Structure (The 6-Stage Visual Journey)
1. **Stage 1: Setting the Baseline (Daily Electricity Demand 2006–2017)**
   - Establishes national consumption patterns, highlighting strong weekly/seasonal rhythms and macro events such as the 2008–2009 global financial recession drop.
2. **Stage 2: The Green Energy Surge (Renewable Expansion 2010–2017)**
   - Tracks the expansion of wind (from 2010) and solar (from 2012) power generation across Germany's power grid.
3. **Stage 3: Seasonal Rhythms & Seasonal Shifts**
   - Explores monthly and seasonal dynamics—winter consumption surges vs. summer troughs, contrasted against summer solar peaks and winter wind storms.
4. **Stage 4: Interconnected Grid Dynamics (Correlation Analysis)**
   - Examines how grid variables correlate, helping stakeholders understand weather-driven generation versus temperature and work-week demand drivers.
5. **Stage 5: The Annual Energy Transformation (Yearly Progress TWh)**
   - Quantifies the macro shift in annual terawatt-hours (TWh) produced by wind and solar, charting their rising share in meeting national demand.
6. **Stage 6: The Synergy of Wind and Solar (Complementary Power)**
   - Demonstrates how wind and solar energy naturally balance one another across seasons and days, creating a more resilient renewable mix.

## 4. Key Analytical Questions Answered
1. *What happened to overall electricity consumption over time?* -> Remained overall structurally stable around ~1,338 GWh/day, with weekly cycles and a notable recession dip in 2009 followed by recovery.
2. *How did renewable energy generation change?* -> Grew exponentially; combined Wind+Solar generation increased from ~124 GWh/day in 2012 to over ~272 GWh/day in 2017.
3. *Are there noticeable seasonal patterns?* -> Consumption peaks during cold, dark winter months (Dec–Jan) and drops during summer (Jul–Aug).
4. *How do wind and solar generation behave across seasons?* -> Wind peaks strongly in winter (due to Atlantic storm systems), whereas Solar peaks strongly in summer (due to longer daylight hours).
5. *What relationships exist between consumption and renewable generation?* -> Wind aligns well with high winter demand, while Solar provides clean daytime peak coverage during summer.
6. *What unusual periods or patterns deserve attention?* -> Extreme winter wind events (e.g., Dec 2017 wind storm peaks over 800 GWh/day) and the 2009 economic crisis dip.

## 5. Planned Visualizations & Narrative Roles

| # | Visualization Title | Chart Type | Narrative Purpose | Key Feature / Annotation |
|---|--------------------|------------|-------------------|--------------------------|
| 1 | `01_electricity_consumption_trend.png` | Time-Series Line with 30d & 365d Rolling Averages | Establish baseline consumption trajectory & macro trends | 2009 Financial Crisis Dip & Annual Peaks/Troughs |
| 2 | `02_renewable_generation_trend.png` | Multi-Line / Area Chart | Demonstrate exponential growth of Wind & Solar generation | 2010–2017 Growth Trajectory & Rolling Trendline |
| 3 | `03_seasonal_pattern.png` | Seasonal Box Plots & Monthly Averages | Reveal monthly human rhythm & seasonal weather impacts | Winter Heating Peak vs Summer Solar Surge |
| 4 | `04_correlation_heatmap.png` | Annotated Correlation Heatmap | Quantify relationships between grid demand and renewables | Plain-English correlation coefficients (-1 to +1) |
| 5 | `05_yearly_comparison.png` | Grouped / Stacked Annual Bar Chart (TWh) | Compare total annual electricity generation & renewable share | Annual total energy (TWh) & growth percentages |
| 6 | `06_wind_solar_relationship.png` | Seasonal Scatter Plot with Trendline | Show seasonal complementarity between Wind and Solar | Color-coded seasons showing inverse generation peaks |
