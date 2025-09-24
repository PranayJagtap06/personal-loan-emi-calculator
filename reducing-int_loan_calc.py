#!/home/mage/miniconda3/envs/ml_env/bin/ python3
"""reducing_int_loan_calc.py."""

import numpy as np
import pandas as pd
import streamlit as st
from typing import Optional
from openpyxl import Workbook

def reducing_intrest_loan_calc(principle_amt: float, interest_rate: float, months_time: Optional[int] = None, emi: Optional[float] = None, save_file: bool = False):
    """Reducing interest rate loan calculator."""
    monthly_int_rate = (interest_rate/100)/12
    if months_time is None:
        months_time = int(np.ceil(np.divide(np.log(np.divide(emi, np.subtract(
            emi, principle_amt*monthly_int_rate))), np.log(1+monthly_int_rate))))
    if emi is None:
        emi = round(np.divide(np.multiply(np.multiply(principle_amt, monthly_int_rate), np.pow(
            1 + monthly_int_rate, months_time)), np.pow(1 + monthly_int_rate, months_time - 1)), 2)

    print(f"{principle_amt=}\ninterest_rate={interest_rate}%\n{months_time=}\n")
    new_principle: float = principle_amt  # Principle amount remaining after paying EMI

    no_tab = int(np.round((len('Sr. No.')+10)/2))
    # print(no_tab)
    principle_tab = int(np.round((max(len(str(principle_amt)), len('Priciple'))+15)/2, decimals=0))
    # print(principle_tab)
    emi_tab = int(np.round((max(len(str(emi)), len('EMI'))+15)/2, decimals=0))
    # print(emi_tab)
    interest_tab = int((len('Interest')+15)/2)
    # print(interest_tab)
    pay_to_principle = int((len("Payment to Principle Amt")+12/2))
    # print(pay_to_principle)

    logs1 = f"|{'Sr. No.': ^{no_tab}}|{'Principle': ^{principle_tab}}|{'EMI': ^{emi_tab}}|{
        'Interest': ^{interest_tab}}|{'Payment to Principle Amt': ^{pay_to_principle}}|"
    print(logs1)
    dashes = f"|{'':-^{len(f'{'Sr. No.': ^{no_tab}}|{'Principle': ^{principle_tab}}|{'EMI': ^{emi_tab}}|{
                           'Interest': ^{interest_tab}}|{'Payment to Principle Amt': ^{pay_to_principle}}')}}|"
    print(dashes)

    interest_array = np.array([])
    pay_to_principle_array = np.array([])

    workbook = Workbook()
    sheet = workbook.active

    sheet.append({'A': 'Sr. No.', 'B': 'Principle', 'C': 'EMI', 'D': 'Interest', 'E': 'Principle Pay'})

    for t in np.arange(months_time):
        interest: float = round(np.multiply(new_principle, monthly_int_rate), 2)  # Interest to be deducted from EMI
        interest_array = np.append(interest_array, interest)
        pay_principle: float = round(np.subtract(emi, interest), 2)  # Amount to be paid towards principle amount
        pay_to_principle_array = np.append(pay_to_principle_array, pay_principle)

        sheet.append({'A': t+1, 'B': new_principle, 'C': emi, 'D': interest, 'E': pay_principle})

        logs2 = f"|{str(t+1): ^{no_tab}}|{new_principle: ^{principle_tab}}|{emi: ^{emi_tab}}|{
            interest: ^{interest_tab}}|{pay_principle: ^{pay_to_principle}}|"
        print(logs2)

        new_principle = int(np.subtract(new_principle, pay_principle))

    sheet.merged_cells.ranges = (f'A{months_time+1}', f'B{months_time+1}')
    sheet.append({'A': 'Grand Total', 'C': round(emi*months_time, 2),
                 'D': round(interest_array.sum(), 2), 'E': round(pay_to_principle_array.sum(), 2)})
    
    print(dashes)
    logs3 = f"|{' Grand Total ': ^{no_tab+principle_tab+1}}|{'₹'+str(round(emi*months_time, 2)): ^{emi_tab}}|{'₹'+str(
        round(interest_array.sum(), 2)): ^{interest_tab}}|{'₹'+str(round(pay_to_principle_array.sum(), 2)): ^{pay_to_principle}}|"
    print(logs3)
    print(dashes)

    # if save_file:
    file_path = workbook.save(f'reducing_interest_rate_loan_sheet-₹{principle_amt}-{months_time}yrs.xlsx')
    df = pd.read_excel()

    return df


# Setup page
about: str = """# Personal Loan EMI Calculator with Reducing Interest Rate
This application calculates the Equated Monthly Installment (EMI) for a personal loan with a reducing interest rate. It provides a detailed breakdown of payments over the loan tenure and allows users to save the payment schedule as an Excel file.
"""

st.set_page_config(
    page_title="Personal Loan EMI Calculator with Reducing Interest Rate",
    page_icon="💸",
    menu_items={
        "About": about
    }
)

st.title(body="Looking for a personal loan? ")
st.markdown(body="*But confused how long your EMI breakdown will be 🤔? Our Personal Loan EMI Calculator is at Your Service...*")

prncpl_amt: float = st.number_input(
    "Principal Loan Amount (₹)",
    min_value=10_000.0,
    max_value=1_00_00_000.0,
    value=100_000.0,
    step=1000.0,
    help="Enter the total amount of the loan you wish to take.",
)

interest_rate: float = st.number_input(
    "Interest Rate (%)",
    min_value=6.0,
    max_value=18.0,
    value=9.5,
    step=0.1,
    help="Percentage of interest charged on the loan amount per annum.",
)

tenure: int = st.number_input(
    "Loan Tenure (in months)",
    min_value=12,
    max_value=12*50,
    value=34,
    step=2,
    help="Percentage of interest charged on the loan amount per annum.",
)

emi: float = st.number_input(
    "EMI Amount (₹)",
    min_value=1000.0,
    max_value=1_00_00_000.0,
    value=3500.0,
    step=500.0,
    help="Enter the EMI amount you can afford to pay each month.",
)

calc_tenure: bool = st.checkbox(label="Calculate Loan Tenure for an EMI Amount (₹)", value=False, help="Check this box if you want to calculate the Loan Tenure based on the principal amount, interest rate, and EMI. Leave it unchecked if you want to calculate your EMI.")

# if __name__ == "__main__":
#     reducing_intrest_loan_calc(200000.0, 9.5, 36)


if st.button(label="Calculate EMI Breakdown"):
    if calc_tenure:
        df = reducing_intrest_loan_calc(prncpl_amt, interest_rate, emi=emi, save_file=True)
    else:
        df = reducing_intrest_loan_calc(prncpl_amt, interest_rate, months_time=tenure, save_file=True)
    st.success("EMI Breakdown calculated and saved as Excel file successfully!")
    st.dataframe(data=df)
    st.markdown("You can find the Excel file in the current working directory.")


# Disclaimer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("-----")
st.write("""**Disclaimer:** This is app is for educational purposes only. The calculations provided are estimates and may not reflect actual loan terms or conditions. Please consult with a financial advisor or lending institution for precise information.""")



# Create the HTML for the circular image
st.markdown(
    """
    ------
    <style>
        a.author {
            text-decoration: none;
            color: #F14848;
        }
        a.author:hover {
            text-decoration: none;
            color: #14a3ee;
        }
    </style>
    <p><em>Created with</em> ❤️ <em>by <a class='author' href='https://pranayjagtap.netlify.app' rel=noopener noreferrer' target='_blank'><b>Pranay Jagtap</b></a></em></p>
    """,
    unsafe_allow_html=True
)
