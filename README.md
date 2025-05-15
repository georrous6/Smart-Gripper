# SmartGripperHackathon

### Project Structure Overview

* **/src**
  Contains the core implementation code that is deployed to and executed on the Gripper.

* **/gui**
  Provides an interactive graphical interface. An additional `README.md` file within this folder explains how to use the GUI.

* **/docs**
  Includes all reference materials used during development. Full books are provided to ensure consistency and completeness in documenting the model built in MATLAB.

* **/object\_classification**
  Contains code for object classification, which can be integrated with the GUI to enhance the overall user experience.

Details regarding the simulation of the model are provided in the following section.

---

- Simulations and Modeling
  
  In this folder we :
  - Simulate the desired force we need to apply in a object through a fuzzy logic decision
    
      This script builds, visualises, and tests a Fuzzy-Inference System (FIS) called GripperFIS.
      The controller estimates how much gripping force a robotic gripper should apply, given two object properties:

      Variable	Role	Range	Linguistic terms (bell-shaped MFs)
    
        - Weight	Input	0 – 500 g	VeryLight · Light · Medium · Heavy
    
        - Hardness	Input	0 – 1 (soft → hard)	VerySoft · Soft · Hard · VeryHard
    
        - Force	Output	0 – 10 (arbitrary units)	VeryLow · Low · Medium · High

      1 . Define inputs and outputs
        addInput and addOutput create the three FIS variables.
        Each variable is assigned 4 generalized bell membership functions (gbellmf) that overlap smoothly and look like Gaussian “bells”.

        fis = addInput(fis,[0 500],'Name','Weight');
        fis = addMF(fis,'Weight','gbellmf',[40 2 50],'Name','VeryLight');
        ...
        fis = addInput(fis,[0 1],'Name','Hardness');
        ...
        fis = addOutput(fis,[0 10],'Name','Force');
        Parameter vector [a b c] means:
        a = width, b = slope, c = centre of the bell.

        2 . Create the rule base (4 × 4 = 16 rules)
          ruleList maps every combination of the two inputs to a force level.

          Example rule:

              If Weight is Heavy and Hardness is Soft then Force is High
          Rules are imported with addRule(fis,ruleList);.

        3 . Visualise the system
          plotfis shows a block diagram of the FIS.

          plotmf plots the membership functions for each variable.

          The surface plot (surf) illustrates how Force varies over the full Weight–Hardness grid.

        4 . Quick test case
          evalfis(fis,[300 0.4]) evaluates the controller for a 300 g object with medium hardness (0.4) and prints the recommended force.
  - model the BLDC motor system we got from the documentation and we apply an adaptive pid controller for the control

      ⚙️ Adaptive PID Controller with BLDC Motor Simulation and Wiener Filtering
        This MATLAB script simulates an adaptive PID control loop for a Brushless DC (BLDC) motor system. It includes:

        A 2st-order electromechanical model of a BLDC motor

        A PID controller that adapts its gains using gradient descent

        A custom calculation of settling time to evaluate controller performance

        A Wiener filter for post-processing noisy output data

        📌 Features  
        🔧 PID Control with Online Tuning
        The PID controller updates its parameters (Kp, Ki, Kd) at each time step based on the current error and the error in settling time, aiming to:

        Track a given target speed

        Achieve a desired settling time

        🔄 BLDC Motor Model
        The model consists of coupled electrical and mechanical dynamics:
 

        📉 Wiener Filter for Signal Denoising
        After simulation, the noisy output (motor speed) is passed through a Wiener filter for noise suppression.

        📈 Output
        Real-time PID gain updates printed in the console

        Plots:

          System response with adaptive PID tuning

          Denoised output using Wiener filtering

        Example:

          t=3.50, omega=5.42, settling=1.02, Kp=98.75, Ki=48.75, Kd=0.08

        📦 Main Components

        Section	Description

        for loop	Main simulation loop

        calculateSettlingTime()	Computes time until the output stabilizes within ±5% of target
        gradient descent	Updates PID gains based on combined error
        wiener2()	Applies Wiener filter to noisy signal
        plot()	Shows system response and filtering results

        🧠 Learning Logic

        The learning step adjusts all PID gains equally using:

        grad = 0.1 * (tracking_error + settling_time_error);
        Kp = Kp - lr * grad;

        ⚠️ Note: As we will see we achieved an optional pid for the dynamic system through control and learning for the parameters

🛠️ System Parameters

Symbol	Description	Value
R	Motor resistance	50 Ω
L	Motor inductance	0.1 H
Ke	Back EMF constant	1 V·s/rad
Kt	Torque constant	1 Nm/A
J	Rotor inertia	0.01 kg·m²
B	Viscous friction	0.001 N·m·s

📊 Sample Visualizations

✅ System response vs. target

🔵 Filtered signal using Wiener filter
    
