# ROS STUFF

everything Ros takes place in **ros_ws/**

to create a new package got to **ros_ws/src/** and run 

    catkin_create_dpkg nameofpackage rospy

then a folder with the name of your package will be created in **ros_ws/src/**

now add your scripts in the **src/** of that folder.

run the following command on the script you want to execute:

    chmod +x main.py

you might want to include a shebang at the head of that file:

    #!/usr/bin/env python3

you can check that this worked by running the script with:

    ./main.py

it should have changed colors.

we now have to declare wich scripts to install.
That is done by modifying the **CMakelist.txt** of your package.

search for the section called: "**catkin_install_python**"

uncomment and fill it according to your package. It should look something like this:


    catkin_install_python(PROGRAMS
    src/main.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    )

When your package is ready:

go to **ros_ws/** and run the following command:

    catkin_make

we then need to source the environment:

    source devel/setup.bash

and that's it !! try running your package threw:

    rosrun packagename main.py