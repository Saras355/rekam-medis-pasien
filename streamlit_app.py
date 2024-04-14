import datetime
import time
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from streamlit_js_eval import streamlit_js_eval


st.set_page_config(
    page_title="Rekam Medis Pasien", 
    page_icon="📊",  
)

obat_options = {
    "Metformin (500-3000 mg)": ["1x1", "2x1", "3x1", "3x2"],
    "Glimepiride (1-8 mg)": ["1x1 mg", "1x2 mg", "1x3 mg", "1x4 mg", "1x5 mg", "1x6 mg", "1x7 mg", "1x8 mg"],
    "Glibenclamide (2.5-20 mg)": ["1x5 mg", "1x10 mg", "1x15 mg","1x20 mg"]
}
obat_hipertensi_options = {
    "Captopril (12,5 - 150 mg/hari)": ["2x12,5 mg", "3x12,5 mg", "2x25 mg", "3x25 mg", "2x50 mg", "3x50 mg"],
    "Amlodipine (2,5 - 10mg/hari)": ["1x2,5 mg", "1x5 mg", "1x10 mg"],
    "Furosemide (20 - 80mg/hari)": ["2x20 mg", "2x40 mg"],
    "Hidroklorothiazid (25 - 50mg/hari)": ["1x25 mg", "1x50 mg"]
}
true_list = [False, False]

selected = option_menu(
    menu_title=None,
    options=["Input Data Pasien", "Input Data Diabetes", "Input Data Hipertensi", "Cari Rekam Medis"],
    icons=["📝", "🔍", "🔍", "🔍"],
    menu_icon="cast",
    default_index=0,
    orientation="vertical",
)

if selected == "Input Data Pasien":
    st.title("Pendataan Pasien Diabetes dan Hipertensi")
    
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Fetch existing pasien data
    existing_pasien_data = conn.read(worksheet="data_pasien", usecols=list(range(2)), ttl=5)
    existing_pasien_data = existing_pasien_data.dropna(how="all")
    
    with st.form(key="pasien_form", clear_on_submit=True):
        st.write("Formulir Data Pasien:")
        nama = st.text_input("Nama*")
        nama = nama.lower()
        no_erm = st.text_input("No eRM*", help="Harap isi dengan nomor pasien yang unik.")
        tanggal_lahir = st.text_input("Tanggal Lahir* (DD-MM-YYYY)")
        jenis_kelamin = st.selectbox("Jenis Kelamin*", ["Laki-laki", "Perempuan"])
        no_telepon = st.text_input("No Telepon*", placeholder="(08xxxxxxxxxx)")
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            # Validasi
            if not (nama and no_erm and tanggal_lahir and jenis_kelamin and no_telepon):
                st.warning("Harap isi semua kolom yang diperlukan.")
                st.stop()
                
            # Validasi tanggal lahir sesuai format
            try:
                tanggal_lahir = datetime.datetime.strptime(tanggal_lahir, "%d-%m-%Y")
            except ValueError:
                st.warning("Tanggal lahir harus dalam format DD-MM-YYYY.")
                st.stop()
            
            # Validasi nomor telepon harus angka
            # try:
            #     int(no_telepon)
            # except ValueError:
            #     st.warning("Nomor telepon harus berupa angka.")
            #     st.stop()
                
            def is_valid_telephone_number(phone_number):
                valid_prefixes = ["08"]  # Angka awalan yang diizinkan
                return any(phone_number.startswith(prefix) for prefix in valid_prefixes)

            # Masukkan nomor telepon dari pengguna
            no_telepon = st.text_input("Nomor Telepon")

            # Validasi nomor telepon
            if not no_telepon:
                st.warning("Nomor telepon tidak boleh kosong.")
                st.stop()
            elif not no_telepon.isdigit():
                st.warning("Nomor telepon harus berupa angka.")
                st.stop()
            elif not is_valid_telephone_number(no_telepon):
                st.warning("Nomor telepon harus dimulai dengan angka 08.")
                st.stop()
            # Validasi NoERM unik
            if no_erm in existing_pasien_data["NoERM"].values:
                st.warning("Nomor pasien sudah ada dalam basis data. Harap masukkan nomor pasien yang unik.")
                st.stop()
            
            # Buat dataframe untuk data pasien baru
            pasien_data = pd.DataFrame(
                {
                    "Nama": [nama],
                    "NoERM": [no_erm],
                    "TanggalLahir": [tanggal_lahir.strftime("%Y-%m-%d")],
                    "JenisKelamin": [jenis_kelamin],
                    "NoTelepon": [no_telepon]
                }
            )
            
            # Update Google Sheets dengan data pasien baru
            updated_pasien_df = pd.concat([existing_pasien_data, pasien_data], ignore_index=True)
            conn.update(worksheet="data_pasien", data=updated_pasien_df)
            st.success("Data pasien berhasil disubmit!")

elif selected in ["Input Data Diabetes", "Input Data Hipertensi"]:

    
    jenis_penyakit = "Diabetes" if selected == "Input Data Diabetes" else "Hipertensi"
    
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)
    if 'my_variable_state' not in st.session_state:
        st.session_state.my_variable_state = 0
    
    if 'my_variable_state2' not in st.session_state:
        st.session_state.my_variable_state2 = 0
        st.session_state.my_variable_state3 = 0
    
    if 'selected_obat' not in st.session_state:
        st.session_state.selected_obat = None
        st.session_state.selected_obat_hipertensi = None
        st.no_erm_input = None
        st.tanggal_lab = None
        st.dokter = None
        st.tanggal_konsul = None
        st.gdp = None
        st.gds = None
        st.td_sistol = None
        st.td_diastol = None
        st.selected_dosis = None
        st.selected_dosis_hipertensi = None
        st.pasien_data = None
        
    # Fetch existing pasien data
    existing_pasien_data = conn.read(worksheet="data_pasien", usecols=list(range(2)), ttl=5)
    existing_pasien_data = existing_pasien_data.dropna(how="all")
    def form1():
        with st.form(key ="data_form", clear_on_submit= True):
            verif_data = None
        
            
            st.write(f"Formulir {jenis_penyakit}:")
            st.write("**Langkah 1. Masukkan No eRM Pasien**")
            st.no_erm_input = st.text_input("No eRM*", help="Masukkan NoERM pasien.")
            
            nama_pasien = None
            submit_button = st.form_submit_button("Submit Langkah 1")
            if submit_button:
                st.session_state.my_variable_state += 1
                if st.no_erm_input:
                    nama_pasien = existing_pasien_data.loc[existing_pasien_data["NoERM"] == st.no_erm_input, "Nama"].values
                if nama_pasien:
                    st.write(f"Nama Pasien: {nama_pasien[0]}")
                    
                    #st.write(submit_button)
                    verif_data = True
                elif st.no_erm_input == "":
                    st.warning("NoERM tidak boleh kosong.")
                    st.stop()

                else:
                    st.warning("NoERM tidak ditemukan.")
                    st.stop()
    def form2():
        if st.session_state.my_variable_state >= 1:
            with st.form(key="data_form2", clear_on_submit= True):
                st.write("**Langkah 2. Masukkan data dokter dan tanggal konsultasi dan lab**")
                st.tanggal_lab = st.date_input("Tanggal Lab*")
                st.dokter = st.selectbox("Dokter*", ["dr. I Made Sugiana, M. Kes", "dr. I Gusti Ayu Agung Dyah Utari", "dr. I Nyoman Gita Jaya", "dr. Nilam Rasa Surma", "dr. Pande Pt. Dodi Martana", "dr. Nil Luh Yuni Wiandari", "dr. Asri Wedhari", "dr. Ni Komang Ayu Trisya Mega Yani", "Dokter Internship"])
                st.tanggal_konsul = st.date_input("Tanggal Konsultasi*")

                # Lanjut dengan mengisi formulir khusus diabetes atau hipertensi
                if jenis_penyakit == "Diabetes":
                    st.gdp = st.text_input("GDP*")
                    st.gds = st.text_input("GDS*")
                    st.selected_obat = st.selectbox("Pilih Obat", list(obat_options.keys()))
                    
                else:
                    #st.td_sistol = st.selectbox("Tekanan Darah Sistolik (mmHg)", list(range(0, 301)), format_func=lambda x: f"{x} mmHg")
                    st.td_sistol = st.selectbox("Tekanan Darah Sistolik (mmHg)", list(range(0, 301)))
                    st.td_diastol = st.selectbox("Tekanan Darah Diastolik (mmHg)", list(range(0, 301)))
                    st.selected_obat_hipertensi = st.selectbox("Pilih Obat Hipertensi", list(obat_hipertensi_options.keys()))

                submit_button2 = st.form_submit_button("Submit Langkah 2")
                
                if submit_button2:
                    st.session_state.my_variable_state2 += 1
                    
                    if jenis_penyakit == "Diabetes":
                        if not(st.gdp and st.gds):
                            st.warning("Harap isi semua kolom yang diperlukan.")
                            st.stop()
                        try:
                            st.gdp = float(st.gdp)
                            st.gds = float(st.gds)
                        except ValueError:
                            st.warning("Masukkan hanya angka untuk GDP, GDS.")
                            st.stop()
                    else:
                        if st.td_sistol < 0 or st.td_sistol > 300:
                            st.warning("Tekanan darah sistolik harus berada dalam rentang 0 hingga 300 mmHg.")
                            st.stop()
                        if st.td_diastol < 0 or st.td_diastol > 300:
                            st.warning("Tekanan darah diastolik harus berada dalam rentang -300 hingga 0 mmHg.")
                            st.stop()

    def form3():
        if st.session_state.my_variable_state2 >= 1:
            
            with st.form("data_form3", clear_on_submit= True):      
                st.write("**Langkah 3. Masukkan dosis**")    
                if jenis_penyakit == "Diabetes":
                    st.selected_dosis = st.selectbox(f"Pilih Dosis {st.selected_obat}", obat_options[st.selected_obat])
                else:
                    st.selected_dosis_hipertensi = st.selectbox(f"Pilih Dosis {st.selected_obat_hipertensi}", obat_hipertensi_options[st.selected_obat_hipertensi])

                submit_button3 = st.form_submit_button("Submit Langkah 3")
                if submit_button3:
                    st.session_state.my_variable_state3 += 1
                    st.write(f"Dosis obat {st.selected_obat if jenis_penyakit == 'Diabetes' else st.selected_obat_hipertensi}: {st.selected_dosis if jenis_penyakit == 'Diabetes' else st.selected_dosis_hipertensi}")
                    
                # Data pasien
    verif_final = False
    def form_final():
        
        if st.session_state.my_variable_state3 >= 1:
            st.pasien_data = existing_pasien_data.loc[existing_pasien_data["NoERM"] == st.no_erm_input].iloc[0]
            
            existing_data_pasien_penyakit = conn.read(worksheet="penyakit_pasien", usecols=list(range(11)), ttl=5)
            existing_data_pasien_penyakit = existing_data_pasien_penyakit.dropna(how="all")
            if st.session_state.my_variable_state3 >= 1:
                with st.form (key = "form_final", clear_on_submit= True):
                    st.write("**Langkah 4. Submit Data Final**")
                    st.write("Pastikan semua data sudah benar sebelum melanjutkan.")
                    st.write("Anda bisa mengganti isi data dengan klik submit pada langkah sebelumnya.")
                    st.write("Data yang akan disubmit:")
                    if jenis_penyakit == "Diabetes":
                        penyakit_data = pd.DataFrame(
                            {
                                "Nama": [st.pasien_data["Nama"]],
                                "NoERM": [st.pasien_data["NoERM"]],
                                "TanggalLab": [st.tanggal_lab.strftime("%Y-%m-%d")],
                                "GDP": [st.gdp],
                                "GDS": [st.gds],
                                "Obat" : [st.selected_obat],
                                "Dosis" : [st.selected_dosis],
                                "TD": None,
                                "Dokter": [st.dokter],
                                "TanggalKonsul": [st.tanggal_konsul.strftime("%Y-%m-%d")],
                                "Jenis Penyakit": [jenis_penyakit],
                            }
                        )
                    else:
                        penyakit_data = pd.DataFrame(
                            {
                                "Nama": [st.pasien_data["Nama"]],
                                "NoERM": [st.pasien_data["NoERM"]],
                                "TanggalLab": [st.tanggal_konsul.strftime("%Y-%m-%d")],
                                "GDP": None,
                                "GDS": None,
                                "Obat" : [st.selected_obat_hipertensi],
                                "Dosis" : [st.selected_dosis_hipertensi],
                                "TD": f"{st.td_sistol}/{st.td_diastol}",
                                "Dokter": [st.dokter],
                                "TanggalKonsul": [st.tanggal_konsul.strftime("%Y-%m-%d")],
                                "Jenis Penyakit": [jenis_penyakit]
                            }
                        )
                    st.write(penyakit_data)
                    submit_button4 = st.form_submit_button("Submit Final")
                    verif_final = True
                    if submit_button4:
                        updated_penyakit_df = pd.concat([existing_data_pasien_penyakit,penyakit_data], ignore_index=True)
                        conn.update(worksheet="penyakit_pasien", data=updated_penyakit_df)
                        #st.write(updated_penyakit_df)
                        
                        st.success(f"Data {jenis_penyakit} pasien berhasil disubmit!")
                        st.write("Halaman akan otomatis direfresh dalam 3 detik.")
                        time.sleep(3)  
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
    form1()
    form2()
    form3()
    form_final()
elif selected == "Cari Rekam Medis":
    # Implementasi fitur pencarian rekam medis di sini
    # Display Title and Description
    st.title("Pendataan Pasien Diabetes dan Hipertensi")
    #st.markdown("Enter the details of the new vendor below.")
    # st.write(st.secrets['connections'])
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read( worksheet="penyakit_pasien", usecols=list(range(11)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    with st.form(key="filter_form", clear_on_submit= True):
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
