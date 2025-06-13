# OpenMANIPULATOR-X: Quick Setup

1. Configure all Dynamixel actuators to **Current (Torque Control) mode** using DYNAMIXEL Wizard 2.0.

2. Verify USB device:

    ls /dev/ttyUSB*

   Confirm the device is `/dev/ttyUSB0`.

3. Add your user to the `dialout` group for serial port permissions:

    sudo usermod -aG dialout $USER

   Then, log out and log back in.

4. Ensure the communication baud rate is set to **1 Mbps (1000000 bps)**.

5. Launch the hardware node with gravity compensation:

    ros2 launch open_manipulator_bringup hardware_x.launch.py

---

This procedure guarantees active torque control and operational gravity compensation.
