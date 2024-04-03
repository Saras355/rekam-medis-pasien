import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt

# Display Title and Description
st.title("Vendor Management Portal")
st.markdown("Enter the details of the new vendor below.")
# st.write(st.secrets['connections'])
# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read( worksheet="Vendors", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Products
BUSINESS_TYPES = [
    "Manufacturer",
    "Distributor",
    "Wholesaler",
    "Retailer",
    "Service Provider",
]
PRODUCTS = [
    "Electronics",
    "Apparel",
    "Groceries",
    "Software",
    "Other",
]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    company_name = st.text_input(label="Company Name*")
    business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
    products = st.multiselect("Products Offered", options=PRODUCTS)
    years_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Additional Notes")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Vendor Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not company_name or not business_type:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        # elif existing_data["CompanyName"].str.contains(company_name).any():
        #     st.warning("A vendor with this company name already exists.")
        #     st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "CompanyName": company_name,
                        "BusinessType": business_type,
                        "Products": ", ".join(products),
                        "YearsInBusiness": years_in_business,
                        "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                        "AdditionalInfo": additional_info,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Vendors", data=updated_df)

            st.success("Vendor details successfully submitted!")


# st.subheader("Existing Vendors Data")
# st.write(existing_data)
            
# Additional input form for filtering by company_name
with st.form(key="filter_form"):
    filter_company_name = st.text_input(label="Enter Company Name to Filter")
    filter_button = st.form_submit_button(label="Filter")

# Filter data based on filter_company_name
if filter_button:
    filtered_data = existing_data[existing_data["CompanyName"].str.contains(filter_company_name)]

    # Display existing vendors data filtered by company_name
    st.subheader("Filtered Vendors Data")
    st.write(filtered_data)

    # Line chart based on filtered data
    if not filtered_data.empty:
        st.subheader("Years in Business Over Time (Filtered)")
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_data["OnboardingDate"], filtered_data["YearsInBusiness"], marker='o')
        plt.xlabel("Onboarding Date")
        plt.ylabel("Years in Business")
        plt.title("Years in Business Over Time (Filtered)")
        plt.xticks(rotation=45)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    else:
        st.info("No data available for the provided filter.")

   