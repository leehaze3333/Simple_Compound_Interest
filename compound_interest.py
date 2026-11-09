# ============================================================
# Compound Interest Calculator - a simple Streamlit web app
# ============================================================
# The user enters:
#   1. An initial deposit (the money you start with)
#   2. A yearly deposit (extra money added at the end of each year)
#   3. A yearly interest rate (in percent)
#   4. A number of years
# The app then shows the final balance, how much of it came
# from interest, a year-by-year table and a growth chart.
#
# Interest is compounded once per year. Each year:
#   new balance = old balance + interest + yearly deposit
# ============================================================


# ------------------------------------------------------------
# SECTION 1: Import the libraries we need
# ------------------------------------------------------------
import streamlit as st   # builds the web page
import pandas as pd      # makes tables (comes installed with streamlit)


# ------------------------------------------------------------
# SECTION 2: Page settings
# ------------------------------------------------------------
st.set_page_config(
    page_title="Compound Interest Calculator",
    page_icon="💰",
    layout="centered",
)


# ------------------------------------------------------------
# SECTION 3: The calculation function
# ------------------------------------------------------------
# This function does all the math. It goes through the years
# one at a time and records what happened in each year.
def calculate_growth(initial_deposit, yearly_deposit, rate_percent, years):
    """Return a list of rows, one per year, describing the balance."""
    rate = rate_percent / 100      # turn 5 (percent) into 0.05
    balance = initial_deposit      # start with the initial deposit
    total_deposited = initial_deposit
    rows = []                      # an empty list we will fill up

    # Year 0 = the starting point, before any interest
    rows.append({
        "Year": 0,
        "Interest earned this year": 0.0,
        "Deposit this year": initial_deposit,
        "Total deposited": total_deposited,
        "Balance": balance,
    })

    # "for year in range(1, years + 1)" repeats the code inside
    # once for each year: 1, 2, 3 ... up to the last year.
    for year in range(1, years + 1):
        interest = balance * rate          # interest earned this year
        balance = balance + interest       # add the interest
        balance = balance + yearly_deposit # add the yearly deposit
        total_deposited = total_deposited + yearly_deposit

        rows.append({
            "Year": year,
            "Interest earned this year": interest,
            "Deposit this year": yearly_deposit,
            "Total deposited": total_deposited,
            "Balance": balance,
        })

    return rows


# ------------------------------------------------------------
# SECTION 4: Page header
# ------------------------------------------------------------
st.title("💰 Compound Interest Calculator")
st.write(
    "See how your money grows over time with an initial deposit, "
    "a yearly deposit and a yearly interest rate."
)
st.divider()


# ------------------------------------------------------------
# SECTION 5: User inputs
# ------------------------------------------------------------
# Two columns so the four inputs sit neatly in a 2 x 2 grid.
left, right = st.columns(2)

with left:
    initial_deposit = st.number_input(
        "Initial deposit ($)",
        min_value=0.0,      # no negative money
        value=1000.0,       # starting value shown in the box
        step=100.0,
        format="%.2f",
    )
    yearly_rate = st.number_input(
        "Yearly interest rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5,
        format="%.2f",
    )

with right:
    yearly_deposit = st.number_input(
        "Yearly deposit ($)",
        min_value=0.0,
        value=500.0,
        step=100.0,
        format="%.2f",
        help="Money you add at the end of every year.",
    )
    years = st.number_input(
        "Number of years",
        min_value=1,        # whole numbers only, at least 1
        max_value=100,
        value=10,
        step=1,
    )


# ------------------------------------------------------------
# SECTION 6: Run the calculation
# ------------------------------------------------------------
rows = calculate_growth(initial_deposit, yearly_deposit, yearly_rate, int(years))

# The last row holds the final numbers.
final_row = rows[-1]
final_balance = final_row["Balance"]
total_deposited = final_row["Total deposited"]
total_interest = final_balance - total_deposited


# ------------------------------------------------------------
# SECTION 7: Show the headline results
# ------------------------------------------------------------
st.divider()
st.subheader(f"After {int(years)} years")

col1, col2, col3 = st.columns(3)
# ":,.2f" adds commas and 2 decimal places, e.g. 12,345.67
col1.metric("Final balance", f"${final_balance:,.2f}")
col2.metric("Total deposited", f"${total_deposited:,.2f}")
col3.metric("Interest earned", f"${total_interest:,.2f}")


# ------------------------------------------------------------
# SECTION 8: Growth chart
# ------------------------------------------------------------
st.subheader("📈 Growth over time")

# Turn our list of rows into a pandas table ("DataFrame").
table = pd.DataFrame(rows)

# The chart shows two lines: money you put in vs. total balance.
chart_data = table.set_index("Year")[["Total deposited", "Balance"]]
st.line_chart(chart_data)


# ------------------------------------------------------------
# SECTION 9: Year-by-year table
# ------------------------------------------------------------
st.subheader("📋 Year-by-year breakdown")

# Show every money column as $1,234.56
money_columns = ["Interest earned this year", "Deposit this year",
                 "Total deposited", "Balance"]
st.dataframe(
    table.style.format({col: "${:,.2f}" for col in money_columns}),
    hide_index=True,
    width="stretch",    # make the table fill the page width
)


# ------------------------------------------------------------
# SECTION 10: Show the formula
# ------------------------------------------------------------
st.subheader("📐 Formula used")
st.latex(r"FV = P(1+r)^n + D \cdot \frac{(1+r)^n - 1}{r}")
st.caption(
    "P = initial deposit, D = yearly deposit, r = yearly rate (as a decimal), "
    "n = number of years. Interest compounds once a year, and each yearly "
    "deposit is added at the end of the year."
)
