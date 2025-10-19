SELECT
    soil_type,
    region,
    fertilizer_type,
    irrigation_method,
    weather_condition,

AVG("soil_ph"::numeric) AS avg_soil_ph,
    AVG("nitrogen"::numeric) AS avg_nitrogen,
    AVG("phosphorus"::numeric) AS avg_phosphorus,
    AVG("potassium"::numeric) AS avg_potassium,
    AVG("moisture"::numeric) AS avg_moisture,
    AVG("temperature_celsius"::numeric) AS avg_temperature_celsius,
    AVG("rainfall_mm"::numeric) AS avg_rainfall_mm
FROM
    crop_dataset
GROUP BY
    soil_type,
    region,
    fertilizer_type,
    irrigation_method,
    weather_condition
ORDER BY
    region ASC,
    soil_type ASC,
    fertilizer_type ASC,
    irrigation_method ASC,
    weather_condition ASC;