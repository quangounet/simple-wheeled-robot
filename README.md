# simple-wheeled-robot

## Installing operating system images for Raspberry Pi
This section describes how to use [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to install **Raspberry Pi OS** for the Pi.
Prerequisite configurations to enable SSH on the Pi and connect it to the internect via wifi are included.

- Install **Raspberry Pi Imager** on your computer.
- Connect your SD card to the computer.
- Open Raspberry Pi Imager and choose **Raspberry Pi OS**.
- Choose the SD card you wish to write your image to.
- Review your selections and click 'WRITE' to begin writing data to the SD card.
- Navigate to the `boot` folder of the SD card
  - Creat an empty file named `ssh`.
  - If you want to access to the Pi via wifi and connect it to the internect, creat `wpa_supplicant.conf`, and paste the following into the file (modify `ssid` and `psk` accordingly)
  ```
    country=SG
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
    scan_ssid=1
    ssid="your_wifi_ssid"
    psk="your_wifi_password"
    }
    ```
- Insert the SD card to the Raspberry Pi

*The following has been tested to work on a Ubuntu 16.04 laptop. 
Need to test with Windows if the robot is to be controlled with the desktops in the lab.*

## Access the Raspberry Pi 
Raspberry Pi 4 has two micro HDMI ports and several USB ports, allowing you to access it with external monitor, keyboard and mouse.
The following section introduce two approaches to remote access to the Pi in *headless* mode: SSH and VNC.

Virtual Network Computing (VNC) allows you to remote access to the Pi's graphical interface, viewed in a window on another computer. 
To set up VNC, you need to SSH into the Pi and change some configurations first.

Default Username and Password for the Pi is:
- username: pi
- password: raspberry

### Access the Raspberry Pi with SSH
- Edit network connection if the Pi is connected to your computer via *Ethernet cable*:
  - Go to `Edit connections...`.
  - Navigate to `IPv4 Settings` tab. Select Method: `Shared to other computers`.
  - Save the connection.
- SSH the Pi
  - `ssh pi@raspberrypi.local` or `ssh pi@[ip-of-the-Pi]`
  - When prompt for password, enter `raspberry`
  - For first time connection, authenticity warning could appear.  Enter `yes` to continue.
- You are now logged in and working on the command line from the Pi `pi@raspberrypi: ~$`.

### Access the Raspberry Pi with VNC
- Enable VNC and change resolution on the Pi:
  - `sudo raspi-config`
  - Go to `Interfacing Options` - `VNC` - enable VNC.
  - Go to `Advanced Options` - `Resolution` - change the resolution to another option (otherwise the VNC Viewer cannot show the desktop).
- Download and install [VNC Viwer](https://www.realvnc.com/en/connect/download/viewer/linux/) on your computer.
- Check IP of the Pi (several approaches):
  - `ping raspberrypi.local` on your computer.
  - `ifconfig` on the Pi.
  - From your router page `192.168.1.1`.
- On your computer, run VNC Viewer and enter the IP address in the search bar.
- You are now able to view the Pi's graphical interface.

## Programming on the Raspberry Pi
Python2 and Python3 come with Raspberry Pi OS. 
Thonny Python IDE (a Python3 development environment) is also pre-installed and is very easy to use. 

