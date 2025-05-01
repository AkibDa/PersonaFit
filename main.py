import pandas as pd
from sklearn.preprocessing import LabelEncoder

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
        "goal": goal,
        "preferences": pref
    }
    
def data_cleaning():
    # Load the CSV
    df = pd.read_csv("sample_exercise_dataset_100.csv")

    # 1. Drop rows with any missing values (or fill with defaults)
    df.dropna(inplace=True)

    # 2. Strip whitespaces & lowercase standardization
    df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)

    # 3. Label encode categorical columns
    label_encoders = {}
    categorical_cols = ["muscle_group", "equipment", "difficulty", "goal_type", "training_type", "experience_level"]

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le  # Save encoders if needed later
        
    # 4. (Optional) Convert reps to numeric range midpoint
    def parse_reps(rep_str):
        try:
            if '-' in rep_str:
                low, high = rep_str.replace(" reps", "").split('-')
                return (int(low) + int(high)) / 2
            elif "sec" in rep_str:
                return int(rep_str.replace("sec", "").strip())
            elif "per" in rep_str:
                return int(rep_str.split()[0])  # e.g., "10 per leg"
            else:
                return int(rep_str)
        except:
            return None

    df["reps"] = df["reps"].apply(parse_reps)
        
    # 5. Convert sets to numeric
    df["sets"] = df["sets"].apply(lambda x: int(x) if str(x).isdigit() else None)

    # 6. Drop rows with invalid parsed numbers
    df.dropna(subset=["reps", "sets"], inplace=True)

    # 7. Save cleaned dataset
    df.to_csv("cleaned_exercise_dataset.csv", index=False)

    print("Dataset cleaned and saved as 'cleaned_exercise_dataset.csv'")
    
if __name__ == "__main__":
    print("Welcome to PersonaFit!")
    print("This is a simple program to help you with personalized plans for your fitness goals.")
    user_data = get_user_data()
    print(f"Hello {user_data['name']}, based on your details, we will create a personalized plan for you.")
    print("User Data:", user_data)
    data_cleaning()