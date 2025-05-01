import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
import joblib
import os
import datetime as date

def model_training():
    # Step 1: Load cleaned dataset
    df = pd.read_csv("cleaned_exercise_dataset.csv")

    # Step 2: Select features for ML
    features = ["muscle_group", "equipment", "difficulty", "goal_type", "training_type", "experience_level", "reps", "sets"]

    # Step 3: Scale numerical features
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])

    # Step 4: Train KNN model
    knn_model = NearestNeighbors(n_neighbors=5, metric='euclidean')
    knn_model.fit(X)

    # Save the model and scaler
    joblib.dump(knn_model, "workout_knn_model.pkl")
    joblib.dump(scaler, "scaler.pkl")

    print("KNN workout recommendation model trained and saved.")

def get_user_data():
    print("Please enter your details:")
    try:
        print("Note: Age should be a number, Weight in kg, Height in cm.")
        name = input("Name: ")
        age = int(input("Age: "))
        weight = float(input("Weight (kg): "))
        height = float(input("Height (cm): "))
        goal = input("Fitness Goal (e.g., strength, hypertrophy, cardio, endurance): ").capitalize()
        experience_level = input("Experience Level (Beginner, Intermediate, Advanced): ").capitalize()
        if experience_level not in ["Beginner", "Intermediate", "Advanced"]:
            raise ValueError("Experience level must be either Beginner, Intermediate, or Advanced.")
        valid_goals = ["Strength", "Hypertrophy", "Cardio", "Endurance"]
        if goal not in valid_goals:
            raise ValueError(f"Goal must be one of {valid_goals}.")
        training_type = input("Training Type (e.g., upper body, core, full body): ").capitalize()
        muscle_group = input("Preferred Muscle Group (e.g., legs, arms, back, chest): ").capitalize()
        equipment = input("Preferred Equipment (e.g., dumbbells, barbell, bodyweight): ").capitalize()
        if equipment not in ["Dumbbells", "Barbell", "Bodyweight"]:
            raise ValueError("Equipment must be either Dumbbells, Barbell, or Bodyweight.")
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
        "training_type": training_type,
        "muscle_group": muscle_group,
        "experience_level": experience_level,
        "equipment": equipment,
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
    
def recommend_workouts_ml(user_input):
    # Load data, model, and scaler
    df = pd.read_csv("cleaned_exercise_dataset.csv")
    knn_model = joblib.load("workout_knn_model.pkl")
    scaler = joblib.load("scaler.pkl")
    
    # Encode and prepare user input
    le_dict = {
        "muscle_group": LabelEncoder().fit(df["muscle_group"]),
        "equipment": LabelEncoder().fit(df["equipment"]),
        "goal_type": LabelEncoder().fit(df["goal_type"]),
        "training_type": LabelEncoder().fit(df["training_type"]),
        "experience_level": LabelEncoder().fit(df["experience_level"]),
    }
    
    # Encode input
    user_vector = [
        le_dict["muscle_group"].transform([user_input["muscle_group"]])[0],
        le_dict["equipment"].transform([user_input["equipment"]])[0],
        le_dict["goal_type"].transform([user_input["goal"]])[0],
        le_dict["training_type"].transform([user_input["training_type"]])[0],
        le_dict["experience_level"].transform([user_input["experience_level"]])[0],
        user_input["reps"],
        user_input["sets"],
    ]

    # Scale
    user_vector_scaled = scaler.transform([user_vector])

    # Get recommendations
    indices = knn_model.kneighbors(user_vector_scaled, return_distance=False)[0]
    return df.iloc[indices][["exercise_name", "reps", "sets", "muscle_group"]].to_dict(orient="records")    
    
def workout_recommendation(user_data):
    # Load cleaned dataset
    df = pd.read_csv("cleaned_exercise_dataset.csv")

    # Load encoders (retrain them for mapping, ideally persist in real app)
    le_experience = LabelEncoder().fit(["beginner", "intermediate", "advanced"])
    le_goal = LabelEncoder().fit(["strength", "hypertrophy", "endurance", "cardio"])

    # Encode user inputs
    user_exp_encoded = le_experience.transform([user_data['experience_level'].lower()])[0]
    user_goal_encoded = le_goal.transform([user_data['goal'].lower()])[0]

    # Filter dataset based on experience level and goal
    filtered_df = df[
        (df["experience_level"] == user_exp_encoded) &
        (df["goal_type"] == user_goal_encoded)
    ]

    # Optional: filter based on preferences (muscle group or training type keywords)
    if user_data.get("preferences"):
        pref_filtered = []
        for pref in user_data["preferences"]:
            filtered = filtered_df[
                df["muscle_group"].astype(str).str.contains(pref.lower()) |
                df["training_type"].astype(str).str.contains(pref.lower())
            ]
            pref_filtered.append(filtered)
        if pref_filtered:
            filtered_df = pd.concat(pref_filtered).drop_duplicates()

    # Return top 5 recommendations
    return filtered_df.sample(min(5, len(filtered_df))).to_dict(orient="records")
     
def log_workout(user_id, workout_data, log_file="user_workout_history.csv"):
    """
    Append a user's workout session to a CSV history log.
    workout_data should be a list of dicts with keys: exercise_name, sets, reps, notes (optional)
    """
    today = str(date.today())
    records = []
    for item in workout_data:
        records.append({
            "user_id": user_id,
            "date": today,
            "exercise_name": item["exercise_name"],
            "sets": item["sets"],
            "reps": item["reps"],
            "notes": item.get("notes", "")
        })
    
    df_new = pd.DataFrame(records)

    # Append or create file
    if os.path.exists(log_file):
        df_existing = pd.read_csv(log_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(log_file, index=False)
    print(f"Workout logged for {user_id} on {today}")     
     
def get_user_progress(user_id, log_file="user_workout_history.csv"):
    if not os.path.exists(log_file):
        return f"No workout history found for {user_id}."

    df = pd.read_csv(log_file)
    user_df = df[df["user_id"] == user_id]

    if user_df.empty:
        return f"No data for {user_id}."

    # Group by exercise, show total sets/reps over time
    summary = user_df.groupby(["exercise_name", "date"])[["sets", "reps"]].sum().reset_index()
    return summary     

if __name__ == "__main__":
    print("Welcome to PersonaFit!")
    print("This is a simple program to help you with personalized plans for your fitness goals.")
    user_data = get_user_data()
    print(f"Hello {user_data['name']}, based on your details, we will create a personalized plan for you.")
    print("User Data:", user_data)
    data_cleaning()
    model_training()
    recommend_workouts_ml(user_data)
    log_workout(user_data['name'], recommend_workouts_ml(user_data))
    print("Workout logged successfully.")
    get_user_progress(user_data['name'])
    print("User progress retrieved successfully.")
    print("Thank you for using PersonaFit! Have a great day!")
    