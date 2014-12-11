cmake_minimum_required(VERSION 2.8.3)
project(hotshot)

find_package(catkin
  REQUIRED
  COMPONENTS
  rospy
  sensor_msgs
  control_msgs
  cv_bridge
  dynamic_reconfigure
  baxter_core_msgs
  baxter_interface
 image_transport
  )
include_directories(
    ${catkin_INCLUDE_DIRS}
    )
add_executable(hotshot_image src/hotshot_image.cpp)
target_link_libraries(hotshot_image ${catkin_LIBRARIES})
# Declare the message files to be built
add_message_files(FILES
    centeringDirection.msg
    )
# Actually generate the language-specific message and service files
generate_messages(DEPENDENCIES std_msgs sensor_msgs)

catkin_package(
  CATKIN_DEPENDS
  rospy
  actionlib
  sensor_msgs
  control_msgs
  trajectory_msgs
  cv_bridge
  dynamic_reconfigure
  baxter_core_msgs
  baxter_interface
)

