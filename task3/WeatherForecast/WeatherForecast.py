
import matplotlib.pyplot as plt
import pandas as pd

WINDOW_WIDTH = 13
WINDOW_HEIGHT = 5
AVERAGE_STEP = 3

data = pd.read_csv("GlobalWeatherRepository.csv")

ua_list = []
i = 0
while i < data.shape[0]:
   if data.iloc[i]['country'] == "Ukraine":
       ua_list.append(data.iloc[i])
   i = i + 1

ua = pd.DataFrame(ua_list)

ua['last_updated'] = pd.to_datetime(ua['last_updated'])

plt.rcParams['figure.figsize'] = (WINDOW_WIDTH, WINDOW_HEIGHT)

def draw():
    plt.legend()
    plt.grid()
    plt.show()

plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_Carbon_Monoxide'][::AVERAGE_STEP], label='Carbon_Monoxide (4000ug/m3)')
plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_Ozone'][::AVERAGE_STEP], label='Ozone (300ug/m3)')
draw()

plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_Nitrogen_dioxide'][::AVERAGE_STEP], label='Nitrogen_dioxide (25ug/m3)')
plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_Sulphur_dioxide'][::AVERAGE_STEP], label='Sulphur_dioxide (40ug/m3)')
draw()

plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_PM2.5'][::AVERAGE_STEP], label='PM2.5 (15ug/m3)')
plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_PM10'][::AVERAGE_STEP], label='PM10 (45ug/m3)')
draw()

plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_us-epa-index'][::AVERAGE_STEP], label='air_quality_us-epa-index (3)')
plt.plot(ua['last_updated'][::AVERAGE_STEP], ua['air_quality_gb-defra-index'][::AVERAGE_STEP], label='air_quality_gb-defra-index (7)')
draw()

ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
ax3 = plt.subplot(2, 1, 2)
ax1.plot(ua['last_updated'][::AVERAGE_STEP], ua['temperature_celsius'][::AVERAGE_STEP], label='temperature_celsius')
ax2.plot(ua['last_updated'][::AVERAGE_STEP], ua['wind_kph'][::AVERAGE_STEP], label='wind_kph')
ax3.plot(ua['last_updated'][::AVERAGE_STEP], ua['precip_mm'][::AVERAGE_STEP], label='precip_mm')
ax1.legend()
ax2.legend()
ax3.legend()
plt.show()




