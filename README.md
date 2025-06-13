# OpenMANIPULATOR-X: 

1. Configurar Dynamixel en modo Effort (Torque Control) con DYNAMIXEL Wizard 2.0.

2. Verificar dispositivo USB:

    ls /dev/ttyUSB*

   Confirmar que el dispositivo sea `/dev/ttyUSB0`.

3. Añadir usuario al grupo dialout para permisos:

    sudo usermod -aG dialout $USER

   Reiniciar sesión.

4. Asegurar que la velocidad de comunicación (baud rate) esté en 1 Mbps (1000000 bps).

5. Ejecutar nodo hardware con compensación de gravedad:

    ros2 launch open_manipulator_bringup hardware_x.launch.py

---

Este procedimiento garantiza control torque activo y compensación de gravedad operativa.

