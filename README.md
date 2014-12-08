# Installation

	$ sudo apt-get install ros-indigo-visp

## Get the source
	# mkdir ~/catkin_ws/src
	$ cd ~/catkin_ws/src
	$ git clone https://github.com/nbellowe/HotShot.git

	$ source ~/catkin_ws/devel/setup.bash

## Build the catkin packages from source

	$ cd ~/catkin_ws
	$ catkin_make 

# Start both
	$ roslaunch hotshot hotshot.launch
