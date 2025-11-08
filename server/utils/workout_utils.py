from server.schemas.workout_schemas import WorkoutCreate, ExerciseName

def calculate_calories_burned(workout: WorkoutCreate, weight_kg = 70)->int:
    exercises = workout.exercises
    for exercise in exercises :
        duration_minutes = exercise.duration
        effective_reps = exercise.repetitions + (exercise.partial_reps * 0.5)
        reps_per_minute = effective_reps / duration_minutes if duration_minutes > 0 else 0
        if exercise.name == ExerciseName.pushup.name:
            
            if reps_per_minute < 10:
                MET = 3.8  
            elif reps_per_minute < 20:
                MET = 6.0  
            else:
                MET = 8.0 
        elif exercise.name == ExerciseName.squat.name:
            if reps_per_minute < 12:
                MET = 5.0  
            elif reps_per_minute < 25:
                MET = 7.0  
            else:
                MET = 9.0  
                
        elif exercise.name == ExerciseName.tricep_dip.name:
            if reps_per_minute < 8:
                MET = 3.5  
            elif reps_per_minute < 15:
                MET = 5.5  
            else:
                MET = 7.5  
        else:
            MET = 3.8  
        

        
        duration_hours = duration_minutes / 60
        calories = MET * weight_kg * duration_hours
        return round(calories)
