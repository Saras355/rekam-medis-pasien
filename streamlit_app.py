import datetime
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Rekam Medis Pasien", 
    page_icon="📊",  
)
selected = option_menu(
    menu_title=None,
    options=["Input Data Pasien", "Cari Rekam Medis"],
    icons=["📝", "🔍"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
if selected == "Input Data Pasien":
        
    # Display Title and Description
    st.title("Pendataan Pasien Diabetes dan Hipertensi")
    #st.markdown("Enter the details of the new vendor below.")
    st.write(st.secrets['connections'])
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read( worksheet="Pasien", usecols=list(range(20)), ttl=5)
    existing_data = existing_data.dropna(how="all")


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
            tanggal_lahir = st.text_input("Tanggal Lahir* (YYYY-MM-DD)")
            # tanggal_lahir = pd.to_datetime(tanggal_lahir, format="%Y-%m-%d")
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
            tanggal_lahir = st.text_input("Tanggal Lahir* (YYYY-MM-DD)")
            #ubah tanggal lahir ke datetime dalam bentuk yyyy-mm-dd
            # tanggal_lahir = pd.to_datetime(tanggal_lahir, format="%Y-%m-%d")
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
        #nomor telepon harus angka 
        #no erm harus angka

        # try :
        #     no_erm = int(no_erm)
        #     no_telepon = int(no_telepon)
        # except ValueError:
        #     st.warning("Masukkan hanya angka untuk NoERM dan No Telepon.")
    
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
                st.stop()
        elif option == "Hipertensi":
            if not(gdp and td):
                belum_isi = True
            # st.warning("Harap isi semua kolom yang diperlukan.")
            try:
                gdp = float(gdp)
                td = float(td)
            except ValueError:
                st.warning("Masukkan hanya angka untuk GDP, TD.")
                st.stop()
        
        # Validasi nomor telepon harus angka
        try:
            int(no_telepon)
        except ValueError:
            st.warning("Nomor telepon harus berupa angka.")
            st.stop()

        # Validasi tanggal lahir sesuai format
        try:
            tanggal_lahir = pd.to_datetime(tanggal_lahir, format="%Y-%m-%d")
        except ValueError:
            st.warning("Tanggal lahir harus dalam format YYYY-MM-DD.")
            st.stop()
        
        #cek bahwa no_erm harus unik 
        if no_erm in existing_data["NoERM"].values:
            st.warning("Nomor pasien sudah ada dalam basis data. Harap masukkan nomor pasien yang unik.")
            st.stop()

        #belum isi 
        if belum_isi:
            st.warning("Harap isi semua kolom yang diperlukan.")
            st.stop()
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
            

       # st.form(key="pasien_form").clear()
    with st.form(key="filter_form"):
        filter_name = st.text_input(label="Masukkan nama pasien yang dicari")
        filter_name = filter_name.lower()
        filter_no_erm = st.text_input(label="Masukkan NoERM pasien yang dicari")
        #filter_no_erm = float(filter_no_erm)
        filter_button = st.form_submit_button(label="Cari")

    # Filter data based on filter_company_name
    if filter_button:
        print(existing_data["Nama"])
        print(filter_name)
        print(existing_data["NoERM"])
        print(filter_no_erm)

    # filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name)) and (existing_data["NoERM"].str.contains(filter_no_erm))]
        filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name)) &(existing_data["NoERM"].astype(str).str.contains(filter_no_erm))]
        filtered_data = filtered_data.sort_values(by="TanggalLab", ascending=False).head(7)
    #filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name))]
        #filtered_data = existing_data[(existing_data["NoERM"].astype(str).str.contains(filter_no_erm))]
        # Display existing vendors data filtered by company_name
        st.subheader(f"Detail Pasien {filter_name}")
        #filtered_data = str(filtered_data["GDP"])
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
        #st.form(key="filter_form").clear()
    
elif selected == "Cari Rekam Medis":
    # Display Title and Description
    st.title("Pendataan Pasien Diabetes dan Hipertensi")
    #st.markdown("Enter the details of the new vendor below.")
    # st.write(st.secrets['connections'])
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read( worksheet="Pasien", usecols=list(range(20)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    with st.form(key="filter_form"):
        filter_name = st.text_input(label="Masukkan nama pasien yang dicari")
        filter_name = filter_name.lower()
        filter_no_erm = st.text_input(label="Masukkan NoERM pasien yang dicari")
        #filter_no_erm = float(filter_no_erm)
        filter_button = st.form_submit_button(label="Cari")

    # Filter data based on filter_company_name
    if filter_button:
        print(existing_data["Nama"])
        print(filter_name)
        print(existing_data["NoERM"])
        print(filter_no_erm)

    # filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name)) and (existing_data["NoERM"].str.contains(filter_no_erm))]
        filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name)) &(existing_data["NoERM"].astype(str).str.contains(filter_no_erm))]
        filtered_data = filtered_data.sort_values(by="TanggalLab", ascending=False).head(7)
    #filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name))]
        #filtered_data = existing_data[(existing_data["NoERM"].astype(str).str.contains(filter_no_erm))]
        # Display existing vendors data filtered by company_name
        st.subheader(f"Detail Pasien {filter_name}")
        #filtered_data = str(filtered_data["GDP"])
        st.write(filtered_data)

        if filtered_data['Jenis Penyakit'].iloc[0] == "Diabetes":
            # Line chart based on filtered data
            if not filtered_data.empty:
               # st.subheader("Years in Business Over Time (Filtered)")
                plt.figure(figsize=(10, 6))

                # Plot GDP
                plt.plot(filtered_data["TanggalLab"], filtered_data["GDP"], marker='o', color='blue', label='GDP')
                
                # Plot GDS
                plt.plot(filtered_data["TanggalLab"], filtered_data["GDS"], marker='o', color='green', label='GDS')

                plt.xlabel("Tanggal Lab")
                plt.ylabel("Nilai")
                #plt.title("Years in Business Over Time (Filtered)")
                plt.xticks(rotation=45)
                plt.legend()  # Menampilkan legenda

                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
            else:
                st.info("No data available for the provided filter.")
        else: 
               # Line chart based on filtered data
            if not filtered_data.empty:
              #  st.subheader("Years in Business Over Time (Filtered)")
                plt.figure(figsize=(10, 6))

                # Plot GDP
                plt.plot(filtered_data["TanggalLab"], filtered_data["GDP"], marker='o', color='blue', label='GDP')
                
                # Plot GDS
                plt.plot(filtered_data["TanggalLab"], filtered_data["TD"], marker='o', color='green', label='GDS')

                plt.xlabel("Tanggal Lab")
                plt.ylabel("Nilai")
                #plt.title("Years in Business Over Time (Filtered)")
                plt.xticks(rotation=45)
                plt.legend()  # Menampilkan legenda

                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
            else:
                st.info("No data available for the provided filter.")
      #  st.form(key="filter_form").clear()
