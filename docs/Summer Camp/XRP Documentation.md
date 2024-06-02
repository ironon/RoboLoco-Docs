General Info

PestoLink driving

* If the robot version is < 1.21, update is necessary ([Link](https://www.google.com/url?q=https://micropython.org/download/RPI_PICO_W/&sa=D&source=editors&ust=1717314600661248&usg=AOvVaw1N38hAzfpG8dCsN3mldzHg) to download recent micropython versions). Hold down the BOOTSEL button (white with a label next to it), before plugging in the USB to the computer. This should turn it into USB mass storage device mode and it should provide a flash drive in file explorer. Download the version URF file from the link, and put it onto the top level of the flash drive. This should update the robot after some time/reset.
* [Setup Info:](https://www.google.com/url?q=https://experientialrobotics.org/drive-an-xrp-robot-with-pestolink/&sa=D&source=editors&ust=1717314600661696&usg=AOvVaw2AZFfiYMfIx1UF9z2KGjQ5) Download repository from link which should contain two python files: pestolink.py, pestolink\_example.py. BOTH FILES ARE NECESSARY. Upload pestolink\_example to top level, pestolink.py to /lib/.
* Once you download the repository and upload them, make sure to press “run” in the top right corner of the screen. This will allow the robot to have bluetooth capabilities.
* Go to [pestol.ink](https://www.google.com/url?q=https://pestol.ink/&sa=D&source=editors&ust=1717314600662035&usg=AOvVaw1-5dNjCtit7A53EUQ7KWqw) on a computer or mobile device. If on a computer, turn on the WASD keys setting (WASD runs more accurately than joystick/controller). Then, press connect and connect to the robot via bluetooth (the robot's name is XRPRobot). On a mobile device, the left joystick will drive the robot, and on the computer, the WASD keys will drive the robot. The buttons on the right will control the motors on the robot

WPILib Java

* If one motor is faster, change the leftspeed or rightspeed as needed. They are located in DriveTrain.java line 61-63
* To switch between tank drive and arcade drive, change setdefaultcommand (in robotcontainer) to whatever you need (getArcadeDriveCommand or getTankDriveCommand)

XRP Editor App

* The XRP Editor app was customly modified by Kavin Muralikrishnan and Aneesh Sule to allow for Pesto Link support.
* Additions:
* Saving files works. The error was that the code referred to a file called state.json, which was in the .gitignore, meaning that it didn’t get ported over to the base repository. state.json was a one line dictionary that just contained the directory in which xrp code would be stored.
* The fix was adding some code to create state.json if it didn’t already exist
* Pesto Link support
* A new Controller section of blocks was added with values for

Line Follower Code 

* Note: Hardware issues. Turning 90 degrees turns it more like 85 or 95, and going straight still has drift.
* ![](https://lh7-us.googleusercontent.com/9GQN9FPEE3BV8WgixcKe7Nn-FPaDDEfqr8OHg1RfPdvTjH0vYJeWlBJRdrYG2ecuiEVn-XnLY3-bBxlwrz8PfrC6YdIVQvteJNqOoNwSFxSmwbk_cbQ_YBERkP4V9CMfsWz-Sls4ESJmht-fceJnf3E)
