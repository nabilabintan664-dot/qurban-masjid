import streamlit as st
import pandas as pd
import os
from datetime import datetime
import base64

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

# ============ INFORMASI BANK ============
BANK_INFO = {
    "Bank Syariah Indonesia (BSI)": {
        "no_rek": "7188888888",
        "an": "Masjid An-Nur",
        "kode_bank": "451"
    },
    "Bank Mandiri Syariah": {
        "no_rek": "7188888889", 
        "an": "Masjid An-Nur",
        "kode_bank": "451"
    }
}

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
    
    .info-rekening {
        background: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #2d5a2c;
        margin: 10px 0;
    }
    
    .tunai-card {
        background: #fff3e0;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #d4a017;
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
UPLOAD_DIR = "bukti_transfer"

# Buat folder untuk bukti transfer
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Kolom database yang benar
COLUMNS = [
    "Nama", "No HP", "Jenis Hewan", "Harga Hewan", 
    "Jumlah Dibayar", "Status Pembayaran", "Kelompok", 
    "Tanggal Daftar", "Metode Pembayaran", "Bank", 
    "Nama Panitia", "Bukti Transfer"
]

if not os.path.exists(DATA_FILE):
    df_empty = pd.DataFrame(columns=COLUMNS)
    df_empty.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ============ SESSION STATE ============
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ============ FORM PENDAFTARAN USER ============
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("## 📝 Form Pendaftaran Qurban")
st.markdown("Silakan isi data di bawah ini untuk mendaftar qurban")

with st.form("form_pendaftaran"):
    col1, col2 = st.columns(2)
    
    with col1:
        nama = st.text_input("Nama Lengkap *", placeholder="Contoh: Ahmad Fauzi")
        no_hp = st.text_input("Nomor WhatsApp/HP *", placeholder="081234567890")
        jenis = st.selectbox("Jenis Hewan Qurban *", ["Kambing", "Sapi"])
    
    with col2:
        if jenis == "Kambing":
            harga_tetap = HARGA_KAMBING
        else:
            harga_tetap = HARGA_SAPI
        
        st.number_input("Harga Hewan (Rp)", value=harga_tetap, disabled=True, label_visibility="collapsed")
        bayar = st.number_input("Jumlah Dibayar (Rp)", min_value=0, max_value=harga_tetap, step=50000, value=0)
        st.caption(f"Maksimal bayar Rp {harga_tetap:,.0f}")
    
    st.markdown("---")
    st.markdown("### 💳 Pilih Metode Pembayaran")
    
    metode = st.radio("Metode Pembayaran", ["Transfer Bank", "Tunai"], horizontal=True)
    
    bukti_file = None
    bank_terpilih = None
    nama_panitia = None
    
    if metode == "Transfer Bank":
        st.markdown('<div class="info-rekening">', unsafe_allow_html=True)
        st.markdown("**Informasi Rekening:**")
        bank_terpilih = st.selectbox("Pilih Bank", list(BANK_INFO.keys()))
        rek_info = BANK_INFO[bank_terpilih]
        st.code(f"""
No. Rekening: {rek_info['no_rek']}
Atas Nama: {rek_info['an']}
Kode Bank: {rek_info['kode_bank']}
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("**Upload Bukti Transfer:**")
        bukti_file = st.file_uploader("Upload screenshot/photo bukti transfer", type=["jpg", "jpeg", "png", "pdf"])
        if bukti_file:
            st.success("File berhasil diupload")
    
    else:  # Tunai
        st.markdown('<div class="tunai-card">', unsafe_allow_html=True)
        st.markdown("**Pilih Panitia yang akan menerima pembayaran:**")
        nama_panitia = st.selectbox("Nama Panitia", [
            "Bapak Ahmad (Ketua Panitia) - 081234567890",
            "Ibu Siti (Bendahara) - 081234567891", 
            "Bapak Rudi (Seksi Qurban) - 081234567892",
            "Ibu Fatimah (Seksi Pengumpulan) - 081234567893"
        ])
        st.info("Silakan hubungi panitia yang dipilih untuk konfirmasi pembayaran tunai.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("Daftar Qurban Sekarang", use_container_width=True)
    
    if submitted:
        error_msg = []
        if not nama:
            error_msg.append("Nama lengkap harus diisi")
        if not no_hp:
            error_msg.append("Nomor HP harus diisi")
        if bayar <= 0:
            error_msg.append("Jumlah pembayaran harus diisi")
        
        if error_msg:
            for err in error_msg:
                st.error(err)
        else:
            status = "Lunas" if bayar >= harga_tetap else "Kurang Bayar"
            tgl_daftar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Simpan bukti transfer jika ada
            bukti_path = ""
            if bukti_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                bukti_filename = f"{nama.replace(' ', '_')}_{timestamp}.{bukti_file.name.split('.')[-1]}"
                bukti_path = os.path.join(UPLOAD_DIR, bukti_filename)
                with open(bukti_path, "wb") as f:
                    f.write(bukti_file.getbuffer())
            
            df = load_data()
            data_baru = pd.DataFrame([{
                "Nama": nama,
                "No HP": no_hp,
                "Jenis Hewan": jenis,
                "Harga Hewan": harga_tetap,
                "Jumlah Dibayar": bayar,
                "Status Pembayaran": status,
                "Kelompok": "Belum Ditentukan",
                "Tanggal Daftar": tgl_daftar,
                "Metode Pembayaran": metode,
                "Bank": bank_terpilih if metode == "Transfer Bank" else "-",
                "Nama Panitia": nama_panitia if metode == "Tunai" else "-",
                "Bukti Transfer": bukti_path
            }])
            
            df = pd.concat([df, data_baru], ignore_index=True)
            save_data(df)
            st.balloons()
            st.success(f"""
            ✅ **Alhamdulillah, pendaftaran berhasil!**
            
            📋 **Detail Pendaftaran:**
            - Nama: {nama}
            - Jenis Hewan: {jenis}
            - Harga: Rp {harga_tetap:,.0f}
            - Dibayar: Rp {bayar:,.0f}
            - Status: {status}
            - Metode: {metode}
            
            🙏 Terima kasih telah berqurban di Masjid An-Nur.
            """)

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
    with st.expander("📊 Daftar Harga Tetap", expanded=True):
        st.markdown(f"""
        <div style="background: #f0f0f0; padding: 10px; border-radius: 10px;">
            <p><strong>🐐 Kambing</strong><br/>
            <span style="color:#2d5a2c; font-size:16px; font-weight:bold;">Rp {HARGA_KAMBING:,.0f}</span></p>
            <hr style="margin: 5px 0;">
            <p><strong>🐄 Sapi</strong><br/>
            <span style="color:#2d5a2c; font-size:16px; font-weight:bold;">Rp {HARGA_SAPI:,.0f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Login Admin
    if not st.session_state.admin_logged_in:
        with st.expander("🔐 Login Admin", expanded=False):
            admin_user = st.text_input("Username", placeholder="admin")
            admin_pass = st.text_input("Password", type="password", placeholder="admin123")
            if st.button("Login", use_container_width=True):
                if admin_user == "admin" and admin_pass == "admin123":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Username atau password salah!")
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d5a2c, #1e3a1e); padding: 8px; border-radius: 10px; text-align: center;">
            <span style="color: #ffd700;">✅ Admin Aktif</span>
        </div>
        """, unsafe_allow_html=True)
        
        menu_admin = st.radio(
            "📋 Panel Admin",
            ["📊 Dashboard", "💰 Update Pembayaran", "📁 Data & Laporan", "👥 Atur Kelompok", "🖼️ Lihat Bukti Transfer"]
        )
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="background: #f0f0f0; padding: 8px; border-radius: 10px;">
        <p style="color: #2d5a2c; font-size: 10px; text-align: center;">
        📞 Kontak: 0812-3456-7890<br/>
        ✉️ qurban@masjidannur.id
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============ MENU ADMIN ============
if st.session_state.admin_logged_in:
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    df = load_data()
    
    # Menu Dashboard
    if menu_admin == "📊 Dashboard":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 📊 Dashboard Qurban")
        
        if not df.empty:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            total_peserta = len(df)
            total_lunas = df[df["Status Pembayaran"] == "Lunas"].shape[0]
            total_kambing = df[df["Jenis Hewan"] == "Kambing"].shape[0]
            total_sapi = df[df["Jenis Hewan"] == "Sapi"].shape[0]
            total_dana = df["Jumlah Dibayar"].sum()
            
            with col1:
                st.markdown(f'<div class="stat-card"><div class="stat-number">{total_peserta}</div><div>Total Peserta</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="stat-card"><div class="stat-number">{total_lunas}</div><div>Peserta Lunas</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="stat-card"><div class="stat-number">{total_kambing}</div><div>Kambing</div></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="stat-card"><div class="stat-number">{total_sapi}</div><div>Sapi</div></div>', unsafe_allow_html=True)
            with col5:
                st.markdown(f'<div class="stat-card"><div class="stat-number">Rp {(total_dana/1000000):.0f}JT</div><div>Total Dana</div></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #d4a017, #ffd700); padding: 0.8rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                <h3 style="color: #1e3a1e; margin:0;">💰 Total Dana Terkumpul</h3>
                <h1 style="color: #1e3a1e; margin:0;">Rp {total_dana:,.0f}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Metode pembayaran chart sederhana
            metode_counts = df["Metode Pembayaran"].value_counts()
            st.markdown("### 📊 Metode Pembayaran")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Transfer Bank", metode_counts.get("Transfer Bank", 0))
            with col_b:
                st.metric("Tunai", metode_counts.get("Tunai", 0))
        else:
            st.info("Belum ada data pendaftaran.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Menu Update Pembayaran
    elif menu_admin == "💰 Update Pembayaran":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 💰 Update Pembayaran")
        
        if df.empty:
            st.warning("Belum ada data pendaftaran.")
        else:
            st.dataframe(df[["Nama", "Jenis Hewan", "Jumlah Dibayar", "Harga Hewan", "Status Pembayaran", "Metode Pembayaran"]], use_container_width=True)
            
            st.markdown("---")
            nama_peserta = st.selectbox("Pilih Peserta", df["Nama"].tolist())
            peserta_data = df[df["Nama"] == nama_peserta].iloc[0]
            
            st.info(f"""
            📋 **Data Peserta:**
            - Nama: {peserta_data['Nama']}
            - Jenis Hewan: {peserta_data['Jenis Hewan']}
            - Harga: Rp {peserta_data['Harga Hewan']:,.0f}
            - Sudah Dibayar: Rp {peserta_data['Jumlah Dibayar']:,.0f}
            - Status: {peserta_data['Status Pembayaran']}
            - Metode: {peserta_data['Metode Pembayaran']}
            """)
            
            max_bayar = peserta_data['Harga Hewan'] - peserta_data['Jumlah Dibayar']
            if max_bayar <= 0:
                st.success("✅ Peserta ini sudah LUNAS!")
            else:
                tambah_bayar = st.number_input("Tambah Pembayaran (Rp)", min_value=0, max_value=max_bayar, step=50000)
                if st.button("Update Pembayaran"):
                    idx = df[df["Nama"] == nama_peserta].index[0]
                    total_baru = df.loc[idx, "Jumlah Dibayar"] + tambah_bayar
                    harga_hewan = df.loc[idx, "Harga Hewan"]
                    df.loc[idx, "Jumlah Dibayar"] = total_baru
                    df.loc[idx, "Status Pembayaran"] = "Lunas" if total_baru >= harga_hewan else "Kurang Bayar"
                    save_data(df)
                    st.success(f"✅ Pembayaran {nama_peserta} berhasil diupdate!")
                    st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Menu Data & Laporan
    elif menu_admin == "📁 Data & Laporan":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 📁 Data & Laporan Qurban")
        
        if df.empty:
            st.info("Belum ada data pendaftaran.")
        else:
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV", 
                csv, 
                f"laporan_qurban_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Menu Atur Kelompok
    elif menu_admin == "👥 Atur Kelompok":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 👥 Atur Kelompok Qurban")
        
        if df.empty:
            st.warning("Belum ada data pendaftaran.")
        else:
            df_lunas = df[df["Status Pembayaran"] == "Lunas"].copy()
            
            if df_lunas.empty:
                st.warning("Belum ada peserta dengan status LUNAS.")
            else:
                kelompok_list = []
                kelompok_id = 1
                
                for _, row in df_lunas.iterrows():
                    if row["Jenis Hewan"] == "Kambing":
                        kelompok_list.append({
                            "Nama": row["Nama"],
                            "Jenis": "Kambing",
                            "Kelompok": f"Kelompok {kelompok_id} (Kambing)"
                        })
                        kelompok_id += 1
                    else:
                        kelompok_list.append({
                            "Nama": row["Nama"],
                            "Jenis": "Sapi",
                            "Kelompok": f"Kelompok {kelompok_id} (Sapi)"
                        })
                        kelompok_id += 1
                
                df_kelompok = pd.DataFrame(kelompok_list)
                
                for _, row in df_kelompok.iterrows():
                    df.loc[df["Nama"] == row["Nama"], "Kelompok"] = row["Kelompok"]
                save_data(df)
                
                st.success("✅ Kelompok berhasil dibuat!")
                st.dataframe(df_kelompok, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Menu Lihat Bukti Transfer
    elif menu_admin == "🖼️ Lihat Bukti Transfer":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## 🖼️ Bukti Transfer Peserta")
        
        if df.empty:
            st.warning("Belum ada data.")
        else:
            df_transfer = df[df["Metode Pembayaran"] == "Transfer Bank"]
            df_transfer = df_transfer[df_transfer["Bukti Transfer"] != ""]
            
            if df_transfer.empty:
                st.info("Belum ada bukti transfer yang diupload.")
            else:
                peserta_options = df_transfer["Nama"].tolist()
                selected_peserta = st.selectbox("Pilih Peserta", peserta_options)
                
                peserta_data = df_transfer[df_transfer["Nama"] == selected_peserta].iloc[0]
                bukti_path = peserta_data["Bukti Transfer"]
                
                if os.path.exists(bukti_path):
                    st.success(f"Bukti transfer dari: {selected_peserta}")
                    
                    # Tampilkan gambar jika file gambar
                    if bukti_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(bukti_path, caption=f"Bukti Transfer - {selected_peserta}", use_container_width=True)
                    
                    # Download button untuk bukti
                    with open(bukti_path, "rb") as f:
                        file_data = f.read()
                        file_name = os.path.basename(bukti_path)
                        st.download_button(
                            label="📥 Download Bukti Transfer",
                            data=file_data,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )
                else:
                    st.error(f"File bukti tidak ditemukan: {bukti_path}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class="custom-divider"></div>
<footer>
    🌙 QurbanHub - Sains dan Teknologi Islam | Kurban Digital Masjid An-Nur 🌙<br>
    Semoga amal ibadah kita diterima oleh Allah SWT
</footer>
""", unsafe_allow_html=True)
