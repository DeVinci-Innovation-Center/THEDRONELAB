execute_process(COMMAND "/home/orca/dvic/THEDRONELAB/ros_ws/build/stateMachine/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/orca/dvic/THEDRONELAB/ros_ws/build/stateMachine/catkin_generated/python_distutils_install.sh) returned error code ")
endif()