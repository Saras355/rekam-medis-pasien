import datetime
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
existing_data = conn.read( worksheet="Pasien", usecols=list(range(20)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Products
# BUSINESS_TYPES = [
#     "Manufacturer",
#     "Distributor",
#     "Wholesaler",
#     "Retailer",
#     "Service Provider",
# ]
# PRODUCTS = [
#     "Electronics",
#     "Apparel",
#     "Groceries",
#     "Software",
#     "Other",
# ]

# Mendefinisikan batasan tanggal
#tahun_min = 1500
#tahun_ini = datetime.datetime.now()
#tahun_max = tahun_ini.year 
 # Tahun saat ini

# Dropdown button untuk memilih opsi
option = st.selectbox("Select an option", ["Diabetes", "Hipertensi"])
#TES1

# Formulir input untuk Tanggal Lahir

with st.form("pasien_form"):
    if option == "Diabetes":
        st.write("Formulir Diabetes:")
        jenis_penyakit = "Diabetes"
        nama = st.text_input("Nama*")
        #ubah jadi lowercase
        nama = nama.lower()
        no_erm = st.text_input("NoERM*")
        #tanggal_lahir = st.date_input("Tanggal Lahir*")
        tanggal_lahir = st.text_input("Tanggal Lahir* (YYYY-MM-DD)")
        #ubah tanggal lahir ke datetime dalam bentuk yyyy-mm-dd
        tanggal_lahir = pd.to_datetime(tanggal_lahir, format="%Y-%m-%d")
        #tanggal_lahir = datetime.strftime(tanggal_lahir, "%Y-%m-%d")
       # tanggal_lahir = st.date_input("Tanggal Lahir", min_value=None, max_value=None, value=None, key=None)
        #tanggal_lahir = datetime.strptime(tanggal_lahir, "%Y/%m/%d")
        #tanggal_lahir = tanggal_lahir.strftime("%Y-%m-%d")
        #tanggal_lahir = st.date_input("Tanggal Lahir*", min_value=datetime(tahun_min, 1, 1), max_value=datetime(tahun_max, 12, 31))
        jenis_kelamin = st.selectbox("Jenis Kelamin*", ["Laki-laki", "Perempuan"])
        umur = st.number_input("Umur*", min_value=0, max_value=150)
        no_telepon = st.text_input("No Telepon*")
        tanggal_lab = st.date_input("Tanggal Lab*")
        gdp = st.text_input("GDP*")
        gds = st.text_input("GDS*")
        jenis_obat1 = st.text_input("Jenis Obat 1*")
        dosis_obat1 = st.selectbox("Dosis Obat 1*", ["1x1","2x1","3x1","1x3","1x4","2x2","3x2"])
        jenis_obat2 = st.text_input("Jenis Obat 2")
        dosis_obat2 = st.selectbox("Dosis Obat 2", ["1x1","2x1","3x1","1x3","1x4","2x2","3x2"])
        jenis_obat3 = st.text_input("Jenis Obat 3")
        dosis_obat3 = st.selectbox("Dosis Obat 3",  ["1x1","2x1","3x1","1x3","1x4","2x2","3x2"])
        dokter = st.text_input("Dokter*")
        tanggal_konsul = st.date_input("Tanggal Konsultasi*")
        #jenis_penyakit = st.text_input("Jenis Penyakit")

    elif option == "Hipertensi":
        jenis_penyakit = "Hipertensi"
        st.write("Formulir Hipertensi:")
        # username = st.text_input("Username")
        # password = st.text_input("Password", type="password")
        nama = st.text_input("Nama*")
        nama = nama.lower()
        no_erm = st.text_input("NoERM*")
        # tanggal_lahir = st.date_input("Tanggal Lahir*")
        #tanggal_lahir = st.date_input("Tanggal Lahir*", min_value=datetime(tahun_min, 1, 1), max_value=datetime(tahun_max, 12, 31))
        jenis_kelamin = st.selectbox("Jenis Kelamin*", ["Laki-laki", "Perempuan"])
        umur = st.number_input("Umur*", min_value=0, max_value=150)
        no_telepon = st.text_input("No Telepon*")
        tanggal_lab = st.date_input("Tanggal Lab*")
        gdp = st.text_input("GDP*")
        td = st.text_input("TD*")
        jenis_obat1 = st.text_input("Jenis Obat 1*")
        dosis_obat1 = st.selectbox("Dosis Obat 1*", ["1x1","2x1","3x1","1x3","1x4","2x2","3x2"])
        jenis_obat2 = st.text_input("Jenis Obat 2")
        dosis_obat2 = st.selectbox("Dosis Obat 2", ["1x1","2x1","3x1","1x3","1x4","2x2","3x2"])
        dokter = st.text_input("Dokter*")
        tanggal_konsul = st.date_input("Tanggal Konsultasi*")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    # try:
    #     gdp = float(gdp_text)
    #     gds = float(gds_text)
    #     td = float(td_text)
    # except ValueError:
    #     st.warning("Masukkan hanya angka untuk GDP, GDS, dan TD.")
    belum_isi = False
    if not (nama and no_erm and tanggal_lahir and jenis_kelamin and umur and no_telepon and tanggal_lab and jenis_obat1 and dosis_obat1 and dokter and tanggal_konsul):
        # st.warning("Harap isi semua kolom yang diperlukan.")
        belum_isi = True
    if option == "Diabetes":
        if not(gdp and gds):
            belum_isi = True
            
        try:
            gdp = float(gdp)
            gds = float(gds)
        except ValueError:
            st.warning("Masukkan hanya angka untuk GDP, GDS.")
    elif option == "Hipertensi":
        if not(gdp and td):
            belum_isi = True
           # st.warning("Harap isi semua kolom yang diperlukan.")
        try:
            gdp = float(gdp)
            td = float(td)
        except ValueError:
            st.warning("Masukkan hanya angka untuk GDP, TD.")
    if belum_isi:
        st.warning("Harap isi semua kolom yang diperlukan.")
    else:
            # Create a new row of vendor data
            if option == "Diabetes":
                pasien_data = pd.DataFrame(
                    [
                        {
                            "Nama": nama,
                            "NoERM": no_erm,
                            "TanggalLahir": tanggal_lahir.strftime("%Y-%m-%d"),
                            "JenisKelamin": jenis_kelamin,
                            "Umur": umur,
                            "NoTelepon": no_telepon,
                            "TanggalLab": tanggal_lab.strftime("%Y-%m-%d"),
                            "GDP": gdp,
                            "GDS": gds,
                            "TD": None,
                            "JenisObat1": jenis_obat1,
                            "DosisObat1": dosis_obat1,
                            "JenisObat2": jenis_obat2,
                            "DosisObat2": dosis_obat2,
                            "JenisObat3": jenis_obat3,
                            "DosisObat3": dosis_obat3,
                            "Dokter": dokter,
                            "TanggalKonsul": tanggal_konsul.strftime("%Y-%m-%d"),
                            "Jenis Penyakit": jenis_penyakit,
                        }
                    ]
                )
            elif option == "Hipertensi":
                pasien_data = pd.DataFrame(
                    [
                        {
                            "Nama": nama,
                            "NoERM": no_erm,
                            "TanggalLahir": tanggal_lahir.strftime("%Y-%m-%d"),
                            "JenisKelamin": jenis_kelamin,
                            "Umur": umur,
                            "NoTelepon": no_telepon,
                            "TanggalLab": tanggal_lab.strftime("%Y-%m-%d"),
                            "GDP": gdp,
                            "GDS": None,
                            "TD": td,
                            "JenisObat1": jenis_obat1,
                            "DosisObat1": dosis_obat1,
                            "JenisObat2": jenis_obat2,
                            "DosisObat2": dosis_obat2,
                            "JenisObat3": jenis_obat3,
                            "DosisObat3": dosis_obat3,
                            "Dokter": dokter,
                            "TanggalKonsul": tanggal_konsul.strftime("%Y-%m-%d"),
                            "Jenis Penyakit": jenis_penyakit,
                        }
                    ]
                )
            

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, pasien_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Pasien", data=updated_df)

            st.success("Data Pasien berhasil disubmit details successfully submitted!")
        
    
    # if option == "Diabetes":
    #     st.write("Diabetes form submitted with following details:")
    #     st.write("Name:", name)
    #     st.write("Email:", email)
    #     st.write("Age:", age)
    # elif option == "Hipertensi":
    #     st.write("Hipertensi form submitted with following details:")
    #     st.write("Username:", username)
    #     st.write("Password:", password)
#TES1

#TESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# Onboarding New Vendor Form
# with st.form(key="vendor_form"):
#     company_name = st.text_input(label="Company Name*")
#     business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
#     products = st.multiselect("Products Offered", options=PRODUCTS)
#     years_in_business = st.slider("Years in Business", 0, 50, 5)
#     onboarding_date = st.date_input(label="Onboarding Date")
#     additional_info = st.text_area(label="Additional Notes")

#     # Mark mandatory fields
#     st.markdown("**required*")

#     submit_button = st.form_submit_button(label="Submit Vendor Details")

#     # If the submit button is pressed
#     if submit_button:
#         # Check if all mandatory fields are filled
#         if not company_name or not business_type:
#             st.warning("Ensure all mandatory fields are filled.")
#             st.stop()
#         # elif existing_data["CompanyName"].str.contains(company_name).any():
#         #     st.warning("A vendor with this company name already exists.")
#         #     st.stop()
#         else:
#             # Create a new row of vendor data
#             vendor_data = pd.DataFrame(
#                 [
#                     {
#                         "CompanyName": company_name,
#                         "BusinessType": business_type,
#                         "Products": ", ".join(products),
#                         "YearsInBusiness": years_in_business,
#                         "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
#                         "AdditionalInfo": additional_info,
#                     }
#                 ]
#             )

#             # Add the new vendor data to the existing data
#             updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

#             # Update Google Sheets with the new vendor data
#             conn.update(worksheet="Vendors", data=updated_df)

#             st.success("Vendor details successfully submitted!")


# st.subheader("Existing Vendors Data")
# st.write(existing_data)
            
# Additional input form for filtering by company_name

#Anggap aja ada filter buat masukkin 

with st.form(key="filter_form"):
    filter_name = st.text_input(label="Masukkan nama pasien yang dicari")
    filter_name = filter_name.lower()
    filter_no_erm = st.text_input(label="Masukkan NoERM pasien yang dicari")
    filter_button = st.form_submit_button(label="Filter")

# Filter data based on filter_company_name
if filter_button:
   # filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name)) and (existing_data["NoERM"].str.contains(filter_no_erm))]
    filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name)) & (existing_data["NoERM"].str.contains(filter_no_erm))]

    # Display existing vendors data filtered by company_name
    st.subheader(f"Detail Pasien {filter_name}")
    st.write(filtered_data)

    # Line chart based on filtered data
    if not filtered_data.empty:
        st.subheader("Years in Business Over Time (Filtered)")
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_data["TanggalLab"], filtered_data["GDP"], marker='o')
        plt.xlabel("Onboarding Date")
        plt.ylabel("Years in Business")
        plt.title("Years in Business Over Time (Filtered)")
        plt.xticks(rotation=45)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    else:
        st.info("No data available for the provided filter.")

   