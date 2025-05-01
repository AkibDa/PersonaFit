import pandas as pd

def get_user_data():
    print("Please enter your details:")
    try:
        print("Note: Age should be a number, Weight in kg, Height in cm.")
        name = input("Name: ")
        age = int(input("Age: "))
        if age < 0 or age > 100:
            print("Age must be between 0 and 100.")
            return None
        weight = float(input("Weight (kg): "))
        if weight < 0 or weight > 300:
            print("Weight must be between 0 and 300 kg.")
            return None
        height = float(input("Height (cm): "))
        if height < 0 or height > 300:
            print("Height must be between 0 and 300 cm.")
            return None

        valid_muscles = ['waist', 'upper legs', 'lower legs', 'chest',
                         'back', 'upper arms', 'cardio', 'shoulders', 'lower arms']
        print(f"Available muscle groups: {', '.join(valid_muscles)}")
        muscle = input("What muscle do you want to hit today? : ").lower()
        if muscle not in valid_muscles:
            raise ValueError(f"Please choose from these muscles: {', '.join(valid_muscles)}")

        print("Thank you for providing your details!")

    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting...")
        return None
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    return {
        "name": name,
        "age": age,
        "weight": weight,
        "height": height,
        "muscle": muscle,
    }


def get_workout_plan(muscle):
    try:
        db = pd.read_csv('exercises.csv')
        exercises = db[db['bodyPart'] == muscle][['name', 'instructions/0']]

        if exercises.empty:
            print(f"No exercises found for {muscle}.")
            return

        print(f"\nYour workout plan for {muscle}:")
        for idx, row in exercises.iterrows():
            print(f"\nExercise: {row['name']}")
            print(f"Instructions: {row['instructions/0']}")

    except FileNotFoundError:
        print("Error: exercises.csv file not found.")
    except Exception as e:
        print(f"An error occurred while generating workout plan: {e}")


if __name__ == "__main__":
    print("Welcome to PersonaFit!")
    print("This is a simple program to help you with personalized plans for your fitness goals.")

    user_data = get_user_data()
    if user_data:
        print(f"\nHello {user_data['name']}, based on your details, we will create a personalized plan for you.")
        get_workout_plan(user_data['muscle'])

    print("\nThank you for using PersonaFit! Have a great day!")