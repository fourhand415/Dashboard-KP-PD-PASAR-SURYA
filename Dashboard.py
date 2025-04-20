import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Halaman Navigasi
menu = st.sidebar.radio("Navigasi", ["Home", "Profil Perusahaan", "Profil Tim", "Data Pasar"])

if menu == "Home":
    st.markdown("<h1 style='text-align: center;'>Dashboard Harga Bahan Pokok</h1>", unsafe_allow_html=True)
    st.columns([1,2,1])[1].image("logo_perusahaan.png")
    st.markdown("<h3 style='text-align: center;'>PD Pasar Surya - Analisis Harga Bahan Pokok</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Dashboard ini menyajikan informasi harga bahan pokok dari berbagai pasar di Surabaya.</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='background-color: #f0f8ff; padding: 10px; border-radius: 10px;'>"
            "<h5 style='text-align: center;'>Supported by</h5>"
            "</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("advancing_humanity.png", use_container_width="auto")
        st.markdown("<p style='text-align: center;'>Institut Teknologi Sepuluh Nopember</p>", unsafe_allow_html=True)
    with col2:
        st.image("logo_stat.png", use_container_width="auto")
        st.markdown("<p style='text-align: center;'>Departemen Statistika ITS</p>", unsafe_allow_html=True)
    with col3:
        st.image("pojok_statistik.png", use_container_width="auto")
        st.markdown("<p style='text-align: center;'>Pojok Statistika</p>", unsafe_allow_html=True)
elif menu == "Profil Perusahaan":
    st.title("Profil Perusahaan")
    st.columns([1,2,1])[1].image("logo_perusahaan.png", caption= "Logo Perusahaan")
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
    st.markdown("<h2 style='text-align: center;'>Profil Tim</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Anggota Tim</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("farhan.JPG", caption="Muhammad Farhan Lucky Putra", use_container_width="True")
        st.markdown("<p style='text-align: center;'><strong>NRP:</strong> 5003221001</p>", unsafe_allow_html=True)
    with col2:
        st.image("gilang.JPG", caption="Gilang Hanif Hendrawan", use_container_width="True")
        st.markdown("<p style='text-align: center;'><strong>NRP:</strong> 500221060</p>", unsafe_allow_html=True)

elif menu == "Data Pasar":
    file_path = "Data_Gabungan.xlsx"
    df = pd.read_excel(file_path, dtype=str, engine="openpyxl")

    df["Pasar"] = df["Pasar"].astype(str)
    pasar_list = ["Semua Pasar"] + list(df["Pasar"].dropna().unique())
    pasar_terpilih = st.sidebar.selectbox("Pilih Pasar", pasar_list)

    if pasar_terpilih == "Semua Pasar":
        st.write(f"### Data Harga Bahan Pokok - Semua Pasar")
        df_filtered = df.copy()
        bahan_list = df_filtered["NAMA BAHAN POKOK DAN PENTING LAINNYA"].dropna().unique()
        bahan_terpilih = st.selectbox("Pilih Bahan Pokok", bahan_list)

        data_bahan = df_filtered[df_filtered["NAMA BAHAN POKOK DAN PENTING LAINNYA"] == bahan_terpilih]
        data_long = data_bahan.melt(id_vars=["Pasar"], var_name="Tanggal", value_name="Harga")
        data_long["Tanggal"] = pd.to_datetime(data_long["Tanggal"], errors="coerce")
        data_long["Harga"] = pd.to_numeric(data_long["Harga"], errors="coerce")
        data_long = data_long.dropna(subset=["Harga"])

        st.write(f"### Rata-rata Harga {bahan_terpilih} di Setiap Pasar")
        avg_per_pasar = data_long.groupby("Pasar")["Harga"].mean().round(2).reset_index()
        col1, col2, col3, col4 = st.columns(4)
        for i, row in avg_per_pasar.iterrows():
            if i % 4 == 0:
                with col1:
                    st.metric(label=row["Pasar"], value=f"{row['Harga']:,.2f}")
            elif i % 4 == 1:
                with col2:
                    st.metric(label=row["Pasar"], value=f"{row['Harga']:,.2f}")
            elif i % 4 == 2:
                with col3:
                    st.metric(label=row["Pasar"], value=f"{row['Harga']:,.2f}")
            else:
                with col4:
                    st.metric(label=row["Pasar"], value=f"{row['Harga']:,.2f}")
        pasar_terendah = avg_per_pasar.loc[avg_per_pasar['Harga'].idxmin()]
        st.info(f"Pasar dengan harga {bahan_terpilih} termurah: {pasar_terendah['Pasar']} ({pasar_terendah['Harga']:,.2f})")
        st.write("### Statistik Deskriptif")
        mean_price = data_long['Harga'].mean()
        median_price = data_long['Harga'].median()
        min_price = data_long['Harga'].min()
        max_price = data_long['Harga'].max()
        std_dev = data_long['Harga'].std()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Rata-rata Harga", value=f"{mean_price:,.2f}")
            st.metric(label="Harga Minimum", value=f"{min_price:,.2f}")
        with col2:
            st.metric(label="Median Harga", value=f"{median_price:,.2f}")
            st.metric(label="Harga Maksimum", value=f"{max_price:,.2f}")
        with col3:
            st.metric(label="Standar Deviasi", value=f"{std_dev:,.2f}")

        fig_box = go.Figure()
        fig_box.add_trace(go.Box(y=data_long["Harga"], name=bahan_terpilih, boxmean=True, marker_color="royalblue"))
        fig_box.update_layout(title="Distribusi Harga di Semua Pasar", template="plotly_dark")
        st.plotly_chart(fig_box)
    else:
        df_filtered = df[df["Pasar"] == pasar_terpilih]
        bahan_list = df_filtered["NAMA BAHAN POKOK DAN PENTING LAINNYA"].dropna().unique()

        if len(bahan_list) > 0:
            st.write(f"### Data Harga Bahan Pokok - {pasar_terpilih}")
            st.dataframe(df_filtered)
            bahan_terpilih = st.selectbox("Pilih Bahan Pokok", bahan_list)

            data_bahan = df_filtered[df_filtered["NAMA BAHAN POKOK DAN PENTING LAINNYA"] == bahan_terpilih]
            data_long = data_bahan.melt(id_vars=["Pasar"], var_name="Tanggal", value_name="Harga")
            data_long["Tanggal"] = pd.to_datetime(data_long["Tanggal"], errors="coerce")
            data_long["Harga"] = pd.to_numeric(data_long["Harga"], errors="coerce")
            data_long = data_long.dropna(subset=["Harga"])

            if data_long.empty:
                st.warning(f"Tidak ada data harga untuk '{bahan_terpilih}' di pasar '{pasar_terpilih}'.")
            else:
                data_long = data_long.sort_values("Tanggal")
                data_long["Fluktuasi"] = data_long["Harga"].diff()

                fig = px.line(data_long, x="Tanggal", y="Harga", title=f"Tren Harga {bahan_terpilih}", markers=True, template="plotly_dark")
                st.plotly_chart(fig)

                fig_fluktuasi = px.bar(data_long, x="Tanggal", y="Fluktuasi", title="Fluktuasi Harga", color="Fluktuasi", template="plotly_dark")
                st.plotly_chart(fig_fluktuasi)

                st.write("### Statistik Deskriptif")
                mean_price = data_long['Harga'].mean()
                median_price = data_long['Harga'].median()
                min_price = data_long['Harga'].min()
                max_price = data_long['Harga'].max()
                std_dev = data_long['Harga'].std()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Rata-rata Harga", value=f"{mean_price:,.2f}")
                    st.metric(label="Harga Minimum", value=f"{min_price:,.2f}")
                with col2:
                    st.metric(label="Median Harga", value=f"{median_price:,.2f}")
                    st.metric(label="Harga Maksimum", value=f"{max_price:,.2f}")
                with col3:
                    st.metric(label="Standar Deviasi", value=f"{std_dev:,.2f}")

                fig_box = go.Figure()
                fig_box.add_trace(go.Box(y=data_long["Harga"], name=bahan_terpilih, boxmean=True, marker_color="royalblue"))
                fig_box.update_layout(title="Distribusi Harga", template="plotly_dark")
                st.plotly_chart(fig_box)
        else:
            st.warning("Tidak ada data bahan pokok yang tersedia untuk pasar yang dipilih.")

    st.write("Dashboard by Farhan & Gilang")