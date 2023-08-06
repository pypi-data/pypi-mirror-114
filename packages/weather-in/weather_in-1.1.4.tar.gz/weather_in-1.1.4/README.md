# weather_in

## What is weather_in?

weather_in is a simple script for terminal use.  It utilizes the <a href = "https://openweathermap.org/current">Open Weather Map API</a> to provide quick, relevant and basic information regarding a specified locale's weather.

## System Requirements

* python3

## Installation

```pip install weather_in```

## Usage

To use weather_in:

### Basic / Current Day

```weather_in City State Country (country is optional; defaults to USA)```

(example: Pasadena California USA)

*note: State should not be abbreviated*

**Example Output**
the temp is: 85.19
low of: 63.68
high of: 105.73
few clouds

### Forecast / Next Five Days

```-f or --forecast```

**Example Output**
2021-08-01: high:84.34, low:82.76, clear sky
2021-08-02: high:84.87, low:82.81, clear sky
2021-08-03: high:85.48, low:83.34, clear sky
2021-08-04: high:84.72, low:83.91, clear sky
2021-08-05: high:84.4, low:83.62, clear sky
