# JakartaPulse: Urban Air Quality & Weather Data Pipeline

End-to-end ETL pipeline yang mengambil data kualitas udara dan cuaca per jam untuk 5 wilayah Jakarta, memodelkannya dalam layer raw/staging/mart di PostgreSQL, dan menampilkannya di dashboard Metabase. Dijalankan otomatis oleh Jenkins.

## Business Problem
Tim analis kota membutuhkan data kualitas udara dan cuaca Jakarta yang terpusat, bersih, dan ter-update tiap jam untuk memantau tren polusi.

## Arsitektur
```
Open-Meteo API -> Python ETL -> PostgreSQL (raw -> staging -> mart) -> Metabase
                      ^
        Jenkins (CI/CD + cron tiap jam) <- GitHub
```

## Tech Stack
| Komponen | Tools |
|---|---|
| Extract | Python (requests) |
| Load | PostgreSQL 16 (psycopg2, UPSERT) |
| Transform | SQL (view staging, tabel mart) |
| Orkestrasi dan CI/CD | Jenkins (Jenkinsfile, cron) |
| Data quality | pytest + 6 SQL check |
| Visualisasi | Metabase |
| Deployment | Docker Compose, dimonitor lewat Portainer |

## Data Model
- `raw.air_quality`, `raw.weather`: data mentah apa adanya, plus `ingested_at`
- `staging.stg_hourly`: join udara + cuaca, dengan kategori AQI
- `mart.daily_air_quality`: agregat harian per wilayah
- `mart.hourly_air_quality`: view per jam untuk dashboard

## Fitur Utama
- **Idempotent**: UPSERT `ON CONFLICT`. Menjalankan ETL dua kali tidak menggandakan data (terbukti: 3720 baris tetap 3720).
- **Retry dengan backoff** saat API gagal.
- **6 data quality checks**: tabel tidak kosong, rentang PM2.5 wajar, rasio null, freshness data, tanpa duplikat di mart, kelima wilayah lengkap.
- **CI/CD**: tiap commit menjalankan build, lint (flake8), unit test (pytest), deploy, dan smoke run.
- **Jadwal tiap jam** lewat job Jenkins terpisah.
- **Secret** disimpan di Jenkins Credentials, bukan di repo.

## Cara Menjalankan
```bash
git clone https://github.com/fiandra12/jakartapulse.git
cd jakartapulse
cp .env.example .env        # isi password
docker compose up -d --build postgres metabase
docker compose --profile etl run --rm -e PAST_DAYS=30 etl-runner
```
Metabase: http://localhost:3000

## Dashboard
![Dashboard](docs/dashboard.png)

## CI/CD
![Jenkins CI/CD](docs/jenkins-cicd.png)
![Jenkins hourly](docs/jenkins-hourly.png)

## Deployment
![Portainer](docs/portainer.png)

## Keputusan Teknis dan Trade-off
- **Layer raw/staging/mart**: data mentah tetap utuh sehingga transformasi bisa diulang tanpa memanggil API lagi.
- **UPSERT, bukan append**: Open-Meteo bisa merevisi data jam terakhir, dan pipeline harus aman dijalankan ulang.
- **Mart di-rebuild penuh (TRUNCATE + INSERT)**: volume kecil sehingga sederhana dan benar. Di skala besar diganti incremental model.
- **Postgres hanya listen di 127.0.0.1**: tidak terekspos ke luar server.

## Roadmap
- Migrasi transformasi ke dbt
- Oracle XE sebagai warehouse kedua
- Notifikasi kegagalan via Telegram
- Sumber data tambahan (BMKG)
