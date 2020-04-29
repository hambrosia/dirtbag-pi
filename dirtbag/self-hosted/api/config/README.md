# Configuration Options

## Settings in config.json
* `enable-email-notifications`: Boolean that enables or disables email alerting. Off by default. Make sure to supply valid SMTP configs in `secret.json` if enabled.
* `polling-interval-minutes`: Specifies the interval between each sensor read / write to the database. Increase this value to reduce the speed at which the database grows.
* `soil-moisture-<min/max>`: Calibrates the minimum and maximum soil moisture values to real-world minimum and maximum, e.g. exposure to air and submersion in water. This is used to calculate the soil moisture percent value.
*`soil-moisture-alert-<low/high>: Integer values between 0-100 to set the lower and upper bounds used for threshold e-mail alerting. If soil moisture falls outside the range, an e-mail will be sent. Otherwise, no action is taken.
* `soil-moisture-alert-time": ISO formatted time. PM notifications take 24hr / military format, e.g. `17:30:00`. DirtBag Pi will check daily at this time to see if the soil moisture reading is within bounds.
* `template`: Specifies the Plotly template to use for styling the graph. Options include `'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none'`

## Secrets in secret.json
Make sure to copy the secrets template to a usable file, e.g. `cp secret-template.json secret.json`. Configuration settings in `secret.json` are ignored by Git. Nonetheless, exercise caution and carefully review your commits to ensure no secrets are published to your version control platform.

* `db-config`: Should contain the entire database configuration string for psycopsg2. By default the database is named `dirtbag`, however you can specify another database name, user, and password. 
* `email-sender-address`: The address of the email account used to send notifications. It is recommended not to use a personal address. Instead, create a service account for use as a notification sender.
* `email-sender-password`: The password of the email account used to send notifications. Use a strong password with 16 or more characters. For this implementation two-factor authentication should be disabled.
* `email-sender-host`: The SMTP host address of the email account used to send notifications.
* `email-sender-port`: The port for the SMTP host of the email account used to send notifications.
