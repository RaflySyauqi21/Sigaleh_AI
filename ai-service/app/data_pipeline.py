import requests
import numpy as np
from datetime import datetime, timedelta


BASE_URL = "https://sigaleh-backend.vercel.app"


def fetch_commodities(wilayah, komoditas, start, end):
    url = f"{BASE_URL}/commodities"
    params = {
        "wilayah": wilayah,
        "komoditas": komoditas,
        "start": start,
        "end": end
    }

    res = requests.get(url, params=params)
    data = res.json()

    for item in data:
        item["Harga"] = float(item["Harga"])

    return data


def fetch_weather(wilayah, start, end):
    url = f"{BASE_URL}/weather"
    params = {
        "wilayah": wilayah,
        "start": start,
        "end": end
    }

    res = requests.get(url, params=params)
    return res.json()


def merge_data(commodities, weather):
    com_dict = {
        item["Tanggal"][:10]: item for item in commodities
    }

    wea_dict = {
        item["Tanggal"][:10]: item for item in weather
    }

    merged = []

    for date in sorted(com_dict.keys()):
        if date in wea_dict:
            merged.append({
                "tanggal": date,
                "harga": com_dict[date]["Harga"],
                "suhu": wea_dict[date]["Suhu_Rata2_C"],
                "hujan": wea_dict[date]["Curah_Hujan_mm"]
            })

    return merged


def build_model_input(merged_data, window_size=30):

    if len(merged_data) < window_size:
        raise ValueError("Data kurang dari 30 hari")

    data = []

    for i in range(7, len(merged_data)):
        harga = merged_data[i]["harga"]
        suhu = merged_data[i]["suhu"]
        hujan = merged_data[i]["hujan"]

        harga_kemarin = merged_data[i-1]["harga"]
        harga_minggu_lalu = merged_data[i-7]["harga"]

        row = [
            harga,
            suhu,
            hujan,
            harga_kemarin,
            harga_minggu_lalu
        ]

        data.append(row)

    return np.array(data[-window_size:])