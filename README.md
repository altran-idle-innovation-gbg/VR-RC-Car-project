# VR-RC-Car-project
RASPBERRY PI- ANDROID, MOUSE, KEYBOARD & BLUETOOTH-CONTROLLED RC-CAR WITH VR-GLASSES LIVE VIDEO STREAMING

## Differences between versions :memo:

<table width="600px">
  <tr>
    <td align="center">VR RC Car :red_car:</td>
    <td align="center"><b>V1</b></td>
    <td align="center"><b>V2</b></td>
    <td align="center"><b>V3</b></td>
  </tr>
  <tr>
    <td><b>COMMUNICATION</b></td>    
    <td>RPi + computer mouse</td>    
    <td>RPi + keyboard</td>    
    <td>Bluetooth</td>  
  </tr>
  <tr>
    <td><b>CONTROL INTERFACE</b></td>            
    <td>Computer Mouse movement (+left, right & middle click)</td>            
    <td>Keyboard buttons (W,A,S & D + Q,R & E + SPACE)</td>            
    <td>Bluetooth Remote Controller</td>      
  </tr>
  <tr>
    <td><b>SERVO / CAMERA MOVEMENT</b></td>                
    <td>Yes</td>                
    <td>Yes</td>
    <td>No</td>
  </tr>
  <tr>
    <td><b>CAMERAS / VR-GLASSES</b></td>                
    <td>Yes</td>                
    <td>Yes</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td><b>WORKING?</b></td>
    <td>Yes</td>
    <td>Yes</td>
    <td>No</td>
  </tr>
  <tr>
    <td><b>ISSUES</b></td>
    <td>Servo motor rotates more than 180°</td>
    <td>Servo motor rotates more than 180°</td>
    <td>Remote Controller's GameMode does not work - which is needed to control the car</td>
  </tr>
</table

## **:mag_right: How to**
> _Cameras - VR Glasses_

:exclamation: Be sure you are connected to the same network on the phone and RPi. :exclamation:
- Open two Chrome windows on the phone and enter the RPi’s IP addresses in each of them.
- Find the IP address by opening the terminal and write "ifconfig" and press enter.
- Add port: 8080 after the IP, should look something like: http://10.46.2.108:8080
  - You will now come to a site called UV4L, click the "Web RTC"-icon.
  - Choose video-resolution and FPS and then press the green **_Call_**-button
