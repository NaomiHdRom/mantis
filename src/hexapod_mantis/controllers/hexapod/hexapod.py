# mantis.py
# Hexapod controller with reordered legs

from controller import Robot
import math

def main():
    robot = Robot()
    time_step = int(robot.getBasicTimeStep())

    # =====================================================
    # ORDEN DE PATAS:
    # Leg 1 -> LF
    # Leg 2 -> RF
    # Leg 3 -> RM
    # Leg 4 -> PR
    # Leg 5 -> LR
    # Leg 6 -> LM
    # =====================================================

    motor_names = [
        # Leg 1 – Left Front (LF)
        "joint_1A", "joint_1B", "joint_1C",

        # Leg 2 – Right Front (RF)
        "joint_2A", "joint_2B", "joint_2C",

        # Leg 3 – Right Middle (RM)
        "joint_3A", "joint_3B", "joint_3C",

        # Leg 4 – Posterior Right (PR)
        "joint_4A", "joint_4B", "joint_4C",

        # Leg 5 – Left Rear (LR)
        "joint_5A", "joint_5B", "joint_5C",

        # Leg 6 – Left Middle (LM)
        "joint_6A", "joint_6B", "joint_6C"
    ]

    motors = []
    for name in motor_names:
        motor = robot.getDevice(name)
        if motor is None:
            print(f"❌ Motor no encontrado: {name}")
            return
        motor.setPosition(0.0)
        motors.append(motor)

    # ================= GAIT =================

    f = 0.5  # frecuencia [Hz]

    # amplitudes [rad]
    aA = 0.25   # coxa
    aB = 0.20   # femur
    aC = 0.05   # tibia

    a = [
         aA,  aB, -aC,   # Leg 1 (LF)
        -aA, -aB,  aC,   # Leg 2 (RF)
         aA,  aB, -aC,   # Leg 3 (RM)
         aA, -aB,  aC,   # Leg 4 (PR)
        -aA,  aB, -aC,   # Leg 5 (LR)
         aA, -aB,  aC    # Leg 6 (LM)
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

    print("✅ Hexapod controller running (legs reordered)")

    while robot.step(time_step) != -1:
        t = robot.getTime()
        for i in range(18):
            pos = a[i] * math.sin(2.0 * math.pi * f * t + p[i]) + d[i]
            motors[i].setPosition(pos)

if __name__ == "__main__":
    main()