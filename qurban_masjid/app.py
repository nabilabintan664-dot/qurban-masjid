import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Kurban - Masjid An-Nur",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ DATA HEWAN KURBAN MASJID ============
# Data khusus untuk satu masjid dengan stok terbatas
HEWAN_KURBAN = [
    {
        "nama": "Kambing Standar",
        "kategori": "Kambing",
        "bobot": "25-30 kg",
        "harga": 3200000,
        "stok": 12,
        "deskripsi": "Kambing lokal sehat, cocok untuk 1 orang",
        "icon": "🐐"
    },
    {
        "nama": "Kambing Premium",
        "kategori": "Kambing",
        "bobot": "35-40 kg",
        "harga": 4500000,
        "stok": 8,
        "deskripsi": "Kambing pilihan dengan bobot besar",
        "icon": "🐏"
    },
    {
        "nama": "Sapi Standar",
        "kategori": "Sapi",
        "bobot": "180-220 kg",
        "harga": 16500000,
        "stok": 5,
        "deskripsi": "Sapi lokal sehat untuk 7 orang",
        "icon": "🐄"
    },
    {
        "nama": "1/7 Sapi Standar",
        "kategori": "Sapi (Patungan)",
        "bobot": "180-220 kg",
        "harga": 2400000,
        "stok": 35,
        "deskripsi": "Bergabung dengan 6 orang lainnya",
        "icon": "🥩"
    },
    {
        "nama": "Sapi Premium",
        "kategori": "Sapi",
        "bobot": "250-300 kg",
        "harga": 21000000,
        "stok": 3,
        "deskripsi": "Sapi impor berkualitas tinggi",
        "icon": "🐂"
    },
    {
        "nama": "1/7 Sapi Premium",
        "kategori": "Sapi (Patungan)",
        "bobot": "250-300 kg",
        "harga": 3000000,
        "stok": 21,
        "deskripsi": "Patungan 7 orang untuk sapi premium",
        "icon": "🥩"
    },
    {
        "nama": "Kerbau Lokal",
        "kategori": "Kerbau",
        "bobot": "200-250 kg",
        "harga": 18500000,
        "stok": 2,
        "deskripsi": "Alternatif hewan kurban",
        "icon": "🐃"
    },
    {
        "nama": "Sedekah Daging",
        "kategori": "Sedekah",
        "bobot": "-",
        "harga": 75000,
        "stok": 999,
        "deskripsi": "Donasi untuk pembagian daging ke mustahik",
        "icon": "🤲"
    }
]

# ============ CUSTOM CSS (Gaya Qurbanholic) ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: #fafaf8;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #0a3e2c 0%, #1a5a3a 100%);
        padding: 2rem 2rem 4rem 2rem;
        border-radius: 0 0 40px 40px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: #ffd966;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Statistik Masjid */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: -2rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .stat-badge {
        background: white;
        border-radius: 30px;
        padding: 0.5rem 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .stat-badge .number {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1a5a3a;
    }
    
    .stat-badge .label {
        font-size: 0.7rem;
        color: #666;
    }
    
    /* Card Katalog */
    .catalog-title {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .catalog-title h2 {
        font-size: 2rem;
        font-weight: 700;
        color: #1a5a3a;
    }
    
    .catalog-title p {
        color: #666;
    }
    
    .qurban-card {
        background: white;
        border-radius: 24px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid #eef2e6;
    }
    
    .qurban-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .card-icon {
        font-size: 2.5rem;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a5a3a;
        margin: 0.5rem 0 0.2rem 0;
    }
    
    .card-bobot {
        font-size: 0.75rem;
        color: #b89a4c;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .card-price {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1a5a3a;
        margin: 0.5rem 0;
    }
    
    .card-price small {
        font-size: 0.7rem;
        font-weight: normal;
        color: #666;
    }
    
    .stock-badge {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .stock-low {
        background: #ffebee;
        color: #c62828;
    }
    
    .btn-pesan {
        background: #1a5a3a;
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.5rem 1rem;
        width: 100%;
        font-weight: 600;
        margin-top: 0.8rem;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .btn-pesan:hover {
        background: #0a3e2c;
    }
    
    /* Keunggulan */
    .feature-section {
        background: #ffffff;
        border-radius: 30px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    .feature-card {
        text-align: center;
        padding: 1rem;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .footer {
        background: #0a3e2c;
        color: white;
        padding: 2rem;
        border-radius: 30px 30px 0 0;
        margin-top: 3rem;
        text-align: center;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, #1a5a3a, #ffd966, #1a5a3a);
        margin: 1.5rem 0;
    }
    
    /* Sidebar Style */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #eef2e6;
    }
</style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
<div class="main-header">
    <h1>🕌 Qurban Masjid An-Nur 1447 H</h1>
    <p>Kuatkan niat dan pilih hewan qurban terbaikmu • Tebarkan berkah untuk sesama</p>
</div>
""", unsafe_allow_html=True)

# ============ STATISTIK MASJID ============
total_stok = sum(h["stok"] for h in HEWAN_KURBAN if h["stok"] > 0)
total_jenis = len([h for h in HEWAN_KURBAN if h["stok"] > 0])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stat-badge"><span class="number">🐐 20+</span><div class="label">Hewan Tersedia</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-badge"><span class="number">📍 3</span><div class="label">Lokasi Penyaluran</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-badge"><span class="number">👥 150+</span><div class="label">Peserta Aktif</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stat-badge"><span class="number">🌙 1447 H</span><div class="label">Tahun Qurban</div></div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============ KATALOG HEWAN KURBAN ============
st.markdown("""
<div class="catalog-title">
    <h2>📦 Katalog Hewan Qurban</h2>
    <p>Pilih hewan qurban yang sesuai dengan kemampuan Anda</p>
</div>
""", unsafe_allow_html=True)

# Filter kategori
kategori_list = ["Semua"] + list(set(h["kategori"] for h in HEWAN_KURBAN))
selected_kategori = st.selectbox("Filter berdasarkan jenis:", kategori_list, index=0)

# Filter berdasarkan kategori
filtered_hewan = HEWAN_KURBAN
if selected_kategori != "Semua":
    filtered_hewan = [h for h in HEWAN_KURBAN if h["kategori"] == selected_kategori]

# Tampilkan dalam grid 4 kolom
cols = st.columns(4)
for idx, hewan in enumerate(filtered_hewan):
    with cols[idx % 4]:
        stock_class = "stock-badge"
        if hewan["stok"] <= 3 and hewan["stok"] > 0:
            stock_class += " stock-low"
        
        stock_text = f"Stok: {hewan['stok']}" if hewan["stok"] < 999 else "Stok: Unlimited"
        
        st.markdown(f"""
        <div class="qurban-card">
            <div class="card-icon">{hewan['icon']}</div>
            <div class="card-title">{hewan['nama']}</div>
            <div class="card-bobot">⚖️ Bobot: {hewan['bobot']}</div>
            <div class="card-price">Rp {hewan['harga']:,.0f}<small>/ekor</small></div>
            <div class="{stock_class}">{stock_text}</div>
            <button class="btn-pesan" onclick="alert('Pesan: {hewan['nama']}')">Pesan Sekarang →</button>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============ KEUNGGULAN MASJID ============
st.markdown("""
<div class="feature-section">
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #1a5a3a;">✨ Keunggulan Qurban di Masjid An-Nur</h2>
        <p>Transparan, Tepat Sasaran, dan Penuh Berkah</p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
        <div class="feature-card">
            <div class="feature-icon">🕌</div>
            <h4>Langganan Masjid</h4>
            <p style="font-size: 0.8rem; color: #666;">Qurban dilaksanakan di masjid dengan pengawasan DKM</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h4>Notifikasi Real-time</h4>
            <p style="font-size: 0.8rem; color: #666;">Update status via WhatsApp setelah pendaftaran</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h4>Tepat Sasaran</h4>
            <p style="font-size: 0.8rem; color: #666;">Daging disalurkan ke mustahik sekitar masjid</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4>Laporan Transparan</h4>
            <p style="font-size: 0.8rem; color: #666;">Laporan lengkap bisa diakses kapan saja</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ PETA PENYALURAN SEDERHANA ============
st.markdown("""
<div style="background: #e8f5e9; border-radius: 24px; padding: 1.5rem; margin: 1rem 0;">
    <div style="text-align: center;">
        <h3 style="color: #1a5a3a;">📍 Lokasi Penyaluran Qurban</h3>
        <p>Daging qurban akan disalurkan ke 3 titik di sekitar masjid</p>
    </div>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 1rem;">
        <div style="text-align: center;">
            <div style="font-size: 1.8rem;">🏘️</div>
            <strong>Panti Asuhan</strong>
            <p style="font-size: 0.7rem;">Yatim & Dhuafa</p>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.8rem;">🏠</div>
            <strong>Lingkungan Masjid</strong>
            <p style="font-size: 0.7rem;">Mustahik sekitar</p>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.8rem;">🏫</div>
            <strong>Pesantren</strong>
            <p style="font-size: 0.7rem;">Santri & Pengajar</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ TESTIMONI ============
st.markdown("""
<div style="margin: 2rem 0;">
    <div style="text-align: center;">
        <h2 style="color: #1a5a3a;">💬 Testimoni Jemaah</h2>
        <p>Apa kata mereka tentang qurban di Masjid An-Nur</p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div style="background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <p style="font-size: 0.9rem;">"Alhamdulillah, prosesnya mudah dan transparan. Dagingnya sampai ke tetangga saya yang membutuhkan."</p>
            <p style="font-weight: 600; margin-top: 0.5rem;">— Bapak Ahmad, Jemaah Masjid An-Nur</p>
        </div>
        <div style="background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <p style="font-size: 0.9rem;">"Senang bisa daftar online. Panitia juga sigap konfirmasi lewat WA."</p>
            <p style="font-weight: 600; margin-top: 0.5rem;">— Ibu Siti, Perumahan Asri</p>
        </div>
        <div style="background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <p style="font-size: 0.9rem;">"Qurban di masjid jadi lebih afdhal, ikut membangun kemakmuran masjid juga."</p>
            <p style="font-weight: 600; margin-top: 0.5rem;">— Ustadz Rudi, Pengajian Ahad Pagi</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class="footer">
    <h3>🕌 Masjid An-Nur</h3>
    <p>Jalan Kenangan No. 123, Kota Santri • Telepon: (021) 1234-5678</p>
    <p>Email: qurban@masjidannur.id | WhatsApp: 0812-3456-7890</p>
    <div class="divider" style="background: #ffd966; margin: 1rem 0;"></div>
    <p style="font-size: 0.7rem;">© 1447 H / 2026 M • Layanan Qurban Digital Masjid An-Nur</p>
</div>
""", unsafe_allow_html=True)

# ============ SIDEBAR (Data Admin & Statistik) ============
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2888/2888406.png", width=60)
    st.markdown("### 🕌 Masjid An-Nur")
    st.markdown("**Sistem Informasi Qurban Digital**")
    st.markdown("---")
    
    # Statistik cepat
    st.markdown("#### 📊 Statistik Qurban")
    total_hewan = sum(1 for h in HEWAN_KURBAN if h["stok"] > 0 and h["kategori"] != "Sedekah")
    st.metric("Jenis Hewan Tersedia", total_hewan)
    st.metric("Total Stok Hewan", total_stok)
    
    st.markdown("---")
    
    # Login Admin (opsional)
    with st.expander("🔐 Panel Admin"):
        admin_user = st.text_input("Username", placeholder="admin")
        admin_pass = st.text_input("Password", type="password", placeholder="admin123")
        if st.button("Login ke Dashboard", use_container_width=True):
            if admin_user == "admin" and admin_pass == "admin123":
                st.success("Login berhasil! Buka menu utama.")
                st.info("Fitur admin dapat diakses di menu utama aplikasi")
            else:
                st.error("Username atau password salah!")
    
    st.markdown("---")
    st.markdown("""
    <div style="background: #f0f7f0; padding: 0.8rem; border-radius: 12px;">
        <p style="font-size: 0.7rem; text-align: center; margin: 0;">
        📞 Info & Pendaftaran:<br>
        <strong>0812-3456-7890</strong><br>
        (08.00 - 16.00 WIB)
        </p>
    </div>
    """, unsafe_allow_html=True)
