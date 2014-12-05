cmake_minimum_required(VERSION 2.8.3)
project(hotshot)
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  roscpp
  rospy
  geometry_msgs
  std_msgs
  message_generation
)
include_directories(
  ${catkin_INCLUDE_DIRS}
)
add_executable(RosToOpencvImage src/projectImageReg.cpp)
target_link_libraries(RosToOpencvImage ${catkin_LIBRARIES})


  # Declare the message files to be built
add_message_files(FILES
    centeringDirection.msg
  )

  # Actually generate the language-specific message and service files
generate_messages(DEPENDENCIES std_msgs sensor_msgs)

  # Declare that this catkin package's runtime dependencies
catkin_package(
   CATKIN_DEPENDS message_runtime std_msgs 
  )
