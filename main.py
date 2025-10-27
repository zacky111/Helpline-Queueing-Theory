from source.generate_input import generate_call_data as generate_input
from source.queue_sim import simulate_queues

import numpy as np
import matplotlib.pyplot as plt

#====================================================================================================
## parametrization - queues
num_queues = 5
queue_capacity = 10

## parametrization - simulation
hours = 24
calls_per_hour_day = 10
calls_per_hour_night = 3
min_service = 5
max_service = 20
#====================================================================================================
# Simulation

df_calls = generate_input(hours=hours)
stats = simulate_queues(df_calls, num_queues, queue_capacity)

#====================================================================================================
## Prepare data for plots
timeline = stats['timeline']
occupancy = np.array(stats['occupancy'])
num_queues = occupancy.shape[1]

# Przybliżone czasy odrzuconych zgłoszeń
df_calls['accepted'] = stats['accepted_flags']
rejected_times = df_calls.loc[~df_calls['accepted'], 'arrival_time'].tolist()

# occupancy array dla heatmapy
occupancy_array = np.array(stats['occupancy'])

# ===== 2x2 subplots =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ===== Wykres 1: Zajętość kolejek =====
for i in range(num_queues):
    axes[0, 0].plot(timeline, occupancy[:, i], label=f'Kolejka {i+1}')
axes[0, 0].set_ylabel("Liczba zajętych miejsc")
axes[0, 0].set_title("Zajętość kolejek w czasie")
axes[0, 0].legend()
axes[0, 0].grid(True)

# ===== Wykres 2: Histogram odrzuconych zgłoszeń =====
axes[0, 1].hist(rejected_times, bins=24, color='red', alpha=0.6)
axes[0, 1].set_xlabel("Czas (godziny)")
axes[0, 1].set_ylabel("Liczba odrzuconych zgłoszeń")
axes[0, 1].set_title("Odrzucone zgłoszenia w ciągu dnia")
axes[0, 1].grid(True)

# ===== Wykres 3: Kołowe dla całości, dnia i nocy =====
calls_day = df_calls[(df_calls['arrival_time'] % 24 >= 8) & (df_calls['arrival_time'] % 24 < 20)]
calls_night = df_calls[(df_calls['arrival_time'] % 24 < 8) | (df_calls['arrival_time'] % 24 >= 20)]

accepted_day = calls_day['accepted'].sum()
accepted_night = calls_night['accepted'].sum()
rejected_day = len(calls_day) - accepted_day
rejected_night = len(calls_night) - accepted_night

pie_data = [
    (stats['accepted_calls'], stats['rejected_calls'], "Całość"),
    (accepted_day, rejected_day, "Dzień"),
    (accepted_night, rejected_night, "Noc")
]

ax = axes[1, 0]
ax.axis('equal')  # zachowanie proporcji koła

for i, (accepted, rejected, title) in enumerate(pie_data):
    ax_pie = ax.inset_axes([0.05 + i*0.32, 0.1, 0.3, 0.8])
    ax_pie.pie([accepted, rejected], labels=None,
               colors=['#4CAF50', '#F44336'], autopct='%1.1f%%', startangle=90)
    ax_pie.set_title(title)

# wspólna legenda pod wszystkimi kołami
handles = [plt.Line2D([0], [0], color='#4CAF50', lw=4),
           plt.Line2D([0], [0], color='#F44336', lw=4)]
labels = ['Przyjęte', 'Odrzucone']
ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

ax.set_axis_off()

# ===== Wykres 4: Heatmapa obciążenia kolejek w czasie (oś X = czas) =====
im = axes[1, 1].imshow(
    occupancy_array.T,
    aspect='auto',
    cmap='viridis',
    origin='lower',
    extent=[timeline[0], timeline[-1], 0.5, num_queues + 0.5]
)
axes[1, 1].set_xlabel("Czas (godziny)")
axes[1, 1].set_ylabel("Kolejka")
axes[1, 1].set_title("Heatmapa obciążenia kolejek w czasie")
axes[1, 1].set_yticks(ticks=np.arange(1, num_queues + 1))
axes[1, 1].set_yticklabels([f'Kolejka {i+1}' for i in range(num_queues)])
fig.colorbar(im, ax=axes[1, 1], orientation='vertical', label='Liczba zajętych miejsc')

plt.tight_layout()
plt.show()
