# IOT-Project

The system: 
- Tower Pro Servo connects with Raspberry Pi and is programmed with Python.
- DHTT22 Digital Temperature Sensor connects to Raspberry Pi with one wire to send temperature data to a terminal and display gauge.
- Red and green LED bulbs connect to Raspberry Pi to indicate high and low temperatures.
- Motor Driver IC connects between Pi and DC Motor for fan control.
- Fan speed automatically adjusts based on temperature changes.
- Fan turns off if temperature drops below 20 degrees Celsius.
- Display gauge shows three different temperature levels (High, Medium, Low).
- MQTT protocol used for message transport between Pi and dashboard.
- Node-Red dashboard displays latest temperature, past data visualization, and temperature prediction
