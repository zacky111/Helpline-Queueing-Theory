import numpy as np
import pandas as pd

def generate_call_data(hours=24, calls_per_hour_day=10, calls_per_hour_night=3, min_service=5, max_service=20):
    """
    Generuje dane zgłoszeń do symulacji kolejki infolinii.
    
    Parametry:
    - hours: liczba godzin do symulacji
    - calls_per_hour_day: średnia liczba połączeń w godzinach dziennych (np. 8:00-20:00)
    - calls_per_hour_night: średnia liczba połączeń w godzinach nocnych
    - min_service, max_service: minimalny i maksymalny czas obsługi klienta w minutach
    """
    data = []
    
    for hour in range(hours):
        # Ustalamy intensywność w zależności od pory dnia
        if 8 <= hour % 24 < 20:  # dzień
            num_calls = np.random.poisson(calls_per_hour_day)
        else:  # noc
            num_calls = np.random.poisson(calls_per_hour_night)
        
        for _ in range(num_calls):
            service_time = np.random.randint(min_service, max_service + 1)
            arrival_time = hour + np.random.random()  # dokładny moment w godzinie
            data.append({
                'arrival_time': round(arrival_time, 2), 
                'service_time': service_time
            })
    
    return pd.DataFrame(data)

