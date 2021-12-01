execute_process(COMMAND "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/build/pycrazyswarm/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/build/pycrazyswarm/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
