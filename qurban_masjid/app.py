import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Qurban - Sistem Kurban Digital Masjid",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ HARGA TETAP ============
HARGA_KAMBING = 3500000  # Rp 3.500.000
HARGA_SAPI = 15000000    # Rp 15.000.000

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fdf8e7 0%, #f5e6c8 50%, #e8d5b5 100%);
    }
    
    .hero {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1562165617-ee9a6af4e7c2?ixlib=rb-4.0.3');
        background-size: cover;
        background-position: center;
        padding: 2rem;
        border-radius: 30px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero h1 {
        font-family: 'Amiri', serif;
        font-size: 2.5rem;
        color: #ffd700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 0;
    }
    
    .hero h3 {
        color: white;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    .hero p {
        color: #ffd700;
        font-style: italic;
        font-size: 0.9rem;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,215,0,0.3);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .animal-card {
        text-align: center;
        background: white;
        border-radius: 20px;
        padding: 1.2rem;
        margin: 0.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    
    .animal-card:hover {
        transform: scale(1.03);
    }
    
    .animal-card h2 {
        color: #2d5a2c;
        margin: 10px 0 5px 0;
        font-size: 1.5rem;
    }
    
    .price-box {
        background: linear-gradient(135deg, #1e3a1e, #2d5a2c);
        border-radius: 15px;
        padding: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .price-box p {
        color: #ffd700;
        margin: 0;
        font-size: 12px;
    }
    
    .price-box h3 {
        color: #ffd700;
        margin: 0;
        font-size: 1.1rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #2d5a2c, #1e3a1e);
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        color: white;
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        font-family: 'Amiri', serif;
    }
    
    .watermark {
        position: fixed;
        bottom: 15px;
        right: 15px;
        background: rgba(0,0,0,0.7);
        color: #ffd700;
        padding: 5px 12px;
        border-radius: 30px;
        font-size: 10px;
        z-index: 999;
        font-family: 'Amiri', serif;
        backdrop-filter: blur(5px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #d4a017, #c4920a);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #c4920a, #b8860b);
        transform: scale(1.02);
    }
    
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #d4a017, #ffd700, #d4a017);
        margin: 1.5rem 0;
        border-radius: 3px;
    }
    
    footer {
        text-align: center;
        padding: 1rem 0;
        color: #8B7355;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ============ WATERMARK ============
st.markdown("""
<div class="watermark">
    🕌 Dikembangkan oleh nabila, dini, bella, lia • QurbanHub Digital
</div>
""", unsafe_allow_html=True)

# ============ HERO SECTION ============
st.markdown("""
<div class="hero">
    <h1>🕌 Qurban 1446 H 🕌</h1>
    <h3>✨ Tebarkan Berkah dengan Qurban Digital ✨</h3>
    <p>"Maka dirikanlah shalat karena Tuhanmu dan berqurbanlah" (QS. Al-Kautsar: 2)</p>
</div>
""", unsafe_allow_html=True)


# ============ INISIALISASI DATA ============
DATA_FILE = "data_qurban.csv"

if not os.path.exists(DATA_FILE):
    df_empty = pd.DataFrame(columns=[
        "Nama", "No HP", "Jenis Hewan", "Harga Hewan", 
        "Jumlah Dibayar", "Status Pembayaran", "Kelompok", "Tanggal Daftar"
    ])
    df_empty.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ============ SESSION STATE ADMIN ============
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ============ FORM PENDAFTARAN USER ============
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("## Form Pendaftaran Qurban")
st.markdown("Silakan isi data dibawah ini untuk mendaftar qurban")

col1, col2 = st.columns(2)

with col1:
    nama = st.text_input("Nama Lengkap", placeholder="Contoh: Ahmad Fauzi", key="nama_user")
    no_hp = st.text_input("Nomor WhatsApp/HP", placeholder="081234567890", key="nohp_user")
    jenis = st.selectbox("Jenis Hewan Qurban", ["Kambing", "Sapi"], key="jenis_user")
    
    if jenis == "Kambing":
        harga_tetap = HARGA_KAMBING
        st.info(f"Harga Kambing: **Rp {harga_tetap:,.0f}** (wajib tetap)")
    else:
        harga_tetap = HARGA_SAPI
        st.info(f"Harga Sapi: **Rp {harga_tetap:,.0f}** (wajib tetap)")

with col2:
    st.number_input("Harga Hewan (Rp)", value=harga_tetap, disabled=True, key="harga_display")
    bayar = st.number_input("Jumlah Dibayar (Rp)", min_value=0, max_value=harga_tetap, step=50000, key="bayar_user")
    st.caption(f"💡 Maksimal bayar Rp {harga_tetap:,.0f}")

if st.button("Daftar Qurban Sekarang", use_container_width=True, key="btn_daftar"):
    if nama and no_hp:
        if bayar > harga_tetap:
            st.error(f"Pembayaran tidak boleh lebih dari Rp {harga_tetap:,.0f}")
        else:
            status = "Lunas" if bayar >= harga_tetap else "Kurang Bayar"
            tgl_daftar = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            df = load_data()
            data_baru = pd.DataFrame([{
                "Nama": nama, "No HP": no_hp, "Jenis Hewan": jenis,
                "Harga Hewan": harga_tetap, "Jumlah Dibayar": bayar,
                "Status Pembayaran": status, "Kelompok": "belum Ditentukan",
                "Tanggal Daftar": tgl_daftar
            }])
            df = pd.concat([df, data_baru], ignore_index=True)
            save_data(df)
            st.balloons()
            st.success(f"""
            **Alhamdulillah, pendaftaran berhasil!**  
            Nama: {nama}  
            Jenis: {jenis}  
            Dibayar: Rp {bayar:,.0f}  
            Status: {status}  
            
            Terimaksih telah berqurban di Masjid An-Nur.
            """)
    else:
        st.error("Nama dan No HP wajib diisi!")

st.markdown('</div>', unsafe_allow_html=True)

# ============ SIDEBAR ADMIN ============
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2888/2888406.png", width=70)
    st.markdown("""
    <div style="text-align: center;">
        <h3 style="color: #2d5a2c;">🕌 Masjid An-Nur</h3>
        <p style="color: #666; font-size: 11px;">Sistem Informasi Qurban Digital</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Daftar harga
    with st.expander("Daftar Harga Tetap", expanded=True):
        st.markdown(f"""
        <div style="background: #f0f0f0; padding: 10px; border-radius: 10px;">
            <p><span style="font-size:20px;"></span> <strong>Kambing</strong><br/>
            <span style="color:#2d5a2c; font-size:16px; font-weight:bold;">Rp {HARGA_KAMBING:,.0f}</span></p>
            <hr style="margin: 5px 0;">
            <p><span style="font-size:20px;"></span> <strong>Sapi</strong><br/>
            <span style="color:#2d5a2c; font-size:16px; font-weight:bold;">Rp {HARGA_SAPI:,.0f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Login Admin
    if not st.session_state.admin_logged_in:
        with st.expander("Login Admin", expanded=False):
            admin_user = st.text_input("Username", placeholder="admin")
            admin_pass = st.text_input("Password", type="password", placeholder="admin123")
            if st.button("Login", use_container_width=True):
                if admin_user == "admin" and admin_pass == "admin123":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Salah!")
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d5a2c, #1e3a1e); padding: 8px; border-radius: 10px; text-align: center;">
            <span style="color: #ffd700;">Admin Aktif</span>
        </div>
        """, unsafe_allow_html=True)
        
        menu_admin = st.radio(
            "Panel Admin",
            ["Update Pembayaran", "Data & Laporan", "Atur Kelompok"]
        )
        
        if st.button("Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="background: #f0f0f0; padding: 8px; border-radius: 10px;">
        <p style="color: #2d5a2c; font-size: 10px; text-align: center;">
        Kontak: 0812-3456-7890<br/>
        qurban@masjidannur.id
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============ MENU ADMIN ============
if st.session_state.admin_logged_in:
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    df = load_data()
    
    # Menu 1: Update Pembayaran
    if menu_admin == "Update Pembayaran":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## Update Pembayaran")
        
        if df.empty:
            st.warning("Belum ada data.")
        else:
            st.dataframe(df[["Nama", "Jenis Hewan", "Jumlah Dibayar", "Harga Hewan", "Status Pembayaran"]], use_container_width=True)
            
            st.markdown("---")
            nama_peserta = st.selectbox("Pilih Peserta", df["Nama"].tolist())
            peserta_data = df[df["Nama"] == nama_peserta].iloc[0]
            
            st.info(f"""
            **Data:**  
            - Jenis: {peserta_data['Jenis Hewan']}  
            - Harga: Rp {peserta_data['Harga Hewan']:,.0f}  
            - Dibayar: Rp {peserta_data['Jumlah Dibayar']:,.0f}  
            - Status: {peserta_data['Status Pembayaran']}
            """)
            
            max_bayar = peserta_data['Harga Hewan'] - peserta_data['Jumlah Dibayar']
            if max_bayar <= 0:
                st.success("Peserta iki wis LUNAS!")
            else:
                tambah_bayar = st.number_input("Tambah Bayar (Rp)", min_value=0, max_value=max_bayar, step=50000)
                if st.button("Update"):
                    idx = df[df["Nama"] == nama_peserta].index[0]
                    total_baru = df.loc[idx, "Jumlah Dibayar"] + tambah_bayar
                    harga_hewan = df.loc[idx, "Harga Hewan"]
                    df.loc[idx, "Jumlah Dibayar"] = total_baru
                    df.loc[idx, "Status Pembayaran"] = "Lunas" if total_baru >= harga_hewan else "Kurang Bayar"
                    save_data(df)
                    st.success(f"Pembayaran {nama_peserta} update!")
                    st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Menu 2: Data & Laporan
    elif menu_admin == "Data & Laporan":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## Laporan Qurban")
        
        if df.empty:
            st.info("belum ada data.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            total_peserta = len(df)
            total_lunas = df[df["Status Pembayaran"] == "Lunas"].shape[0]
            total_kambing = df[df["Jenis Hewan"] == "Kambing"].shape[0]
            total_sapi = df[df["Jenis Hewan"] == "Sapi"].shape[0]
            total_dana = df["Jumlah Dibayar"].sum()
            
            with col1:
                st.markdown(f'<div class="stat-card"><div style="font-size:1.5rem;"></div><div class="stat-number">{total_peserta}</div><div>Total Peserta</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="stat-card"><div style="font-size:1.5rem;"></div><div class="stat-number">{total_lunas}</div><div>Lunas</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="stat-card"><div style="font-size:1.5rem;"></div><div class="stat-number">{total_kambing}</div><div>Kambing</div></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="stat-card"><div style="font-size:1.5rem;"></div><div class="stat-number">{total_sapi}</div><div>Sapi</div></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #d4a017, #ffd700); padding: 0.8rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                <h3 style="color: #1e3a1e; margin:0;">Total Dana Terkumpul</h3>
                <h1 style="color: #1e3a1e; margin:0;">Rp {total_dana:,.0f}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, f"laporan_qurban_{datetime.now().strftime('%Y%m%d')}.csv", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Menu 3: Atur Kelompok
    elif menu_admin == "Atur Kelompok":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## Atur Kelompok Qurban")
        
        if df.empty:
            st.warning("Belum ada data.")
        else:
            df_lunas = df[df["Status Pembayaran"] == "Lunas"].copy()
            
            if df_lunas.empty:
                st.warning("Belum ada yang LUNAS.")
            else:
                kelompok_list = []
                kelompok_id = 1
                
                for _, row in df_lunas.iterrows():
                    if "Kambing" in row["Jenis Hewan"]:
                        kelompok_list.append({"Nama": row["Nama"], "Jenis": "Kambing", "Kelompok": f"Kelompok {kelompok_id} "})
                        kelompok_id += 1
                    else:
                        kelompok_list.append({"Nama": row["Nama"], "Jenis": "Sapi", "Kelompok": f"Kelompok {kelompok_id} "})
                        kelompok_id += 1
                
                df_kelompok = pd.DataFrame(kelompok_list)
                
                for _, row in df_kelompok.iterrows():
                    df.loc[df["Nama"] == row["Nama"], "Kelompok"] = row["Kelompok"]
                save_data(df)
                
                st.success("Kelompok kasil digawe!")
                st.dataframe(df_kelompok, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class="custom-divider"></div>
<footer>
    🌙 QurbanHub - Sains dan Teknologi Islam Kurban Digital | Masjid An-Nur 🌙<br>
    Semoga amal ibadah kita diterima oleh Allah SWT
</footer>
""", unsafe_allow_html=True)
