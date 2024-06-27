All these labs make use of the Raspberry Pi 4 device, and a laptop for XAMPP.

# Lab 1 - [lab1 report](https://drive.google.com/file/d/1sdROprX0mL9JBaH1SvOBbSq_qHte7YP7/view?usp=sharing)
Raspberry Pi 4 setup. Simple hello world. Systemd on boot service, where waits for network to connect and then does an HTTP GET request for weather

# Lab 2 - [lab2 report](https://drive.google.com/file/d/1_uOUWwGd-EMFdpVDmhyMQN4rafyR_L4Z/view?usp=sharing)
Code to read 3 different sensors from the Raspberry Pi (each read in their respective demo.py file):
* SHT30 temperature and humidity sensor
* SEESAW soil temperature and humidity sensor
* ADC voltage reading, for wind sensor.

* sensor-polling.py: All three sensors polled

* concurrent-sensor-reading.py: All sensors read concurrently using asyncio 

* asyncio-extra-credit.py: All sensors read concurrently, where sensors read after getting a flag.

# Lab 3 (group project) Ad-Hoc Raspberry Pi Sensor network - [lab3 report](https://drive.google.com/file/d/1KNI8JMOvU63eRIEXWZDDM5CZKKzS2LRS/view?usp=sharing)
Three raspberry Pi's connected via ad-hoc, where data is sent. Data is then ploted.

**My contributions**: 
I setup/taught group-mates how to do the linux ad-hoc connections. Also created the sensor reading getter functions. Did pair programming, where assisted in debugging the project, mainly in regards to socket-programming and packet transmission/parsing. 

## Part 2 - Polling
Primary Pi sends a request to Secondary Pi for data. Secondary Pi sends back data. Primary Pi then alternate to other Secondary Pi. After polling both Pi's, creates a plot of data.
## Part 3 - Token Ring
Circular topology of three Pi's. 
Pi #1 (has the token first) sends data to Pi #2
Pi #2 aggregates its data and Pi #1 data, sends to Pi #3
Pi #3 aggregates its data and both Pi #1 & #2, then plots.
Repeat.

# Lab 4 (continuation of lab 3) WildFire reading/warning website - [lab4 report](https://drive.google.com/file/d/1GApGWuNkP6MsItSJ7ehjSOaLXeLpRvgl/view?usp=sharing)

Continuation of lab 3, but now with Wildfire warning detection and a front-end and back-end. For backend, MYSQL server that is ran via on XAMPP.

Front end, flask webserver for the front end also hosted via XAMPP HTTP server.

Wildfire warning and thresholds added, where the warning is sent via an HTTP packet.

**My contributions:**
Pair programming, troubleshooted getting the SQL server commands to work via Python. Added front-end wildfire color/warnings, along with other HTML front-end edits after website has been created. Modified the code to work with my partner's file-data-reader class, where instead of polling data, we read example pre-written data. Also created an overall wildfire percent page for part 4.

## Part 2-3 Reading sensors on website
Lab 3, but with data readings & plots being stored on a SQL server and read on webite

## Part 4 Wild Fire
Part 2-3, but with wildfire aspect of the lab (eg. warnings, color-coding) implemented.



