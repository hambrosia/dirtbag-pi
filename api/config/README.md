# Configuration Options
* `db-config`: Should contain the entire database configuration string for psycopsg2. By default the database is named `dirtbag`, however you can specify another database name, user, and password. 
* `polling-interval-minutes`: Specifies the interval between each sensor read / write to the database. Increase this value to reduce the speed at which the database grows.
* `soil-moisture-<min/max>`: Calibrates the minimum and maximum soil moisture values to real-world minimum and maximum, e.g. exposure to air and submersion in water. This is used to calculate the soil moisture percent value.
* `template`: Specifies the Plotly template to use for styling the graph. Options include `'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none'`
