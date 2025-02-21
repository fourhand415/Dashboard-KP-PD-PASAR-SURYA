import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Halaman Navigasi
menu = st.sidebar.radio("Navigasi", ["Home", "Profil Perusahaan", "Profil Tim", "Dashboard"])

if menu == "Home":
    st.title("Selamat Datang di Dashboard Harga Bahan Pokok")
    st.image("logo.png")
    st.write("### PD Pasar Surya - Analisis Harga Bahan Pokok")
    st.write("Dashboard ini menyajikan informasi harga bahan pokok dari berbagai pasar di Surabaya.")
elif menu == "Profil Perusahaan":
    st.title("Profil Perusahaan")
    st.image("logo_perusahaan.png", caption="Logo Perusahaan")
    st.write("### PD Pasar Surya")
    st.write("PD Pasar Surya adalah perusahaan yang bergerak di bidang pengelolaan pasar tradisional di Surabaya. Pengelolaan pasar dimulai sejak jaman pemerintahan kolonial Belanda tahun 1872. Semenjak kemerdekaan Indonesia, pengelolaan pasar di nasionalisasi menjadi Dinas Pasar dibawah Pemerintah Kota Surabaya. Untuk mendorong profesionalisme, tahun 1982 Dinas Pasar berubah menjadi Perusahaan Daerah Pasar. Perubahan nama terakhir tahun 1999 menjadi Perusahaan Daerah Pasar Surya.")
    st.write("#### Visi:")
    st.write("Menjadikan PD Pasar Surya sebagai penyedia fasilitas perdagangan yang mandiri, maju, profesional, serta sebagai sarana pemberdayaan masyarakat Kota Surabaya, serta merupakan alternatif sumber pendapatan yang andal bagi Pemerintah Kota Surabaya")
    st.write("#### Misi:")
    st.write("1. Optimasi kinerja PD Pasar Surya dengan meningkatkan pelayanan terhadap masyarakat pengguna pasar secara profesional")
    st.write("2. Memberdayakan pedagang pasar dengan melibatkan secara aktif di dalam pelaksanaan program-program PD Pasar Surya")
    st.write("3. Meningkatkan keamanan, ketertiban pasar dan lingkungan pasar sehingga tercipta kondisi pasar yang tertib, aman, bersih, dan lengkap")
    st.write("4. Meningkatkan peran serta masyarakat dalam mempercepat perkembangan pasar")
    st.write("5. Mengembangkan profesional organisasi PD Pasar Surya")

elif menu == "Profil Tim":
    st.title("Profil Tim")
    st.write("### Anggota Tim")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Nama: Muhammad Farhan Lucky Putra")
        st.write("#### NRP: 5003221001")
        st.image("anggota_1.JPG", caption="Foto Mahasiswa 1")
    
    with col2:
        st.write("#### Nama: Gilang Hanif Hendrawan")
        st.write("#### NRP: 500221060")
        st.image("anggota_2.JPG", caption="Foto Mahasiswa 2")

elif menu == "Dashboard":
    st.title("Dashboard Harga Bahan Pokok")
    
    # Load data
    file_path = "Data_Gabungan.xlsx"
    df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
    
    # Pastikan kolom "Pasar" ada
    df["Pasar"] = df["Pasar"].astype(str)
    
    # Sidebar: Pilih Pasar
    pasar_list = df["Pasar"].dropna().unique()
    pasar_terpilih = st.sidebar.selectbox("Pilih Pasar", pasar_list)
    
    # Filter data berdasarkan pasar yang dipilih
    df_filtered = df[df["Pasar"] == pasar_terpilih]
    
    # Tampilkan tabel data
    st.write(f"### Data Harga Bahan Pokok - {pasar_terpilih}")
    st.dataframe(df_filtered)
    
    # Pilih bahan pokok untuk visualisasi
    if not df_filtered.empty:
        bahan_list = df_filtered.iloc[:, 1].dropna().unique()
        if len(bahan_list) > 0:
            bahan_terpilih = st.selectbox("Pilih Bahan Pokok", bahan_list)
            
            # Filter harga berdasarkan bahan pokok
            data_bahan = df_filtered[df_filtered.iloc[:, 1] == bahan_terpilih]
            
            # Konversi data ke format long untuk visualisasi
            data_long = data_bahan.melt(id_vars=["Pasar"], var_name="Tanggal", value_name="Harga")
            
            # Konversi kolom Tanggal ke datetime
            data_long["Tanggal"] = pd.to_datetime(data_long["Tanggal"], errors="coerce")
            
            # Pastikan kolom harga numerik
            data_long["Harga"] = pd.to_numeric(data_long["Harga"], errors="coerce")
            
            # Hitung fluktuasi harga dari hari sebelumnya
            data_long = data_long.sort_values(by="Tanggal")
            data_long["Fluktuasi"] = data_long["Harga"].diff()
            
            # Plot grafik harga dengan tema lebih menarik
            fig = px.line(data_long, x="Tanggal", y="Harga", title=f"Tren Harga {bahan_terpilih} di {pasar_terpilih}",
                          markers=True, template="plotly_dark")
            st.plotly_chart(fig)
            
            # Plot fluktuasi harga dengan grafik batang
            fig_fluktuasi = px.bar(data_long, x="Tanggal", y="Fluktuasi", title="Fluktuasi Harga Harian",
                                   color="Fluktuasi", color_continuous_scale=["red", "green"], template="plotly_dark")
            st.plotly_chart(fig_fluktuasi)
            
            # Statistik deskriptif dengan tampilan menarik
            if not data_long["Harga"].dropna().empty:
                mean_price = data_long['Harga'].mean()
                median_price = data_long['Harga'].median()
                min_price = data_long['Harga'].min()
                max_price = data_long['Harga'].max()
                std_dev = data_long['Harga'].std()
                
                st.write("### Statistik Deskriptif")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Rata-rata Harga", value=f"{mean_price:,.2f}")
                    st.metric(label="Harga Minimum", value=f"{min_price:,.2f}")
                with col2:
                    st.metric(label="Median Harga", value=f"{median_price:,.2f}")
                    st.metric(label="Harga Maksimum", value=f"{max_price:,.2f}")
                with col3:
                    st.metric(label="Standar Deviasi", value=f"{std_dev:,.2f}")
                
                # Boxplot distribusi harga
                fig_box = go.Figure()
                fig_box.add_trace(go.Box(y=data_long["Harga"], name=bahan_terpilih, boxmean=True, marker_color="royalblue"))
                fig_box.update_layout(title="Distribusi Harga", template="plotly_dark")
                st.plotly_chart(fig_box)
        else:
            st.write("Tidak ada data bahan pokok yang tersedia.")
    else:
        st.write("Data tidak tersedia untuk pasar yang dipilih.")
    
    st.write("Dashboard ini dibuat dengan Streamlit - Versi Ditingkatkan!")


