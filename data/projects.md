# Intro Project
This project is a step by step idea of how a data project would work. Using a parquet file provided, you must either derive or graph what is asked of you. For each step, submit your code + necessary screenshots in a Jupyter notebook. If you are stuck on a step, please come to office hours.

## Our car
The data we will be using is from FS-3, our car from 2024-2025. This data was collected from the Norcal Shootout in 2025, a practice event to test our car more. The specific parquet I have provided came from Rolling Resistance tests. Our car was, and will always be electric. A motor controller (the SME channels) reports motor RPM, torque demand, and motor/controller temps. An accumulator pack, (the ACC channels) report pack voltage, current, per-cell volage, temperature across segments, and state of charge.

**The IMU**  
The vehicle dynamics module has an intertial inertial unit on board, the VDM X/Y/Z AXIS ACCELERATION (in g's) and the VDM_X/Y/Z AXIS YAW RATE (in °/s) come from it. This is an independent way of seeing how the car is physically doing, separate from the motor signal or GPS. If the car brakes hard, you can see it in the acceleration axes without needing to check the brake sensors at all; if it's cornering, the yaw rate would show it. This will come in handy during your intro project.

**GPS**  
VDM_GPS_Latitude and VDM_GPS_Longitude don't just tell you where the car is in the world, but can also show you where the car is, especially in a fixed area (eg a track). When plotted against each other can show the shape of the track the car drove. GPS also gives you speed (VDM_GPS_SPEED measured in MPH!!) and altitude, which you can use to cross check during your project. The values from the GPS speed are less accurate, as they transmit less frequently compared to 'SME_TRQSPD_Speed.'

**Brake Data**  
There are three different brake related signals. ETC_STATUS_BRAKELIGHT is a simple on/off flag for when the brake light is lit, which is a clear indicator of when the car is braking. ETC_STATUS_BRAKE_SENSE_VOLTAGE tells you more; it's the voltage of the brake's sensor. It moves proportionally with how hard the brake is pressed. TMAIN_DATA_BRAKES_F and TMAIN_DATA_BRAKES_R go further, giving separate front and rear brake pressure; however that data may not be useful for this project.

## Onboarding Project Steps
1. Using parquet logic, forward fill and print all the values in a table format from the file. Provide a screenshot from your terminal display of what got printed.
2. a) Using matplotlib, graph the speed of the car(in MPH) vs time. Refer to the [data_columns.csv](https://github.com/formulaslug/fs-5-software-intro-projects/blob/main/data/data_columns.csv) to know which column means what. Use that graph to find the speed of the car at 10s. To find the speed of the car, use 'SME_TRQSPD_Speed.' It is measured in RPM which you will need to convert. Please refer to the physics section below for the explanation. 
3. Give a time frame for when the car is accelerating, braking, and coasting. Explain how you found these values out. Then plot those states over time on three different graphs
4. Find out how many laps the car drove as well as the start and end time for each lap. The car has a GPS system you can utilize to visualize this. Provide a screenshot of your method along with an explanation of how you went about finding this.
5. Using the lap times found from part 4, determine the max speed, max acceleration, time spent accelerating, and time spent coasting. 
6. From the coasting data (from all laps), remove anything below 5 m/s and anything below a second. 
7. Use that coast down data to determine vehicle drag + rolling resistance. Please refer below for the explanation of the physics. 
8. Write 3 or more paragraphs about what you learned about the car, and your takeaways from the data.

## Physics

### **Step 2**
The motor and wheels do not spin at the same rate, and the wheels don't spin at the same rate as the car - which makes us need to convert through both to get car's real speed. 

The motor and wheel are connected by a sprocket + chain reduction: 12 teeth on the motor side, 41 on the wheel side. Since the wheel sprocket has more teeth, the wheel turns slower than the motor. Treat wRPM as wheel rpm and mRPM as motor RPM.

 $wRPM= mRPM * 12/41$

Now we need to convert wheel rpm into angular velocity, which is measured in radians per second. 

$ω = wRPM * (2pi/60)$

Finally, we need to convert angular velocity into a linear ground speed. Think about a ferris wheel, if you were standing in the middle, you are barely moving while the whole thing spins fast. If you are standing by the edge, you are covering more ground at the same spin rate, just a faster speed, since you are farther from the center. The same can be applied to a spinning wheel. The outside edge of the tire is a fixed distance from the center. Now that you know how fast the wheel is spinning, multiplying by the radius will give you the speed of the edge of the wheel. Since the car grips the road, the spot where the tire touches the pavement moves across the ground at the same speed - which is the car's speed.

This gives you a final equation of:

$v = mRPM * GR * (2pi/60) * WR$

*where v is your final speed, wRPM is wheel RPM, GR is gear ratio, and WR is wheel radius*

### **Step 7**

When the car is coasting, the only things slowing it down is drag and rolling resistance. This is why isolating the coast down data is an important step. Rolling resistance is roughly a constant regardless of speed, this is caused by the friction from the tires moving as they roll. The rolling resistance formula is: 

$F_-roll = Crr * m * g$

Crr is the rolling resistance coefficient, which is what we are trying to solve for. m is the car's mass and g is gravity(9.81 m/s). m * g is the car's weight pressing down on the tires. Since none of this depends on speed, the force stays roughly the same. 

Drag is the air pushing back against the car as it drives. This is where the aerodynamics comes in. If we were to be driving a rectangular block, it would head on face much more drag due to it's large frontal area. Compare that to a sleek F1 car, which is shaped that way to help air glide off of it, reducing drag. The equation for drag is:

$F_-drag = 1/2 * p * Cd * A * v^2$

p is air density, v is the car's speed, Cd is the drag coeff, and A is the frontal area. We will bundle Cd * A and solve for that value. Drag grows much faster with speed, since speed squared is a direct component of the formula. Doubling the speed quadruples the drag.

Both forces act together to slow the car down. Newton's second law says force equals mass times acceleration: a net force is what causes an object's speed to change

$m_-eff * (dv/dt) = -(F_-drag + F_-roll)$

*where m_eff is the effective mass*

The derivative of speed is acceleration. If you haven't taken calculus yet, do NOT fret. This just means the rate of change of velocity is acceleration. The effective mass is the car's mass + the changing inertial components.

Putting all the equations together gives us:

$m_-eff * dv/dt = - (.5 * p * Cd * A * v^2) - (Crr * m * g)$

*we can then move the effective mass over*  

$dv/dt = - ((.5 * p * Cd * A)/m_-eff) * v^2 - ((Crr * m * g)/m_-eff)$

We can now use this as an equation of a straight line, using v^2 as your x-axis and dv/dt as your y-axis. 

y = slope * x + intercept

Using your clean coastdown data, compute dv/dt at each point (the change in speed between consecutive readings, divided by the time between them), and plot it against v². Then fit a straight line through those points. The slope and intercept give you the unknowns.

$.5 * p * Cd * A = -slope * m_-eff$ *(drag term)*  
$Crr = -intercept * m_-eff / (m * g)$ *(rolling resistance term)*

## Information you might need
Gear ratio: 12/41 (sprocket ratio, motor-to-wheel)  
Wheel radius: 0.2 m  
Car mass: 221.4 kg  
Air density: 1.225 kg/m³  
Effective car mass or m_eff: 244.08 kg
