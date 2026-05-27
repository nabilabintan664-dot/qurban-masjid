import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Qurban - Masjid At- taubah",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ INISIALISASI DATABASE ============
DATA_FILE = "pesanan_qurban.csv"
UPLOAD_DIR = "bukti_transfer"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Kolom database
COLUMNS = [
    "Nama_Mudhohi", "No_HP", "Jenis_Hewan", "Harga", 
    "Jumlah_Dibayar", "Status_Pembayaran", "Metode",
    "Doa_Harapan", "Tanggal_Pesan", "Bukti_Transfer"
]

if not os.path.exists(DATA_FILE):
    df_empty = pd.DataFrame(columns=COLUMNS)
    df_empty.to_csv(DATA_FILE, index=False)

def load_pesanan():
    return pd.read_csv(DATA_FILE)

def save_pesanan(df):
    df.to_csv(DATA_FILE, index=False)

# ============ SESSION STATE ============
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "selected_hewan" not in st.session_state:
    st.session_state.selected_hewan = None

# ============ DATA HEWAN ============
HEWAN_KURBAN = [
    {"nama": "Kambing Standar", "bobot": "25-30 kg", "harga": 3200000, "stok": 12, "icon": "🐐"},
    {"nama": "Kambing Premium", "bobot": "35-40 kg", "harga": 4500000, "stok": 8, "icon": "🐏"},
    {"nama": "Sapi Standar (Utuh)", "bobot": "180-220 kg", "harga": 16500000, "stok": 5, "icon": "🐄"},
    {"nama": "1/7 Sapi Standar", "bobot": "Patungan", "harga": 2400000, "stok": 35, "icon": "🥩"},
    {"nama": "Sapi Premium (Utuh)", "bobot": "250-300 kg", "harga": 21000000, "stok": 3, "icon": "🐂"},
    {"nama": "1/7 Sapi Premium", "bobot": "Patungan", "harga": 3000000, "stok": 21, "icon": "🥩"},
]

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    /* Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: #fafaf8; }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #0a3e2c 0%, #1a5a3a 100%);
        padding: 2rem;
        border-radius: 0 0 40px 40px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .main-header h1 { font-size: 2.2rem; font-weight: 800; color: #ffd966; margin: 0; }
    .main-header p { opacity: 0.9; margin-top: 0.5rem; }
    
    /* Statistik */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: -1.5rem 0 2rem 0;
        flex-wrap: wrap;
    }
    .stat-badge {
        background: white;
        border-radius: 30px;
        padding: 0.4rem 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    }
    .stat-badge .number { font-size: 1.2rem; font-weight: 800; color: #1a5a3a; }
    .stat-badge .label { font-size: 0.7rem; color: #666; }
    
    /* Card Katalog */
    .catalog-title { text-align: center; margin: 2rem 0; }
    .catalog-title h2 { font-size: 1.8rem; font-weight: 700; color: #1a5a3a; }
    
    .qurban-card {
        background: white;
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        border: 1px solid #eef2e6;
        text-align: center;
    }
    .qurban-card:hover { transform: translateY(-4px); }
    .card-icon { font-size: 2.2rem; }
    .card-title { font-size: 1rem; font-weight: 700; color: #1a5a3a; margin: 0.3rem 0; }
    .card-price { font-size: 1.2rem; font-weight: 800; color: #1a5a3a; }
    .stock-badge {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        font-size: 0.65rem;
        display: inline-block;
    }
    .btn-pesan {
        background: #1a5a3a;
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.4rem 0.8rem;
        width: 100%;
        font-weight: 600;
        margin-top: 0.6rem;
        cursor: pointer;
    }
    
    /* Modal Form Style */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .modal-content {
        background: white;
        border-radius: 24px;
        padding: 1.5rem;
        max-width: 500px;
        width: 90%;
        max-height: 85vh;
        overflow-y: auto;
        position: relative;
    }
    
    /* Footer */
    .footer {
        background: #0a3e2c;
        color: white;
        padding: 1.5rem;
        border-radius: 30px 30px 0 0;
        margin-top: 2rem;
        text-align: center;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
<div class="main-header">
    <h1>🕌 Qurban Masjid At-taubah 1447 H</h1>
    <p>Tebarkan berkah & pilih hewan qurban terbaikmu</p>
</div>
""", unsafe_allow_html=True)

# ============ STATISTIK ============
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-badge"><span class="number">🐐 5+</span><div class="label">Jenis Hewan</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-badge"><span class="number">📍 3</span><div class="label">Lokasi Penyaluran</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-badge"><span class="number">👥 120+</span><div class="label">Peserta Aktif</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-badge"><span class="number">🌙 1447 H</span><div class="label">Tahun Qurban</div></div>', unsafe_allow_html=True)

# ============ KATALOG ============
st.markdown('<div class="catalog-title"><h2> Katalog Hewan Qurban</h2><p>Pilih hewan qurban sesuai kemampuan Anda</p></div>', unsafe_allow_html=True)

# Tampilkan grid 3 kolom
cols = st.columns(3)
for idx, hewan in enumerate(HEWAN_KURBAN):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="qurban-card">
            <div class="card-icon">{hewan['icon']}</div>
            <div class="card-title">{hewan['nama']}</div>
            <div class="card-price">Rp {hewan['harga']:,.0f}</div>
            <div class="stock-badge"> Stok: {hewan['stok']} </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tombol pesan dengan callback
        if st.button(f"Pesan {hewan['nama']}", key=f"btn_{idx}", use_container_width=True):
            st.session_state.show_form = True
            st.session_state.selected_hewan = hewan
            st.rerun()

# ============ MODAL FORM PEMESANAN (Seperti Infakin) ============
if st.session_state.show_form and st.session_state.selected_hewan:
    hewan = st.session_state.selected_hewan
    
    with st.form(key="form_pemesanan"):
        st.markdown(f"""
        <div style="background: #f0f7f0; padding: 0.8rem; border-radius: 16px; margin-bottom: 1rem;">
            <h3 style="color:#1a5a3a;"> Isi data berikut</h3>
            <p><strong>Hewan:</strong> {hewan['nama']} | <strong>Harga:</strong> Rp {hewan['harga']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form fields seperti Infakin
        nama_mudhohi = st.text_input("Nama Mudhohi (Yang berqurban) *", placeholder="Contoh: Ahmad bin Abdullah")
        no_hp = st.text_input("Nomor WhatsApp/HP *", placeholder="081234567890")
        doa_harapan = st.text_area("Doa & Harapan (Opsional)", placeholder="Doakan orang tua saya...\nSemoga diterima amal ibadah kami...", height=100)
        
        # Pilihan metode pembayaran
        st.markdown("**Metode Pembayaran**")
        metode = st.radio("", ["Transfer Bank (QRIS/BSI/Mandiri)", "Tunai (ke masjid)"], horizontal=True)
        
        bukti_file = None
        if "Transfer" in metode:
            st.info(" Silakan transfer ke BSI 7188888888 a.n Masjid An-Nur")
            bukti_file = st.file_uploader("Upload bukti transfer", type=["jpg", "png", "pdf"])
        
        # Jumlah yang mau dibayar
        bayar = st.number_input("Jumlah yang ingin dibayar (Rp)", min_value=0, max_value=hewan['harga'], value=min(hewan['harga'], 500000), step=50000)
        
        submitted = st.form_submit_button(" KIRIM PEMESANAN", use_container_width=True)
        
        if submitted:
            error_msg = []
            if not nama_mudhohi:
                error_msg.append("Nama mudhohi wajib diisi")
            if not no_hp:
                error_msg.append("Nomor HP wajib diisi")
            if "Transfer" in metode and bukti_file is None:
                error_msg.append("Untuk transfer bank, wajib upload bukti transfer")
            
            if error_msg:
                for err in error_msg:
                    st.error(err)
            else:
                # Simpan bukti
                bukti_path = ""
                if bukti_file:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    bukti_filename = f"{nama_mudhohi.replace(' ', '_')}_{timestamp}.{bukti_file.name.split('.')[-1]}"
                    bukti_path = os.path.join(UPLOAD_DIR, bukti_filename)
                    with open(bukti_path, "wb") as f:
                        f.write(bukti_file.getbuffer())
                
                # Simpan ke database
                status = "Lunas" if bayar >= hewan['harga'] else "Kurang Bayar"
                df = load_pesanan()
                data_baru = pd.DataFrame([{
                    "Nama_Mudhohi": nama_mudhohi,
                    "No_HP": no_hp,
                    "Jenis_Hewan": hewan['nama'],
                    "Harga": hewan['harga'],
                    "Jumlah_Dibayar": bayar,
                    "Status_Pembayaran": status,
                    "Metode": metode,
                    "Doa_Harapan": doa_harapan,
                    "Tanggal_Pesan": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Bukti_Transfer": bukti_path
                }])
                df = pd.concat([df, data_baru], ignore_index=True)
                save_pesanan(df)
                
                st.balloons()
                st.success(f"""
                 **Pesanan berhasil dikirim!**
                
                Terima kasih {nama_mudhohi}, pesanan {hewan['nama']} telah tercatat.
                Panitia akan menghubungi Anda dalam 1x24 jam.
                """)
                
                # Reset form
                st.session_state.show_form = False
                st.session_state.selected_hewan = None
                st.rerun()
    
    # Tombol close modal
    if st.button(" Tutup", use_container_width=True):
        st.session_state.show_form = False
        st.session_state.selected_hewan = None
        st.rerun()

# ============ KEUNGGULAN ============
st.markdown("""
<div style="background: white; border-radius: 24px; padding: 1.5rem; margin: 2rem 0;">
    <div style="text-align: center;"><h3 style="color:#1a5a3a;">✨ Keunggulan Qurban di Masjid An-Nur</h3></div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); gap: 1rem; margin-top: 1rem;">
        <div style="text-align:center;"><span style="font-size:1.8rem;">🕌</span><br/><strong>Langganan Masjid</strong><br/><small>DKM mengawal langsung</small></div>
        <div style="text-align:center;"><span style="font-size:1.8rem;">📱</span><br/><strong>Notifikasi WA</strong><br/><small>Update real-time</small></div>
        <div style="text-align:center;"><span style="font-size:1.8rem;">🎯</span><br/><strong>Tepat Sasaran</strong><br/><small>Mustahik sekitar masjid</small></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class="footer">
    <h4>🕌 Masjid At-taubah</h4>
    <p>Jalan Candi No. 123, Kota Sidoarjo | Telp: (021) 1234-5678<br/>
    WhatsApp: 0812-3456-7890 | Email: qurban@masjidannur.id</p>
    <small>© 1447 H / 2026 M • Bintan Nabilah-Dini Oktabiyanti-Sinta Bella-Aulia Riska</small>
</div>
""", unsafe_allow_html=True)

# ============ SIDEBAR ADMIN ============
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2888/2888406.png", width=50)
    st.markdown("###  Admin Masjid")
    
    if not st.session_state.admin_logged_in:
        with st.expander(" Login Admin", expanded=True):
            user = st.text_input("Username", placeholder="admin")
            pwd = st.text_input("Password", type="password", placeholder="admin123")
            if st.button("Login", use_container_width=True):
                if user == "admin" and pwd == "admin123":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Salah!")
    else:
        st.success(" Admin aktif")
        
        # Dashboard Admin
        df = load_pesanan()
        
        st.markdown("---")
        st.markdown("###  Dashboard Admin")
        
        if df.empty:
            st.info("Belum ada pesanan")
        else:
            st.metric("Total Pesanan", len(df))
            st.metric("Pesanan Lunas", df[df["Status_Pembayaran"] == "Lunas"].shape[0])
            st.metric("Kurang Bayar", df[df["Status_Pembayaran"] == "Kurang Bayar"].shape[0])
        
        menu = st.radio("Menu", [" Daftar Pesanan", " Update Status", " Laporan"], key="admin_menu")
        
        if menu == " Daftar Pesanan":
            st.dataframe(df, use_container_width=True)
            
            # Lihat detail & bukti
            if not df.empty:
                pilih = st.selectbox("Lihat detail pesanan", df["Nama_Mudhohi"].tolist())
                detail = df[df["Nama_Mudhohi"] == pilih].iloc[0]
                st.json(detail.to_dict())
                if detail["Bukti_Transfer"] and os.path.exists(detail["Bukti_Transfer"]):
                    st.image(detail["Bukti_Transfer"], caption="Bukti Transfer", width=200)
        
        elif menu == " Update Status":
            if not df.empty:
                pilih = st.selectbox("Pilih pesanan", df["Nama_Mudhohi"].tolist())
                idx = df[df["Nama_Mudhohi"] == pilih].index[0]
                status_baru = st.selectbox("Status Baru", ["Lunas", "Kurang Bayar", "Batal"])
                if st.button("Update"):
                    df.loc[idx, "Status_Pembayaran"] = status_baru
                    save_pesanan(df)
                    st.success("Status diupdate!")
                    st.rerun()
        
        elif menu == " Laporan":
            st.download_button("Download CSV", df.to_csv(index=False), "laporan_qurban.csv")
        
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
