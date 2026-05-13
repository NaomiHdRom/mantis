# mantis.py
# Python controller for your Hexapod in Webots

from controller import Robot
import math

def main():
    robot = Robot()
    time_step = int(robot.getBasicTimeStep())

    # === Motores reales definidos en tu .wbt ===
    motor_names = [
        "joint_1A", "joint_1B", "joint_1C",
        "joint_2A", "joint_2B", "joint_2C",
        "joint_3A", "joint_3B", "joint_3C",
        "joint_4A", "joint_4B", "joint_4C",
        "joint_5A", "joint_5B", "joint_5C",
        "joint_6A", "joint_6B", "joint_6C"
    ]

    motors = []
    for name in motor_names:
        motor = robot.getDevice(name)
        motor.setPosition(0.0)  # modo posición
        motors.append(motor)

    # === Parámetros de marcha ===
    f = 0.5  # frecuencia [Hz]

    # amplitudes [rad]
    aA = 0.25   # coxa (rotación horizontal)
    aB = 0.20   # femur
    aC = 0.05   # tibia

    a = [
         aA,  aB, -aC,
        -aA, -aB,  aC,
         aA,  aB, -aC,
         aA, -aB,  aC,
        -aA,  aB, -aC,
         aA, -aB,  aC
    ]

    # fases
    p = [
        0.0, 2.0, 2.5,
        0.0, 2.0, 2.5,
        0.0, 2.0, 2.5,
        0.0, 2.0, 2.5,
        0.0, 2.0, 2.5,
        0.0, 2.0, 2.5
    ]

    # offsets (postura base)
    dA = 0.6
    dB = 0.8
    dC = -2.4

    d = [
        -dA,  dB,  dC,
         0.0, dB,  dC,
         dA,  dB,  dC,
         dA,  dB,  dC,
         0.0, dB,  dC,
        -dA,  dB,  dC
    ]

    print("✅ Hexapod controller running")

    while robot.step(time_step) != -1:
        t = robot.getTime()

        for i in range(18):
            pos = a[i] * math.sin(2.0 * math.pi * f * t + p[i]) + d[i]
            motors[i].setPosition(pos)

if __name__ == "__main__":
    main()