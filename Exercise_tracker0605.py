from colorama import Fore, Style, init

def summarize_weekly_workouts(weekly_goal_minutes):
    """
    Records and summarizes weekly workout data with colored output.

    Args:
        weekly_goal_minutes (int): The target number of minutes for the weekly workout goal.

    Returns:
        None: Prints the workout summary.
    """
    # Initialize Colorama for cross-platform compatibility
    init(autoreset=True)

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workout_minutes = {}
    total_exercised_minutes = 0
    longest_workout_day = ""
    max_workout_minutes = 0

    print(f"{Fore.CYAN}Please enter the number of minutes exercised for each day:")

    # 1. Get daily workout data
    for day in days_of_week:
        while True:
            try:
                minutes = int(input(f"{Fore.YELLOW}Minutes exercised on {day}: {Style.RESET_ALL}"))
                if minutes < 0:
                    print(f"{Fore.RED}Minutes cannot be negative. Please enter a valid number.{Style.RESET_ALL}")
                else:
                    workout_minutes[day] = minutes
                    total_exercised_minutes += minutes
                    # 3. Find the longest workout day
                    if minutes > max_workout_minutes:
                        max_workout_minutes = minutes
                        longest_workout_day = day
                    break
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")

    print(f"\n{Fore.MAGENTA}--- Workout Summary ---")

    # 2. Calculate total time
    print(f"📊 {Fore.YELLOW}Total minutes exercised: {total_exercised_minutes} minutes{Style.RESET_ALL}")

    # 3. Day with the longest workout
    if longest_workout_day:
        print(f"🥇 {Fore.GREEN}Day with the longest workout: {longest_workout_day} ({max_workout_minutes} minutes){Style.RESET_ALL}")
    else:
        print(f"🥇 {Fore.RED}No workouts recorded this week.{Style.RESET_ALL}")

    # 4. Whether the weekly goal was met
    if total_exercised_minutes >= weekly_goal_minutes:
        print(f"🎯 {Fore.RED}Weekly goal met! (Goal: {weekly_goal_minutes} minutes){Style.RESET_ALL}")
    else:
        print(f"🎯 {Fore.RED}Weekly goal not met. You exercised {total_exercised_minutes} minutes out of {weekly_goal_minutes} minutes.{Style.RESET_ALL}")

# --- Implementation Instructions ---
if __name__ == "__main__":
    # You can change the weekly_goal_minutes here to your desired goal
    weekly_target = 150
    summarize_weekly_workouts(weekly_target)