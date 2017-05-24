# Raspberry PI Temperature Sensor

Reads temperature from a DS18B20 temperature sensor every minute, store in sqlite database.

## Setup

Add to `config/boot.txt` and reboot.

```
dtoverlay=w1-gpio
```

![](https://github.com/cjolly/pi_temperature_sensor/blob/master/diagram.jpg)

## How to run
`python t.py`

