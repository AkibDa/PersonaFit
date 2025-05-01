def get_user_data():
    print("Please enter your details:")
    try:
        print("Note: Age should be a number, Weight in kg, Height in cm.")
        print("Make sure to provide your preferences clearly.")
        name = input("Name: ")
        age = int(input("Age: "))
        weight = float(input("Weight (kg): "))
        height = float(input("Height (cm): "))
        goal = input("Fitness Goal (e.g., weight loss, muscle gain, maintenance): ")
        pref = input("Preferences (Home or Gym, available equipment): ")
        print("Thank you for providing your details!")
        
    except TypeError:
        print("Invalid input. Please enter valid data types.")
        return None
    
    except ValueError:
        print("Invalid input. Please enter numeric values for age, weight, and height.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    return {
        "name": name,
        "age": age,
        "weight": weight,
        "height": height,
        "goal": goal,
        "preferences": pref
    }
    
if __name__ == "__main__":
    print("Welcome to PersonaFit!")
    print("This is a simple program to help you with personalized plans for your fitness goals.")
    user_data = get_user_data()
    print(f"Hello {user_data['name']}, based on your details, we will create a personalized plan for you.")
    print("User Data:", user_data)