# Configuration Options

## Settings in config.json

* `polling-interval-minutes`: Specifies the interval between each sensor read / write to the database. Increase this value to reduce the speed at which the database grows.
* `soil-moisture-<min/max>`: Calibrates the minimum and maximum soil moisture values to real-world minimum and maximum, e.g. exposure to air and submersion in water. This is used to calculate the soil moisture percent value.
* `template`: Specifies the Plotly template to use for styling the graph. Options include `'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none'`

## Secrets in secret.json
Configuration settings in secret.json are ignored by Git. Nonetheless, exercise caution and carefully review your commits to ensure no secrets are published to your version control platform.

* `db-config`: Should contain the entire database configuration string for psycopsg2. By default the database is named `dirtbag`, however you can specify another database name, user, and password. 
* `email-sender-address`: The address of the email account used to send notifications. It is recommended not to use a personal address. Instead, create a service account for use as a notification sender.
* `email-sender-password`: The password of the email account used to send notifications. Use a strong password with 16 or more characters. For this implementation two-factor authentication should be disabled.
* `email-sender-host`: The SMTP host address of the email account used to send notifications.
* `email-sender-port`: The port for the SMTP host of the email account used to send notifications.
