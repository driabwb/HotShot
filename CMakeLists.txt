cmake_minimum_required(VERSION 2.8.3)
project(hotshot)
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  roscpp
  rospy
  geometry_msgs
  std_msgs
)
catkin_package(
)
include_directories(
  ${catkin_INCLUDE_DIRS}
)
add_executable(RosToOpencvImage src/projectImageReg.cpp)
target_link_libraries(RosToOpencvImage ${catkin_LIBRARIES})
