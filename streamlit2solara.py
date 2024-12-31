import folium
import ee
import random
import numpy as np
import os
import leafmap.foliumap as leafmap
import requests
import datetime
import pickle
import pandas as pd
import plotly.express as px
import time
import json
from folium.plugins import Draw
import solara
from datetime import datetime
from datetime import date

ee.Authenticate()
ee.Initialize(project='vegetation-2023-408901')

def load_model(path):
    with open (path, 'rb') as loaded_model:
        model = pickle.load(loaded_model)
    return model

def get_steps(steps):
    benchmark_year = 2023
    today = str(date.today())
    year = today.split('-')[0]
    month = today.split('-')[1]
    gap = int(year) - benchmark_year
    gap_month = gap * 12 + int(month)
    total_steps = gap_month + steps
    return total_steps

def generate_timestamps(num_steps):
    months = 12
    year = 2023
    month_ = 1

    dates = []

    for num in range(num_steps):
        year_change = num // 12
        year_ = year + year_change

        if num % 12 == 0:
            month_ = 1

        date = f"{year_}-{month_}-01"
        dates.append(date)

        month_ += 1
    return dates

def predict(model, num_steps):
    prediction = model.forecast(num_steps)
    timestamp = generate_timestamps(num_steps)
    data_dict = {
        'predictions': list(prediction.values),
        'timesteps': timestamp,
    }
    
    df = pd.DataFrame(data_dict)
    fig = px.line(df, x="timesteps", y=df.columns[0:2], title='Predicted Mean NDVI Trend', width=1000, height=700)
    return fig

@solara.component
def NDVIDisplayer():
    solara.Title("NDVI Displayer")

    SA_CENTER = [39.204260, -120.755200]
    SJ_CENTER = [36.824278, -118.910522]

    valleys = ['Sacramento', 'San Joaquin']
    model = None
    sa_model = load_model('sa_model')
    sj_model = load_model("sj_model")

    solara.Markdown("Select which valley your field is in:")

    valley_select = solara.Select("Select a valley", options=valleys, value="Sacramento")

    start_date_input = solara.DatePicker("Start date", value=date.today())
    end_date_input = solara.DatePicker("End date", value=date.today())

    if valley_select == 'Sacramento':
        model = sa_model
        loc = SA_CENTER  # recenters the map to SA valley
    else:
        model = sj_model
        loc = SJ_CENTER  # recenters the map to SJ Valley

    m = folium.Map(location=loc, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', zoom_start=9)
    Draw(export=False).add_to(m)

    solara.FoliumMap(m)

solara.App(NDVIDisplayer)