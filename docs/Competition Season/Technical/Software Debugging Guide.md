Software Debugging Guide

We’re having so many freaking problems in making the robot work that we should probably document them.

* Tele-op drift

Issues
------

1. Be careful to not collect too little data, or SysID will not work.
1. If the auto doesn’t drive straight, it’s hard to fix this. You should probably fix the auto, but it’s possible to align the robot so it gets the data before it drives off the carpet.
1. Make sure to actually implement SysID logging in code, logging is not automatic.
1. Doesn’t drive straight
1. You should probably tune your PID values
2. [What if my PID values seem to have zero effect on robot drift?](#h.gzimm45b3v6q)

        

Robot Drift Caused Without PID?
-------------------------------

5/11/2024

Had a weekend meeting today and spent a good 4 hours trying to figure out a simple question: why is the robot not driving straight?

At first, we believed it was PID values. We adjusted the Proportional term in turning PID to a value of 1, which hypothetically, should mean the robot should zigzag around the desired angle, as it violently oscillates around the setpoint. We tried this today, to zero effect, the behavior was the exact same as before. A bit later, we identified the issue that we believe was causing this, which is that rotational PID sets its setpoint to what it is currently at. Essentially, the input will take in a xspeed, y speed, and rotation. It converts these to be speeds to be delivered to the robot, a translation and rotation speed. When the turning motors of the robot don’t have to move to satisfy this, the PID sets the setpoint to be the current position. This means that if the wheels have drifted, the PID doesn’t prevent this, but reinforces it, allowing the drift to continue.

We operated under this theory for the entire meeting today, and tried a bunch of different things to address it:

#### If the user is not rotating the robot, set the setpoint for turning to the last setpoint

The idea behind this was that by setting the rotational setpoint to what it was previously every time .drive() was called, it would fix our issue, as long as the user hasn’t rotated the robot since then. Didn’t work because the wheels can rotate without one explicitly using the rotation stick. (If you’re facing forward and try to go 90 deg right, the wheels need to rotate, and this doesn’t account for that). In retrospect yes this was a silly idea.

#### Randomly set the rotation setpoint to -100 or 100, so the average is zero.

        What the frick was the point of this idea? How did we greenlight this? It made sense at the time, I promise (Rohit).

        (it was really funny so it was totally worth it)

#### Figure out the math to make idea #1 work (current theory)

Our condition for setting the setpoint to what it was previously was exclusively based off the rotation stick, the right stick, this approach would use math and stuff to figure out what inputs would change the rotation of the wheels, and depending on whether the current input would change the rotation of the wheels or not, do method #1. 

        

        

[https://www.chiefdelphi.com/t/rotational-drift-when-trying-to-drive-in-a-straight-line/455761/2](https://www.google.com/url?q=https://www.chiefdelphi.com/t/rotational-drift-when-trying-to-drive-in-a-straight-line/455761/2&sa=D&source=editors&ust=1717314662129182&usg=AOvVaw1uiGEBx3u3PMpAeUkBxAtM)

They have the same issue.

