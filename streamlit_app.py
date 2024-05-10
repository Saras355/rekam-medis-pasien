import datetime
import time
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from streamlit_js_eval import streamlit_js_eval
from dateutil.relativedelta import relativedelta
import plotly.express as px



st.set_page_config(
    page_title="Rekam Medis Pasien", 
    page_icon="📊",  
)
def filter_data(data, name, no_erm):
    filtered_data = data[(data["Nama"].str.contains(name, na=False)) & (data["NoERM"].str.contains(no_erm, na=False))]
    return filtered_data


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

obat_options_2 = {
    "Tidak Ada" : ["Tidak Ada"],
    "Metformin (500-3000 mg)": ["1x1", "2x1", "3x1", "3x2"],
    "Glimepiride (1-8 mg)": ["1x1 mg", "1x2 mg", "1x3 mg", "1x4 mg", "1x5 mg", "1x6 mg", "1x7 mg", "1x8 mg"],
    "Glibenclamide (2.5-20 mg)": ["1x5 mg", "1x10 mg", "1x15 mg","1x20 mg"]
}

obat_hipertensi_options_2 = {
    "Tidak Ada" : ["Tidak Ada"],
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
#Ambil data penyakit_pasien dari Google Sheets
def tampilkan_dashboard():
    conn = st.connection("gsheets", type=GSheetsConnection)
    import datetime

    # Ambil data penyakit_pasien dari Google Sheets
    existing_data = conn.read(worksheet="penyakit_pasien", usecols=list(range(11)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    # st.write(existing_data)
    # st.write("muncul")

   #
        # Filter data berdasarkan bulan dan tahun yang diinginkan (misalnya, bulan April 2024)
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    target_month = current_month - 1 # April
    if target_month == 0:
        target_month = 12  # Ubah target_month menjadi Desember
        target_year -= 1 
    target_year = current_year

    
    existing_data["TanggalKonsul"] = pd.to_datetime(existing_data["TanggalKonsul"])

    filtered_data = existing_data[(existing_data["TanggalKonsul"].dt.month == target_month) & (existing_data["TanggalKonsul"].dt.year == target_year)]
    # st.write(filtered_data)
    #hitung total yang diabetes

    #hitung total yang hipertensi
    
    #hitung total yang diabetes
    total_diabetes = len(filtered_data[filtered_data["Jenis Penyakit"] == "Diabetes"])

    #hitung yang hipertensi
    total_hipertensi = len(filtered_data[filtered_data["Jenis Penyakit"] == "Hipertensi"])
    # Filter data untuk pasien Diabetes dengan GDP/GDS antara 80-130
    #st.write(total_hipertensi)
    diabetes_data = filtered_data[(filtered_data["Jenis Penyakit"] == "Diabetes") & ((filtered_data["GDP"] >= 80) & (filtered_data["GDP"] <= 130) | (filtered_data["GDS"] >= 80) & (filtered_data["GDS"] <= 130))]
    # st.write(diabetes_data)
    if total_diabetes:
    # Hitung persentase pasien Diabetes yang memenuhi kriteria
        diabetes_percentage = len(diabetes_data) /total_diabetes * 100
        # st.write(diabetes_percentage)
    else:
        diabetes_percentage = 0
    # Filter data untuk pasien Hipertensi dengan TD < 140
    filtered_data["TD"] = filtered_data["TD"].apply(lambda x: int(x.split("/")[0]) if isinstance(x, str) else x)
    hipertensi_data = filtered_data[(filtered_data["Jenis Penyakit"] == "Hipertensi") & ((filtered_data["TD"] < 140))]
    # st.write(hipertensi_data)
    if total_hipertensi:
        # Hitung persentase pasien Hipertensi yang memenuhi kriteria
        hipertensi_percentage = len(hipertensi_data) / total_hipertensi * 100
        
        # st.write(hipertensi_percentage)
    else:
        hipertensi_percentage = 0
    # Tampilkan hasil dalam bentuk grafik
    #   st.markdown(f"**Capaian untuk bulan {target_month} tahun {target_year} :**")
    st.write(f"**Persentase Pasien yang Memenuhi Kriteria di Bulan {target_month}/{target_year}:**")

    columns = st.columns(2)

    if total_diabetes:
        columns[0].write(f"<div style='font-size:24px; background-color: #FFCCCC; padding: 10px; border-radius: 5px;'>{diabetes_percentage:.2f}%</div>", unsafe_allow_html=True)
        columns[0].write("<div style='background-color: #FFCCCC; padding: 10px; border-radius: 5px;'>Pasien Diabetes dengan GDP/GDS 80-130</div>", unsafe_allow_html=True)
    else:
        columns[0].write(f"<div style='font-size:24px; background-color: #FFCCCC; padding: 10px; border-radius: 5px;'> -- </div>", unsafe_allow_html=True)
        columns[0].write("<div style='background-color: #FFCCCC; padding: 10px; border-radius: 5px;'>Pasien Diabetes dengan GDP/GDS 80-130</div>", unsafe_allow_html=True)

    if total_hipertensi:
        columns[1].write(f"<div style='font-size:24px; background-color: #FFCCCC; padding: 10px; border-radius: 5px;'>{hipertensi_percentage:.2f}%</div>", unsafe_allow_html=True)
        columns[1].write("<div style='background-color: #FFCCCC; padding: 10px; border-radius: 5px;'>Pasien Hipertensi dengan TDS < 140</div>", unsafe_allow_html=True)
    else:
        columns[1].write(f"<div style='font-size:24px; background-color: #FFCCCC; padding: 10px; border-radius: 5px;'> --- </div>", unsafe_allow_html=True)
        columns[1].write("<div style='background-color: #FFCCCC; padding: 10px; border-radius: 5px;'>Pasien Hipertensi dengan TDS < 140</div>", unsafe_allow_html=True)
st.write()

if selected == "Input Data Pasien":
    tampilkan_dashboard()
    st.write()
    st.write()
    st.title("Pendataan Pasien Diabetes dan Hipertensi")
    
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Fetch existing pasien data
    existing_pasien_data = conn.read(worksheet="data_pasien", usecols=list(range(6)), ttl=5)
    existing_pasien_data = existing_pasien_data.dropna(how="all")
   
    with st.form(key="pasien_form", clear_on_submit=True):
        st.write("Formulir Data Pasien:")
        nama = st.text_input("Nama*")
        nama = nama.lower()
        no_erm = st.text_input("No eRM*", help="Harap isi dengan nomor pasien yang unik.").strip()
        tempat_lahir = st.text_input("Tempat Lahir*")
        tanggal_lahir = st.text_input("Tanggal Lahir* (DD-MM-YYYY)")
        jenis_kelamin = st.selectbox("Jenis Kelamin*", ["Laki-laki", "Perempuan"])
        no_telepon = st.text_input("No Telepon*", placeholder="(08xxxxxxxxxx)")
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            # Validasi
            if not (nama and no_erm and tempat_lahir and tanggal_lahir and jenis_kelamin and no_telepon):
                st.warning("Harap isi semua kolom yang diperlukan.")
                st.stop()
                
            # Validasi tanggal lahir sesuai format
            try:
                tanggal_lahir = datetime.datetime.strptime(tanggal_lahir, "%d-%m-%Y")
            except ValueError:
                st.warning("Tanggal lahir harus dalam format DD-MM-YYYY.")
                st.write(tanggal_lahir)
                # st.stop()
            
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
            # no_telepon = st.text_input("Nomor Telepon")

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
            no_erm = no_erm + "x"
            # st.write(no_erm)
            # st.write(existing_pasien_data["NoERM"].values)
            if no_erm in existing_pasien_data["NoERM"].values:
                st.warning("Nomor pasien sudah ada dalam basis data. Harap masukkan nomor pasien yang unik.")
                st.stop()
            
            # Buat dataframe untuk data pasien baru
            pasien_data = pd.DataFrame(
                {
                    "Nama": [nama],
                    "NoERM": [no_erm ],
                    "TempatLahir": [tempat_lahir],  
                    "TanggalLahir": [tanggal_lahir.strftime("%Y-%m-%d")],
                    "JenisKelamin": [jenis_kelamin],
                    "NoTelepon": [no_telepon]
                }
            )
            
            # Update Google Sheets dengan data pasien baru
            # updated_pasien_df = pd.concat([existing_pasien_data, pasien_data], ignore_index=True)
            updated_pasien_df = existing_pasien_data.append(pasien_data, ignore_index=True)

            conn.update(worksheet="data_pasien", data=updated_pasien_df)
            st.success("Data pasien berhasil disubmit!")
            nama = no_erm = tempat_lahir = tanggal_lahir = jenis_kelamin = no_telepon =  None

            #streamlit_js_eval(js_expressions="parent.window.location.reload()")

elif selected in ["Input Data Diabetes", "Input Data Hipertensi"]:
    tampilkan_dashboard()
    st.write()

   
    st.write()
    st.write()
    st.title("Input Data Diabetes dan Hipertensi")

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
        with st.form(key ="data_form", clear_on_submit= False):
            verif_data = None
        
            
            st.write(f"Formulir {jenis_penyakit}:")
            st.write("**Langkah 1. Masukkan No eRM Pasien**")
            st.no_erm_input = st.text_input("No eRM*", help="Masukkan NoERM pasien.").strip()            
            nama_pasien = None
            submit_button = st.form_submit_button("Submit Langkah 1")
            if submit_button:
                st.session_state.my_variable_state += 1
                if st.no_erm_input:
                    # nama_pasien = existing_pasien_data.loc[existing_pasien_data["NoERM"] == st.no_erm_input, "Nama"].values
                    nama_pasien = existing_pasien_data.loc[existing_pasien_data["NoERM"].str.rstrip("x") == st.no_erm_input, "Nama"].values

                if nama_pasien[0]:
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
            with st.form(key="data_form2", clear_on_submit= False):
                st.write("**Langkah 2. Masukkan data dokter dan tanggal konsultasi dan lab**")
                st.tanggal_lab = st.date_input("Tanggal Lab*")
                st.dokter = st.selectbox("Dokter*", ["dr. I Made Sugiana, M. Kes", "dr. I Gusti Ayu Agung Dyah Utari", "dr. I Nyoman Gita Jaya", "dr. Nilam Rasa Surma", "dr. Pande Pt. Dodi Martana", "dr. Nil Luh Yuni Wiandari", "dr. Asri Wedhari", "dr. Ni Komang Ayu Trisya Mega Yani", "Dokter Internship"])
                #st.tanggal_konsul = st.date_input("Tanggal Konsultasi*")

                # Lanjut dengan mengisi formulir khusus diabetes atau hipertensi
                if jenis_penyakit == "Diabetes":
                    st.gdp = st.text_input("GDP") #krn ada kemungkinan dia ga puasa 
                    st.gds = st.text_input("GDS")
                    st.selected_obat = st.selectbox("Pilih Obat", list(obat_options.keys()))
                    st.selected_obat_2 = st.selectbox("Pilih Obat", list(obat_options_2.keys()))
                  
                    
                else:
                    #st.td_sistol = st.selectbox("Tekanan Darah Sistolik (mmHg)", list(range(0, 301)), format_func=lambda x: f"{x} mmHg")
                    st.td_sistol = st.selectbox("Tekanan Darah Sistolik (mmHg)", list(range(0, 301)))
                    st.td_diastol = st.selectbox("Tekanan Darah Diastolik (mmHg)", list(range(0, 301)))
                    st.selected_obat_hipertensi = st.selectbox("Pilih Obat Hipertensi", list(obat_hipertensi_options.keys()))
                    st.selected_obat_hipertensi_2 = st.selectbox("Pilih Obat Hipertensi", list(obat_hipertensi_options_2.keys()))


                submit_button2 = st.form_submit_button("Submit Langkah 2")
                
                if submit_button2:
                    st.session_state.my_variable_state2 += 1
                    
                    if jenis_penyakit == "Diabetes":
                        # if not(st.gdp and st.gds):
                        #     st.warning("Harap isi semua kolom yang diperlukan.")
                        #     st.stop()
                        if not st.gdp:
                            st.gdp = 0.0
                        if not st.gds:
                            st.gds = 0.0
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
            
            with st.form("data_form3", clear_on_submit= False):      
                st.write("**Langkah 3. Masukkan dosis**")    
                if jenis_penyakit == "Diabetes":
                    st.selected_dosis = st.selectbox(f"Pilih Dosis {st.selected_obat}", obat_options[st.selected_obat])
                    st.selected_dosis_2 = st.selectbox(f"Pilih Dosis {st.selected_obat_2}", obat_options_2[st.selected_obat_2])
                else:
                    st.selected_dosis_hipertensi = st.selectbox(f"Pilih Dosis {st.selected_obat_hipertensi}", obat_hipertensi_options[st.selected_obat_hipertensi])
                    st.selected_dosis_hipertensi_2 = st.selectbox(f"Pilih Dosis {st.selected_obat_hipertensi_2}", obat_hipertensi_options_2[st.selected_obat_hipertensi_2])
                submit_button3 = st.form_submit_button("Submit Langkah 3")
                if submit_button3:
                    st.session_state.my_variable_state3 += 1
                    st.write(f"Dosis obat 1:  {st.selected_obat if jenis_penyakit == 'Diabetes' else st.selected_obat_hipertensi}: {st.selected_dosis if jenis_penyakit == 'Diabetes' else st.selected_dosis_hipertensi}")
                    st.write(f"Dosis obat 2:  {st.selected_obat_2 if jenis_penyakit == 'Diabetes' else st.selected_obat_hipertensi_2}: {st.selected_dosis_2 if jenis_penyakit == 'Diabetes' else st.selected_dosis_hipertensi_2}")

                # Data pasien
    verif_final = False
    def form_final():
        
        if st.session_state.my_variable_state3 >= 1:
            print("la: " + st.no_erm_input)
            print("du:" + existing_pasien_data["NoERM"])
            #st.pasien_data = existing_pasien_data.loc[existing_pasien_data["NoERM"] == st.no_erm_input+"x"].iloc[0]
            st.pasien_data = existing_pasien_data.loc[existing_pasien_data["NoERM"] == st.no_erm_input+"x"]
            existing_data_pasien_penyakit = conn.read(worksheet="penyakit_pasien", usecols=list(range(10)), ttl=5)
            existing_data_pasien_penyakit = existing_data_pasien_penyakit.dropna(how="all")
            # st.write(st.pasien_data)
            # st.write(existing_data_pasien_penyakit)
            # st.write(st.pasien_data["Nama"].values)
            if st.session_state.my_variable_state3 >= 1:
                with st.form (key = "form_final", clear_on_submit= False):
                    st.write("**Langkah 4. Submit Data Final**")
                    st.write("Pastikan semua data sudah benar sebelum melanjutkan.")
                    st.write("Anda bisa mengganti isi data dengan klik submit pada langkah sebelumnya.")
                    st.write("Data yang akan disubmit:")
                    if jenis_penyakit == "Diabetes":
                        penyakit_data = pd.DataFrame(
                            {
                                "Nama": [st.pasien_data["Nama"].values[0]],
                                "NoERM": [st.pasien_data["NoERM"].values[0]],
                                "TanggalKonsul": [st.tanggal_lab.strftime("%Y-%m-%d")],
                                "GDP": [st.gdp],
                                "GDS": [st.gds],
                                "Obat" : [st.selected_obat],
                                "Dosis" : [st.selected_dosis],
                                "Obat2" : [st.selected_obat_2],
                                "Dosis2" : [st.selected_dosis_2],
                                "TD": None,
                                "Dokter": [st.dokter],
                               # "TanggalKonsul": [st.tanggal_konsul.strftime("%Y-%m-%d")],
                                "Jenis Penyakit": [jenis_penyakit],
                            }
                        )
                    else:
                        penyakit_data = pd.DataFrame(
                            {
                                "Nama": [st.pasien_data["Nama"].values[0]],
                                "NoERM": [st.pasien_data["NoERM"].values[0]],
                                "TanggalKonsul": [st.tanggal_lab.strftime("%Y-%m-%d")],
                                "GDP": None,
                                "GDS": None,
                                "Obat" : [st.selected_obat_hipertensi],
                                "Dosis" : [st.selected_dosis_hipertensi],
                                "Obat2" : [st.selected_obat_hipertensi_2],
                                "Dosis2" : [st.selected_dosis_hipertensi_2],
                                "TD": f"{st.td_sistol}/{st.td_diastol}",
                                "Dokter": [st.dokter],
                              #  "TanggalKonsul": [st.tanggal_konsul.strftime("%Y-%m-%d")],
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

# elif selected == "Dashboard Pasien":
#    st.write("haloo")
    
            # if total_diabetes:
            #     st.write(f"<span style='font-size:24px'>{diabetes_percentage:.2f}%</span>", unsafe_allow_html=True)
            #     st.write(f"Pasien Diabetes")
            # else:
            #     st.write("-")

            # if total_hipertensi:
            #     st.write(f"<span style='font-size:24px'>{hipertensi_percentage:.2f}%</span>", unsafe_allow_html=True)
            #     st.write(f"Pasien Hipertensi")
            # else:
            #     st.write("-")
            # if total_diabetes:
            #     st.markdown(f"- Besar persentase pasien Diabetes yang memenuhi kriteria: {diabetes_percentage}% dari {total_diabetes} total pasien Diabetes.")
            # else:
            #     st.markdown("- Tidak ada data tersedia untuk pasien Diabetes.")
                    
            # if total_hipertensi:
            #     st.markdown(f"- Besar persentase pasien Hipertensi yang memenuhi kriteria sebanyak {hipertensi_percentage}% dari {total_hipertensi} total pasien Hipertensi.")
            # else: 
            #     st.markdown("- Tidak ada data tersedia untuk pasien Hipertensi.")

            # plt.figure(figsize=(4, 4))
            # plt.bar(["Diabetes", "Hipertensi"], [diabetes_percentage, hipertensi_percentage], color=['blue', 'green'])
            # plt.xlabel("Jenis Penyakit")
            # plt.ylabel("Persentase Pasien (%)")
            # plt.title(f"Persentase Pasien yang Memenuhi Kriteria di Bulan {target_month}/{target_year}")
            # plt.ylim(0, 100)
            # plt.show()
            # st.pyplot(plt)
           
            

    #     else:
    #         st.warning(f"Tidak ada data tersedia untuk bulan {target_month}, {target_year}.")
    # else:
    #     st.warning("Tidak ada data tersedia untuk ditampilkan.")


elif selected == "Cari Rekam Medis":
    # st.write("Formulir Pencarian Rekam Medis:")
    # filter_name = st.text_input("Masukkan nama pasien yang dicari:")
    # filter_no_erm = st.text_input("Masukkan NoERM pasien yang dicari:") + "x"
    # filter_button = st.button("Cari")
    # conn = st.connection("gsheets", type=GSheetsConnection)
    # existing_data = conn.read( worksheet="penyakit_pasien", usecols=list(range(11)), ttl=5)
    # existing_data = existing_data.dropna(how="all")
    # if filter_button:
    #     filtered_data = filter_data(existing_data, filter_name, filter_no_erm)
    #     if not filtered_data.empty:
    #         st.subheader(f"Detail Pasien {filter_name}")
    #         st.write(filtered_data)

    #         # Split data based on disease
    #         diabetes_data = filtered_data[filtered_data["Jenis Penyakit"] == "Diabetes"]
    #         hipertensi_data = filtered_data[filtered_data["Jenis Penyakit"] == "Hipertensi"]

    #         # Plotting diabetes data
    #         if not diabetes_data.empty:
    #             st.subheader("Grafik Data Diabetes")
    #             fig_diabetes = px.scatter(diabetes_data, x="Tanggal Konsul", y="GDP", color_discrete_sequence=["blue"], 
    #                                       hover_data={"Tanggal Konsul": False, "GDP": True},
    #                                       labels={"GDP": "GDP (Diabetes)"})
    #             fig_diabetes.update_traces(mode="markers+text", marker=dict(size=10))
    #             st.plotly_chart(fig_diabetes)

    #             fig_gds = px.scatter(diabetes_data, x="Tanggal Konsul", y="GDS", color_discrete_sequence=["green"], 
    #                                  hover_data={"Tanggal Konsul": False, "GDS": True},
    #                                  labels={"GDS": "GDS (Diabetes)"})
    #             fig_gds.update_traces(mode="markers+text", marker=dict(size=10))
    #             st.plotly_chart(fig_gds)

    #         # Plotting hipertensi data
    #         if not hipertensi_data.empty:
    #             st.subheader("Grafik Data Hipertensi")
    #             fig_hipertensi = px.scatter(hipertensi_data, x="Tanggal Konsul", y="TD", color_discrete_sequence=["red"], 
    #                                         hover_data={"Tanggal Konsul": False, "TD": True},
    #                                         labels={"TD": "TD (Hipertensi)"})
    #             fig_hipertensi.update_traces(mode="markers+text", marker=dict(size=10))
    #             st.plotly_chart(fig_hipertensi)
    #     else:
    #         st.info("Data tidak tersedia untuk filter yang diberikan.")


    def create_hover_text(row):
        hover_text = f"Obat 1: {row['Obat']}<br>Dosis 1: {row['Dosis']}<br>"
        if not pd.isnull(row['Obat2']) and not pd.isnull(row['Dosis2']):
            hover_text += f"Obat 2: {row['Obat2']}<br>Dosis 2: {row['Dosis2']}"
        return hover_text
    

    def create_hover_text_diabetes(row):
        hover_text_diabetes = f"Obat 1: {row['Obat']}<br>Dosis 1: {row['Dosis']}<br>"
        if not pd.isnull(row['Obat2']) and not pd.isnull(row['Dosis2']):
            hover_text_diabetes += f"Obat 2: {row['Obat2']}<br>Dosis 2: {row['Dosis2']}"
        if not pd.isnull(row['GDS']):
            hover_text_diabetes += f"GDS: {row['GDS']}"
        return hover_text_diabetes
    tampilkan_dashboard()
    st.write()
    # Implementasi fitur pencarian rekam medis di sini
    # Display Title and Description
    st.title("Pencarian Pasien Diabetes dan Hipertensi")
    #st.markdown("Enter the details of the new vendor below.")
    # st.write(st.secrets['connections'])
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read( worksheet="penyakit_pasien", usecols=list(range(12)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    with st.form(key="filter_form", clear_on_submit= True):
        filter_name = st.text_input(label="Masukkan nama pasien yang dicari")
        filter_name = filter_name.lower()
        filter_no_erm = st.text_input(label="Masukkan NoERM pasien yang dicari").strip() + "x"






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
        filtered_data = filtered_data.sort_values(by="TanggalKonsul", ascending=False).head(4)
    #filtered_data = existing_data[(existing_data["Nama"].str.contains(filter_name))]
        #filtered_data = existing_data[(existing_data["NoERM"].astype(str).str.contains(filter_no_erm))]
        # Display existing vendors data filtered by company_name
        st.subheader(f"Detail Pasien {filter_name}")
        #filtered_data = str(filtered_data["GDP"])
        st.write(filtered_data)

        # Split data based on disease
        diabetes_data = filtered_data[filtered_data["Jenis Penyakit"] == "Diabetes"]
        hipertensi_data = filtered_data[filtered_data["Jenis Penyakit"] == "Hipertensi"]

        #filtered hanya ambil yang tanggalnya terbaru -> 4 bulan terakhir

        # diabetes_data = diabetes_data.head(4)
        # hipertensi_data = hipertensi_data.head(4)

        # #kode buat ambil bulan ini
        # # Filter data berdasarkan bulan dan tahun yang diinginkan (misalnya, bulan April 2024)
        # current_month = datetime.datetime.now().month
        # current_year = datetime.datetime.now().year

        # #target motnhnya dalam rentang waktu 4 bulan terakhir
        # diabetes_data['TanggalKonsul'] = pd.to_datetime(diabetes_data['TanggalKonsul'])
        # hipertensi_data['TanggalKonsul'] = pd.to_datetime(hipertensi_data['TanggalKonsul'])
        # # target_month = current_month - 1 
        # four_months_ago = datetime.datetime.now() - relativedelta(months=3, days=datetime.datetime.now().day-1)




        # target_year = current_year
        # # if target_month == 0:
        # #     target_month = 12  
        # #     target_year -= 1 
        # # #filtered baik utnuk data diabetes dan hipertensi based dari target_month dan target_year
        # diabetes_data = diabetes_data[(diabetes_data["TanggalKonsul"] >= four_months_ago) & (diabetes_data["TanggalKonsul"].dt.year == datetime.datetime.now().year)]
        # hipertensi_data = hipertensi_data[(hipertensi_data["TanggalKonsul"] >= four_months_ago) & (hipertensi_data["TanggalKonsul"].dt.year == datetime.datetime.now().year)]


        #buat tooltip
    
        #diabetes_data['hover_text'] = diabetes_data.apply(create_hover_text, axis=1)

        #buat graph dulu untuk dibates 
        # Plotting data diabetes
        # if not diabetes_data.empty:
        #     #st.write(diabetes_data)
        #     st.subheader("Grafik Data Diabetes")
        #     fig_diabetes = px.scatter(diabetes_data, x="TanggalKonsul", y="GDP", color="NoERM", hover_name=f"GDP/GDS : {"GDP"}/ {"GDS"}",
        #                             labels={"GDP": "GDP (Diabetes)"}, title="Grafik Data Diabetes",
        #                             template="plotly_white", hover_data={"hover_text": True})   
        #     fig_diabetes.update_traces(mode="markers+lines", marker=dict(size=10))
        #     fig_diabetes.update_layout(showlegend=True)
        #     st.plotly_chart(fig_diabetes)

        #buat graph dulu untuk dibates 
        # Plotting data diabetes
        # st.write(diabetes_data)
        # st.write(hipertensi_data)
        if not diabetes_data.empty:
      
            diabetes_data['hover_text_diabetes'] = diabetes_data.apply(create_hover_text_diabetes, axis=1)

            st.subheader("Grafik Data Diabetes")
            fig_diabetes = px.scatter(diabetes_data, x="TanggalKonsul", y="GDP", color="NoERM", hover_name="GDP",
                                        labels={"GDP": "GDP (Diabetes)"}, title="Grafik Data Diabetes",
                                        template="plotly_white", hover_data={"hover_text_diabetes": True})   
            fig_diabetes.update_traces(mode="markers+lines", marker=dict(size=10))
            fig_diabetes.update_layout(showlegend=True)
            st.plotly_chart(fig_diabetes)




        if not hipertensi_data.empty:
            hipertensi_data['hover_text'] = hipertensi_data.apply(create_hover_text, axis=1)
            hipertensi_data[['TDS', 'TDD']] = hipertensi_data['TD'].str.split('/', expand=True)

            # Mengonversi nilai menjadi numerik untuk pengurutan yang benar
            hipertensi_data['TDS'] = pd.to_numeric(hipertensi_data['TDS'])
            hipertensi_data['TDD'] = pd.to_numeric(hipertensi_data['TDD'])
            st.subheader("Grafik Data Hipertensi")
            fig_hipertensi = px.scatter(hipertensi_data, x="TanggalKonsul", y="TDS", color="NoERM",
                                        labels={"TDS": "TDS", "TDD": "TDD"}, 
                                        title="Grafik Data Hipertensi", template="plotly_white",
                                        hover_name="TD", hover_data={"hover_text": True})
            fig_hipertensi.update_traces(mode="markers+lines", marker=dict(size=10))
            fig_hipertensi.update_layout(showlegend=True, hoverlabel=dict(font=dict(size=16)))
            st.plotly_chart(fig_hipertensi)
        # Membuat plot dengan informasi sebelum dan setelah "/" pada sumbu y dan legenda yang sesuai
        # if not hipertensi_data.empty:
        #     st.subheader("Grafik Data Hipertensi")
        #     fig_hipertensi = px.scatter(hipertensi_data, x="TanggalKonsul", y="TDS", color="NoERM",
        #                                 labels={"TDS": "TDS", "TDD": "TDD"}, 
        #                                 title="Grafik Data Hipertensi", template="plotly_white",
        #                                 hover_name="TD")
        #     fig_hipertensi.update_traces(mode="markers+lines", marker=dict(size=10))
        #     fig_hipertensi.update_layout(showlegend=True)
        #     st.plotly_chart(fig_hipertensi)
        # # Plotting data hipertensi
        # if not hipertensi_data.empty:
        #     st.subheader("Grafik Data Hipertensi")
        #     fig_hipertensi = px.scatter(hipertensi_data, x="TanggalKonsul", y="TD", color="NoERM", hover_name="NoERM",
        #                                 labels={"TD": "TD (Hipertensi)"}, title="Grafik Data Hipertensi",
        #                                 template="plotly_white")
        #     fig_hipertensi.update_traces(mode="markers+lines", marker=dict(size=10))
        #     fig_hipertensi.update_layout(showlegend=True)
        #     st.plotly_chart(fig_hipertensi)







        #BATASSSSSSSSSSSSSSSSSSSS

        # if filtered_data['Jenis Penyakit'].iloc[0].values == "Diabetes":
        #     #filter data -> jadi filtered data untuk diabetes
            
        #     # Line chart based on filtered data
        #     if not filtered_data.empty:
        #        # st.subheader("Years in Business Over Time (Filtered)")
        #         plt.figure(figsize=(10, 6))

        #         # Plot GDP
        #         plt.plot(filtered_data["TanggalKonsul"], filtered_data["GDP"], marker='o', color='blue', label='GDP')
                
        #         # Plot GDS
        #         plt.plot(filtered_data["TanggalKonsul"], filtered_data["GDS"], marker='o', color='green', label='GDS')

        #         plt.xlabel("Tanggal Konsul")
        #         plt.ylabel("Nilai")
        #         #plt.title("Years in Business Over Time (Filtered)")
        #         plt.xticks(rotation=45)
        #         plt.legend()  # Menampilkan legenda

        #         st.set_option('deprecation.showPyplotGlobalUse', False)
        #         st.pyplot()
        #     else:
        #         st.info("No data available for the provided filter.")
        # #else: 
        # #buat graph untuk hipertensi
        # if filtered_data['Jenis Penyakit'].iloc[0].values == "Hipertensi":
        #        # Line chart based on filtered data
        #     if not filtered_data.empty:
        #       #  st.subheader("Years in Business Over Time (Filtered)")
        #         plt.figure(figsize=(10, 6))

        #         # Plot GDP
        #         plt.plot(filtered_data["TanggalKonsul"], filtered_data["GDP"], marker='o', color='blue', label='GDP')
                
        #         # Plot GDS
        #         plt.plot(filtered_data["TanggalKonsul"], filtered_data["TD"], marker='o', color='green', label='GDS')

        #         plt.xlabel("Tanggal Konsul")
        #         plt.ylabel("Nilai")
        #         #plt.title("Years in Business Over Time (Filtered)")
        #         plt.xticks(rotation=45)
        #         plt.legend()  # Menampilkan legenda

        #         st.set_option('deprecation.showPyplotGlobalUse', False)
        #         st.pyplot()
        #     else:
        #         st.info("No data available for the provided filter.")
      #  st.form(key="filter_form").clear()
