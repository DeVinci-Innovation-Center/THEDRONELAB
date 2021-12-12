#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/orca/dvic/THEDRONELAB/ros_ws/src/pycrazyswarm"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/orca/dvic/THEDRONELAB/ros_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/orca/dvic/THEDRONELAB/ros_ws/install/lib/python3/dist-packages:/home/orca/dvic/THEDRONELAB/ros_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/orca/dvic/THEDRONELAB/ros_ws/build" \
    "/usr/bin/python3" \
    "/home/orca/dvic/THEDRONELAB/ros_ws/src/pycrazyswarm/setup.py" \
    egg_info --egg-base /home/orca/dvic/THEDRONELAB/ros_ws/build/pycrazyswarm \
    build --build-base "/home/orca/dvic/THEDRONELAB/ros_ws/build/pycrazyswarm" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/orca/dvic/THEDRONELAB/ros_ws/install" --install-scripts="/home/orca/dvic/THEDRONELAB/ros_ws/install/bin"
