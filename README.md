# 2016 Robot Code
**Robot Code** | [UI](https://github.com/frc1418/2016-UI) | [Image Processing](https://github.com/frc1418/2016-vision) | [Oculus Rift](https://github.com/frc1418/2016-oculus)

This code was used to control Team 1418's robot in 2016, during the FIRST Stronghold challenge.

The team had a historic season in 2016. They were part of the 1st place alliance at the Greater DC District competition at Battlefield High School, and then proceeded to lead the first place alliances at the Bethesda District competition and the Chesapeake Regional Championship. The team finished the stellar season by making it to quarterfinals at the World Championship in St. Louis.

## Robot code features

* Full pyfrc integration for testing & robot simulation
* Unit tests over the robot code with 70% code coverage
* Arcade drive system
* Allows manipulation of arm, winch, and intake
* Complex autonomous mode support
	* Multiple working autonomous modes used in competition
		* Charge - Drive straight forward at maximum speed for a few seconds. Used for static defenses like rock wall, ramparts, and rough terrain.
        * ChargeCamera - Drives over defense, then uses vision to score ball in low goal
        * GenericAutonomous - Basic autonomous modes to go over most defenses including low bar, portcullis, cheval, and generic charge.
        * Defense autonomous modes:
            * Cheval - Go over cheval de frise
            * LowBar - Go over low bar
            * Portcullis - Go through portcullis
        * ModularAutonomous - Automatically generated autonomous using setup built in UI
	* Automatic support for tuning autonomous mode parameters via the UI

## Deploying onto the robot

The robot code is written in Python, so to run it you must install
[pyfrc](https://github.com/robotpy/pyfrc) onto the robot.

With the pyfrc library installed, you can deploy the code onto the robot
by running robot.py with the following argument:

	python3 robot.py deploy

This will run the unit tests and upload the code to the robot of your
choice.

## Testing/Simulation

The robot code has full integration with pyfrc. Make sure you have pyfrc
installed, and then you can use the various simulation/testing options
of the code by running robot.py directly.

    python3 robot.py sim

## File Structure

    robot/
    	The robot code lives here.
        automations/
            Several automatic scripts for performing common functions like shooting a ball.
        autonomous/
            Autonomous modes.
        common/
            New robotpy components
        components/
            Management of complicated robot systems
	tests/
		py.test-based unit tests that test the code and can be run via pyfrc
    electrical_test/
    	Barebones code ran to make sure all of the electronics are working

## Authors

* [Tim Winters](https://github.com/Twinters007)
* [Carter Fendley](https://github.com/CarterFendley)
* [Matt Puentes](https://github.com/killerhamster222)
* [Dustin Spicuzza](https://github.com/virtuald), mentor
* [Erik Boesen](https://github.com/ErikBoesen)