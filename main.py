# import statements
import matplotlib.pyplot as plt

# base
all_drives = []  # list to hold data for all drives

# thresholds
t_eqi_safe = 0.5  # Upper bound for safe EQI
t_sqi_safe = 0.5  # Upper bound for safe SQI

# inputs and checks functions
def enter_values():
    while True:
        try:
            eye_closure_rate = float(input("Enter eye closure rate (as a percentage): "))
            if eye_closure_rate < 0 or eye_closure_rate > 100:
                print("Please enter value between 0 and 100%.")
                continue
            break  # valid
        except ValueError:
            print("Please enter a numeric value.")

    while True:
        try:
            blink_duration = float(input("Enter blink duration (in milliseconds): "))
            if blink_duration < 0:
                print("Please enter a non-negative value.")
                continue
            break  # valid
        except ValueError:
            print("Please enter a numeric value.")

    while True:
        try:
            saccadic_velocity = float(input("Enter saccadic velocity (degrees/second): "))
            if saccadic_velocity < 0:
                print("Please enter a non-negative value.")
                continue
            break  # valid
        except ValueError:
            print("Please enter a numeric value.")

    while True:
        try:
            steering_angle_variability = float(input("Enter steering angle variability (degrees): "))
            if steering_angle_variability < 0:
                print("Please enter a non-negative value.")
                continue
            break  # valid
        except ValueError:
            print("Please enter a numeric value.")

    while True:
        try:
            lane_deviation = float(input("Enter lane deviation (seconds): "))
            if lane_deviation < 0:
                print("Please enter a non-negative value.")
                continue
            break  # valid
        except ValueError:
            print("Please enter a numeric value.")
            
    while True:
        try:
            steering_correction_time = float(input("Enter steering correction time (seconds): "))
            if steering_correction_time < 0:
                print("Please enter a non-negative value.")
                continue
            break  # valid
        except ValueError:
            print("Please enter a numeric value.")

    # normalize with realistic capping
    norm_eye_closure = min(eye_closure_rate / 50, 1)
    norm_blink_duration = min(blink_duration / 500, 1) 
    norm_saccadic_velocity = min(saccadic_velocity / 30, 1)
    norm_steering_variability = min(steering_angle_variability / 15, 1)
    norm_lane_deviation = min(lane_deviation / 5, 1)  
    norm_steering_correction = min(steering_correction_time / 5, 1)  


    # Calculate u_eqi and u_sqi
    u_eqi = (
        norm_eye_closure * 0.5 +
        norm_blink_duration * 0.3 +
        (1 - norm_saccadic_velocity) * 0.2  # iverse
    )
    u_sqi = (
        norm_steering_variability * 0.6 +
        norm_lane_deviation * 0.3 +
        norm_steering_correction * 0.1
    )

    if u_eqi <= t_eqi_safe and u_sqi <= t_sqi_safe:
        print("Driver is proceeding safely and alertly. Please continue!")
    else:
        print("WARNING! Driver is likely suffering from drowsiness!")
    
    return [u_eqi, u_sqi]


# recording functions
def enter_new_drive():
    global all_drives

    while True:
        new_drive = input("Start a new drive (y or n): ").strip().lower()

        if new_drive == 'y':
            drive_data = []
            while True:
                print("\nEnter data for a new data point:")
                drive_data.append(enter_values())

                add_more = input("Add another data point to this drive? (y or n): ").strip().lower()
                if add_more == 'n':
                    break

            all_drives.append(drive_data)  # Add this drive's data points
            print(f"Drive {len(all_drives)} recorded with {len(drive_data)} data points.")
        elif new_drive == 'n':
            if len(all_drives) == 0:
                print("No drives recorded. See ya later!")
                break
            else:
                print("All drives recorded:")
                for i, drive in enumerate(all_drives, 1):
                    print(f"Drive {i}: {len(drive)} data points recorded.")
                plot_drives()
                break
        else:
            print("Please enter 'y' or 'n'.")


# plotting function
def plot_drives():
    if not all_drives:
        print("No drives to plot.")
        return

    for i, drive in enumerate(all_drives, 1):
        plt.figure()

        # Plot the safe zone
        plt.fill_betweenx(
            [0, t_sqi_safe],
            0, t_eqi_safe,
            color="green", alpha=0.2, label="Safe Zone"
        )

        # Plot each data point in this drive
        for j, (u_eqi, u_sqi) in enumerate(drive):
            color = "green" if u_eqi <= t_eqi_safe and u_sqi <= t_sqi_safe else "red"
            plt.scatter(u_eqi, u_sqi, color=color, label=f"Point {j+1}", edgecolors="black")

        # Customize the plot
        plt.xlabel("Eye Quality Index (EQI)")
        plt.ylabel("Steering Quality Index (SQI)")
        plt.title(f"Drive {i}: EQI vs SQI")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Show the plot for this drive
        plt.show()


# Start the program
enter_new_drive()
