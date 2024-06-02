ACL RoboLoCo 5338 

2024 Technical Binder



---

![](https://lh7-us.googleusercontent.com/BRHet9gzDVcw-bAkT1QXY76vXcYU0-KrqIXX_NLPhhDmkpf4MnOVK7GYLdV0CoBWXEgAGZIyf5mLLzyiP3RzOe51fdbotYoZooO3k7P2yOMbjYtmqyzYKcBvC_P-Hj2C98zEFyr0L5qjQ9ho3m2Pvgo)

---



Foreword
========



---

The 2024 RoboLoCo Technical Binder details all necessary information about our robot, including its many sub-assemblies and their functions, the software utilized in its operation, and the strategy our team employs in the 2024 FRC game, Crescendo.

Our team has taken every detail into account through the journey of building our robot. We have analyzed the game and constructed a machine capable of accomplishing the most with the simplest design possible, and our software team’s efficient programming and precise electrical wiring make our intentions a reality. 

It is the honor of RoboLoCo, FRC team 5338, to present our robot for the 2024 Crescendo season: Rock’n’Rivets.



---

![](https://lh7-us.googleusercontent.com/o9eT9R-56DvwZ16nrJ92LgazWa4UDVBUlpygPBx5DZLWkkKP8di8Y2eH4FlMwXYgQi1Drz6Q44pPa-_wLI5gNyyh1mTbZ58l8pl2RQ65PhPTmKqUuNeWa0sBKzeMv4KEkqRs-rcF6xZeWIuD-HqZJ6I)

Table of Contents
=================



---

[Foreword](#h.jmv1pxel40kq)[2](#h.jmv1pxel40kq)

[Table of Contents](#h.k36679fmztd)[3](#h.k36679fmztd)

[Strategy Analysis](#h.1suuk7d6u880)[4](#h.1suuk7d6u880)

[Robot Overview](#h.qdhsfm51db2n)[5](#h.qdhsfm51db2n)

[Drivetrain](#h.usgqcvpaks0)[6](#h.usgqcvpaks0)

[Arm](#h.6fx3ufnmx9q)[7](#h.6fx3ufnmx9q)

[Shooter](#h.wje90fc2e3mx)[8](#h.wje90fc2e3mx)

[Intake](#h.bwuhbqiztymd)[9](#h.bwuhbqiztymd)

[Autonomous](#h.6cftuook279w)[10](#h.6cftuook279w)

[Tele-Op](#h.x38jkxq870v7)[11](#h.x38jkxq870v7)



---

Strategy Analysis
=================



---

Robot Design

* Overall goal was simplicity, robustness, and efficiency
* Aimed to intake from the ground, score into the amp and speaker, and climb
* Did not target trap due to added complexity and source intake due to minimal benefit as it required extra alignment
* Centralize all scoring into one mechanism to allow for maximized build time and improvements with simpler controls
* Low profile for stability and maneuverability underneath the chain
* Constrain all mechanisms within the robot bumpers, as the field involves several obstacles and congested zones
* Allows for faster cycles and less worry about robot damage/penalties
* Remain modular, with the ability to quickly remove and replace parts in case of improvements or damage

Scouting and Alliance Selection

* Created a scouting app to determine which robots would best pair with Rock’n’Rivets and our alliance partner via data collection
* Coded using Dart and applied using the Google Flutter framework, allowing the app to be run on Windows, Android, and MacOS
* The app has both match and pit scouting functionality to account for robot performance and robot design
* Compile data to detect trends through spreadsheets, using statistical tests and other Excel methods to mathematically analyze how each robot’s performance

Robot Overview
==============



---

![](https://lh7-us.googleusercontent.com/9Wmi4OLdE6YFp8Ekz2EamI6sNNqjIAyw9ld760nTWRlPodLIX_AIoVUud5hrwg7Lh0Q8vAKfW-FjRRb28HehdIp2Fu4goPq86EhpogYZmSXzdz0aGFM_GSAeWFvxDbDTU_wVPCpBC4BkZLWOL-jCyg4)



---

Physical Properties:

Frame Dimensions: 31.1” x 26.3”

Frame Perimeter: 114.8”  
Weight (- Bumpers): ~95 lbs  
Weight (+ Bumpers): ~110 lbs



---

Scoring:

Speaker & Amp - Variable Angle Shooter

Ground Intake - Under the Bumper  
Chain Climb - Using Arm

---



Drivetrain ――――――――――――――――――
-----------------------------

The chassis allows for swift and aggressive movement around the field, a benefit of our new swerve drivetrain.

REV MAXSwerve Modules

* 3” MAXSwerve Wheels 2.0
* 4.8 m/s free speed
* REV NEO 1.1s for drive, REV NEO 550s for steer
* 3D printed Swerve Covers that also support polycarbonate skirts and Intake Wings

Polycarbonate Skirts

* Lightweight sheets of polycarbonate surrounding the underside of the chassis preventing unwanted note clogging

Bumpers

* L brackets inserted into thick aluminum plates fixed in place with quick release pins
* Quick and tool-less bumper changes while maintaining stability and durability

Electronics/Control

* Polycarbonate Bellypan/Electronics Board
* RoboRIO 2.0
* Custom CAN PCB (star topology)
* Elevated REV Power Distribution Hub
* Pigeon 2.0 IMU

---

Arm ―――――――――――――――――――――
-------------------------

  


The arm allows for scoring into the amp and the speaker with its variable angle capability. Additionally, the integrated chain climb hooks allow for climb and ensemble points.

Chain Tensioners

* Allows for quick adjustment of chain tension without a turnbuckle by turning just two Cams
* Increases range of motion and allows for even tension in both chains

Hard Stop

* 3D Printed out of TPU to prevents damage to the arm
* Positioned to score in speaker when against subwoofer

Chain Climb Hook

* Fabricated on a waterjet out of ⅛” aluminum
* Allows for climb by catching on the chain when the arm closes
* Reduces climb time and weight by eliminating the need for a separate climb mechanism

Variable Angle

* Two REV motors physically mated with a shaft, each with a 60:1 gearbox.
* When the chain is factored in (60:18), the gear ratio is increased to 200:1, allowing for fast and powerful arm movement
* Can rotate until it fires downward, allowing for amp scoring

Electronics/Control

* Limelight 2.0 to allow for robot vision

Shooter ―――――――――――――――――――
---------------------------

![](https://lh7-us.googleusercontent.com/U6cBo-XeD3XukUFC91NFThy3cPyZqZC-ozX9mjMxsuAS9kQrIDF-LQGncSBymPPaLgdX9ejo1P4rbJVfi2JhAR2PpR2jBnuq5PPOXOAOjtZMevszb1-B47gIT-qM36PX6VofO_eCACfagZPZv_bmaOw)

The shooter allows for notes to be scored into both the speaker and amp. Utilizing a combination of powered and free-spinning axles, the shooter was designed to maximize accuracy and power.

Shooting Mechanism

* Two axles, each powered by a 4:3 gear ratio REV NEO 1.1, use orange stealth wheels to shoot notes

Indexer

* Uses silicone coated rollers powered by a single 1:1 REV NEO 1.1 to hold notes when not scoring and feed them into the shooter
* Two live rollers, connected with belt and gears, and two freely spinning rollers
* Freely spinning rollers prevent note damage and allow notes to accelerate faster

Electronics/Control

* Grapple Robotics LaserCAN detects if a note is present, allowing for consistent intake cycles during autonomous



---

![](https://lh7-us.googleusercontent.com/0JAVx_asmNFsPmQHxke5H6ix0jz8W4tjxm7rIgkFdOmAn8c-m15nrleHvBI1z4s3rlzj2xTd4BxobzURJy6pGpja5MJMaejU5ioxhhJb64yBkfMNybOZGhj6eZKIGb9L-JXfEFGpuqXHVX-mspyGt-U)

Intake ――――――――――――――――――――
---------------------------

The Outside-Inside intake sits outside the chassis, but inside the bumpers. It allows for efficient under-the-bumper note pickup from the ground while ensuring safety from collisions at all times.

Under the Bumper

* Allows for intake of notes on the move while bumpers prevent physical damage
* 4:1 gear ratio REV NEO 1.1 powering 3 dead axles using belt and gears to suck the note into the indexer
* Silicone tubing around polycarbonate rollers for high grip

“Wings”

* 3D printed mounting brackets with a polycarbonate sheet
* Funnels the note into the indexer, allowing for intaking to occur at any position along the front of the robot.

“Boomerang” Bracket

* Added after the intake was broken during Week 3 Competition
* Large ¼” aluminum boomerang-esque bracket fabricated on a waterjet, designed to transfer impact energy into the more rigid chassis

Electronics/Control

* Logitech camera provides live feed to driver station for note pickup

Autonomous ―――――――――――――――――
----------------------------

The robot follows pre-programmed paths using input from odometry to intake and shoot notes.

Vision & Pathfinding

* Uses feedback from encoders and gyroscope input to know the robot’s position on the field
* LaserCAN mounted on the indexer informs the robot whether a note is fully inside the robot or if the rollers need to be spun more

Driving

* Uses PathPlanner, which allows for trajectories to automatically be created given the proper values
* PathPlanner generates trajectories as bezier curves, then motors are controlled using PID
* Several unique autonomous paths were created for different starting positions, which can be picked from the dashboard



---

[[a]](#cmnt1)[[b]](#cmnt2)Tele-Op ―――――――――――――――――――
---------------------------

Each sub-system has its own class that contains several commands for that sub-system, with a class to map controller inputs to method calls. Both driver and operator use xbox series X controllers as their preferred method of input.

Mechanism Controls

* Amp scoring, climb, and distance shooting(from the stage) have a pre-set position on the motor to reduce cycle time
* Soft stop on arm motors prevent the arm from exceeding 1 ft past frame perimeter
* One button simultaneously controls shooter, indexer, and intake motors to accurately shoot notes
* Camera gives live feed of the intake, allowing the operator to know where the note is relative to the intake

Driving

* Field Centric Swerve
* Left joystick controls the robot movement and the right joystick controls the orientation of the robot
* Slow mode can be toggled on/off by the drive to give more precision to the driver

![](https://lh7-us.googleusercontent.com/nBaQUVOZ9LEg8LgzUfhr3iWtLWXpWUQFCQkcoAhTupDifrQhVmxIWM4Y1s_vtyqxNCCVo5D--kvXYmB37EMlp83u7CXxhzRaOH6RTx6WTTUZNmwJIDy25gn0BpVywuu5pV5BeJpcJpy7GjgK7_4npeI)

[[a]](#cmnt_ref1)auto paths screenshots?

[[b]](#cmnt_ref2)once i get em ye

