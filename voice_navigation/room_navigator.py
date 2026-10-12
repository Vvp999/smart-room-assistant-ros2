import speech_recognition as sr
import subprocess


rooms = {
    "kitchen": (3.186, 3.529),
    "living": (6.814, 3.150),
    "bedroom": (7.610, -2.388),
    "dining": (-0.452, 1.977),
    "study": (-4.178, 3.360),
    "store": (-4.226, -1.196)
}

r = sr.Recognizer()

while True:

    with sr.Microphone(device_index=8) as source:

        print("\nSpeak now...")

        r.adjust_for_ambient_noise(source, duration=1)

        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()

        print("You said:", command)

    except Exception as e:
        print("Voice recognition failed:", e)
        continue

    if "exit" in command:
        print("Exiting...")
        break

    room = None

    if "kitchen" in command:
        room = "kitchen"
    elif "living" in command:
        room = "living"
    elif "bedroom" in command:
        room = "bedroom"
    elif "dining" in command:
        room = "dining"
    elif "study" in command:
        room = "study"
    elif "store" in command:
        room = "store"

    if room is None:
        print("Room not recognized")
        continue

    x, y = rooms[room]

    print(f"\nNavigating to {room}")
    print(f"Goal X={x} Y={y}")

    goal = (
        f"{{pose: {{header: {{frame_id: map}}, "
        f"pose: {{position: {{x: {x}, y: {y}, z: 0.0}}, "
        f"orientation: {{w: 1.0}}}}}}}}"
    )

    print("Goal string:")
    print(goal)

    cmd = [
        "ros2",
        "action",
        "send_goal",
        "/navigate_to_pose",
        "nav2_msgs/action/NavigateToPose",
        goal
    ]

    subprocess.run(cmd)

    print("Navigation goal sent")