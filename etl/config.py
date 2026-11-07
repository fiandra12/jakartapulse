import os

LOCATIONS = {
    "Jakarta Pusat": (-6.1862, 106.8341),
    "Jakarta Utara": (-6.1384, 106.8629),
    "Jakarta Barat": (-6.1683, 106.7588),
    "Jakarta Selatan": (-6.2615, 106.8106),
    "Jakarta Timur": (-6.2250, 106.9004),
}


def db_params():
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "dbname": os.getenv("POSTGRES_DB", "jakartapulse"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
    }
