import pandas as pd

def get_user_data():
    print("Please enter your details:")
    try:
        print("Note: Age should be a number, Weight in kg, Height in cm.")
        name = input("Name: ")
        age = int(input("Age: "))
        if age<0 or age>100:
            print("Why need a workout plan?\nTake some rest.")
            return None
        weight = float(input("Weight (kg): "))
        height = float(input("Height (cm): "))
        if weight<0 or weight>100 or height<0 or height>1000:
            print("Why need a workout plan?\nTake some rest.")
            return None
        experience_level = input("Experience Level (Beginner, Intermediate, Advanced): ").capitalize()
        if experience_level not in ["Beginner", "Intermediate", "Advanced"]:
            raise ValueError("Experience level must be either Beginner, Intermediate, or Advanced.")
        muscle = input("What muscle do you want to hit today? : ").capitalize()
        if muscle not in ['Core', 'Full Body', 'Shoulders', 'Chest', 'Back', 'Arms', 'Legs']:
            raise ValueError("Mention Proper Muscle!")
        print("Thank you for providing your details!")
        
    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting...")
        return None
    
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
        "experience_level": experience_level,
        "muscle": muscle,
    }

def get_workout_plan(experience_level, muscle):
    db = pd.read_csv('sample_exercise_dataset_100.csv')
    print(f"\n{experience_level} workout plan:")

    print(db[(db['experience_level'] == experience_level) & (db['muscle_group'] == muscle)]['exercise_name'])

if __name__ == "__main__":
    print("Welcome to PersonaFit!")
    print("This is a simple program to help you with personalized plans for your fitness goals.")
    user_data = get_user_data()
    print(f"Hello {user_data['name']}, based on your details, we will create a personalized plan for you.")
    print("User Data:", user_data)
    get_workout_plan(user_data["experience_level"],user_data['muscle'])
    print("Thank you for using PersonaFit! Have a great day!")
    