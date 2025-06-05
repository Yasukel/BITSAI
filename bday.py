from datetime import datetime, date
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

def get_user_birthdate():
    while True:
        user_input = input(Fore.CYAN + "Enter your birthdate (YYYY-MM-DD): " + Style.RESET_ALL)
        try:
            birth_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            if birth_date > date.today():
                print(Fore.RED + "🚫 Birthdate cannot be in the future. Try again.")
                continue
            return birth_date
        except ValueError:
            print(Fore.RED + "❌ Invalid date format. Please use YYYY-MM-DD.")

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

def get_week_day(input_date):
    return input_date.strftime("%A")

def print_birthday_info(birth_date):
    print(Fore.YELLOW + f"🎉 Your birthday is on {birth_date.strftime('%B %d, %Y')}.")

# --- Main Program ---
if __name__ == "__main__":
    birth_date = get_user_birthdate()
    age = calculate_age(birth_date)
    weekday = get_week_day(birth_date)

    print(Fore.GREEN + f"🎂 You are {age} years old.")
    print(Fore.MAGENTA + f"📅 You were born on a {weekday}.")
    print_birthday_info(birth_date)
