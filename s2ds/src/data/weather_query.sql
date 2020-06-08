SELECT dt_iso, temp, feels_like, humidity, wind_speed, wind_deg, rain_1h, rain_3h, snow_1h,snow_3h, clouds_all, weather_main, weather_icon
from weather_history
WHERE dt_iso >= '2018-01-01'
ORDER BY dt_iso
