
The \*.msg files need to be moved to a src/project/msg
Uncomment in package.xml
	  <build_depend>message_generation</build_depend>
	  <run_depend>message_runtime</run_depend>

In CMakeLists.txt 
   the REQUIRED COMPONENTS
        message_generation
   `add_message_files`
	uncomment and change *.msg to the new messages
   `generate_messages`
	uncomment the entire thing


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

# Usage

# Start both
	$ roslaunch hotshot hotshot.launch
