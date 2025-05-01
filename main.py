import streamlit as st
import pandas as pd

# Load exercise data
@st.cache_data
def load_data():
  try:
    df = pd.read_csv('fitness_exercises.csv')
    return df
  except:
    st.error("❌ Exercise database not found. Please ensure 'fitness_exercises.csv' is in the correct directory.")
    return None


# Main app
def main():
  st.set_page_config(page_title="PersonaFit", page_icon="💪", layout="wide")

  st.title("💪 PersonaFit - Your Personal Fitness Assistant")
  st.markdown("### Get customized workout plans based on your body metrics")

  # Sidebar for user input
  with st.sidebar:
    st.header("Your Details")
    name = st.text_input("Name*", help="Required field")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=300, value=70)
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)

    muscle_options = ['waist', 'upper legs', 'lower legs', 'chest',
                      'back', 'upper arms', 'cardio', 'shoulders', 'lower arms']
    target_muscle = st.selectbox("Target Muscle Group*", muscle_options)

    if st.button("Generate Workout Plan", type="primary"):
      if not name:
        st.warning("⚠️ Please enter your name")
      else:
        user_data = {
          "name": name,
          "age": age,
          "weight": weight,
          "height": height,
          "muscle": target_muscle
        }
        st.session_state.user_data = user_data
        st.session_state.show_plan = True

  # Main content area
  if 'show_plan' not in st.session_state:
    st.session_state.show_plan = False

  if st.session_state.show_plan:
    user_data = st.session_state.user_data
    df = load_data()

    if df is not None:
      st.header(f"🏋️‍♂️ {user_data['name']}'s Personalized Workout Plan")
      st.subheader(
        f"Target: {user_data['muscle'].title()} | Age: {user_data['age']} | Weight: {user_data['weight']}kg | Height: {user_data['height']}cm")

      # Filter exercises
      filtered_exercises = df[df['bodyPart'].str.lower() == user_data['muscle']]

      if filtered_exercises.empty:
        st.warning(f"❌ No exercises found for {user_data['muscle']}.")
      else:
        st.success(f"✅ Found {len(filtered_exercises)} exercises for you!")

        for i, exercise in filtered_exercises.iterrows():
          with st.expander(f"**{i + 1}. {exercise['name'].title()}** ({exercise['equipment'].title()})",
                           expanded=False):
            col1, col2 = st.columns([1, 2])

            with col1:
              # Display exercise GIF with error handling
              try:
                gif_url = exercise['gifUrl']
                if pd.notna(gif_url) and gif_url.startswith('http'):
                  st.markdown(f"**Exercise Demo:**")
                  st.markdown(f'<img src="{gif_url}" width="100%">', unsafe_allow_html=True)
                else:
                  st.warning("GIF not available")
              except Exception as e:
                st.error(f"Couldn't load GIF: {str(e)}")

            with col2:
              st.markdown(f"**Equipment:** {exercise['equipment'].title()}")
              st.markdown("**Instructions:**")

              # Handle instructions/0 column
              if 'instructions/0' in exercise:
                instructions = exercise['instructions/0']
              elif 'instructions' in exercise:
                instructions = exercise['instructions']
              else:
                instructions = "No instructions available"

              st.write(instructions)

              # YouTube search link
              youtube_search = f"https://www.youtube.com/results?search_query={exercise['name'].replace(' ', '+')}+exercise"
              st.markdown(f"[📺 Watch YouTube Tutorials]({youtube_search})", unsafe_allow_html=True)

        # Download button
        csv = filtered_exercises[['name', 'equipment', 'bodyPart']].to_csv(index=False)
        st.download_button(
          label="📥 Download Workout Plan",
          data=csv,
          file_name=f"{user_data['name']}_{user_data['muscle']}_workout.csv",
          mime="text/csv"
        )

  # About section
  st.sidebar.markdown("---")
  st.sidebar.markdown("""
    **About PersonaFit**  
    Uses the [Fitness Exercises Dataset](https://www.kaggle.com/datasets/omarxadel/fitness-exercises-dataset)
    """)


if __name__ == "__main__":
  main()