# Bike Sharing Dataset Analysis & Streamlit Dashboard

## Deskripsi Singkat
Proyek ini berisi analisis **Bike Sharing Dataset** untuk memahami pola penyewaan sepeda berdasarkan:
- faktor waktu (jam puncak, workingday vs non-workingday),
- kondisi cuaca,
- musim.

Hasil analisis dibuat dalam bentuk:
1) **Notebook Jupyter**: `ML_Muhammad_Hafidz_Hazimulfikri.ipynb`  
2) **Dashboard Streamlit**: `app.py`

## Dataset yang Digunakan
Dataset yang dipakai:
- `day.csv` → data penyewaan sepeda per hari  
- `hour.csv` → data penyewaan sepeda per jam  

Target utama:
- `cnt` = total rental (gabungan `casual` + `registered`)

## Cara Menjalankan Proyek (Local)

### 1) Install library (wajib)
Masuk ke folder project, lalu jalankan:
```bash
pip install -r requirements.txt
```
2) Menjalankan Notebook
Jalankan Jupyter:
jupyter notebook
Buka file notebook:
ML_Muhammad_Hafidz_Hazimulfikri.ipynb
Lalu run cell dari atas sampai bawah.

3) Menjalankan Dashboard (Streamlit)
Pastikan file ini berada dalam folder yang sama:
app.py
day.csv
hour.csv
requirements.txt
Jalankan:
streamlit run app.py
Jika streamlit tidak terbaca, coba:
python -m streamlit run app.py

## Ringkasan Insight
- Jam puncak rental cenderung terjadi pada jam commuting (pagi dan sore). Pola puncak lebih jelas pada workingday.
- Pada non-workingday/libur, pola penyewaan lebih menyebar dan cenderung naik pada siang–sore (lebih banyak dipakai untuk aktivitas santai/rekreasi).
- Cuaca memengaruhi demand: kondisi cerah menghasilkan rental lebih tinggi, sedangkan cuaca buruk menurunkan jumlah penyewaan.
- Musim juga berpengaruh, sehingga demand naik-turun sepanjang tahun dan bisa jadi pertimbangan untuk strategi operasional/promo.
