
### USER FUNCTIONS ###

# Log in

POST request to /token/login

Body = {username: username, password: password}
Success = {'token': access_token, "advice": "It's dangerous to go alone, take this with you *hands over a *JWT*"}, 200 (success)
Failure = {"message": "Invalid username or password"}, 401 (access denied)

# Create a user:

POST request to /users

Body = {username: username, password: password}
Success = {id :user.id, username: user.username}, 200 (success)
Failure = {error: Username already exists}, 400 (bad request)

# Return all users:

GET request to /users

Success = [{id: user.id, username: user.username}], 200 (success)
Failure = {error: No users found!}, 400 (bad request)

### WOKOUT FUNCTIONS ###

# Return users workouts:

GET request to /workouts/<user_id>

Success = [workout.to_dict()], 200 (success)
Failure = {error: User not found}, 404 (not found)
#TODO: Add failure for no workouts

# Return single workout:

GET request to /workouts/<user4_id>/<workout_id>

Success = {workout: workout.to_dict()}, 200 (success)
Failure = {"error": "Workout not found"}, 404 (not found)

# Create workout:

POST request to /workouts</user_id>

Success = {user_id: user.id, workout_id: workout.id}, 201 (created)
Failure = {error: User not found}, 404 (not found)
#TODO: Add failure to create

Side-effect: Adds workout to user workout_list

# Add exercise to workout

POST request to /workouts/<user_id>/<workout_id>/add_exercise

Body = {exercise_name: exercise name}
Success = {workout id: workout.id, exercise added: exercise_name}, 201 (created)
Failures =  {error: Workout not found}, 404 (not found)
            {error: Exercise already exists, try adding details!}, 418 (I'm a teapot)
Success =   {workout id: workout.id, exercised added: exercise_name}, 201 (created)

# Add exercise details to nested workout

PATCH request to /workouts/<user_id>/<workout_id>/add_details

Body = {exercise_name: exercise name, # Only required field, all others optional
        reps: reps,
        loading: loading,
        rest: rest,
        notes: notes}
Failure = {error: Exercise not found!}, 418 (I'm a teapot)
Success* =  {reps: reps,
            loading: loading,
            rest: rest,
            notes: notes}, 201 (created)
            
            *Only details in body part of response

# Edit exercise details nested in workout

PATCH request to /workouts/<user_id>/<workout_id>/edit_details

Body = {reps_index: reps_index,
        reps_value: reps_value,
        loading_index: loading_index,
        loading_value: loading_value,
        rest_index: rest_index,
        rest_value: rest_value,
        performance_notes_index: performance_notes_index,
        performance_notes_value: performance_notes_value,
        }
Failures =  {message: No details to update provided or indices out of range}, 400 (bad request)
            {message: $field_value[index] out of range for $field}, 400 (bad request)
Success = {
    updated_reps: reps[reps_index] = reps_value,
    updated_loading: loading[loading_index] = loading_value,
    updated_rest: rest[rest_index] = rest_value,
    updated_performance_notes: performance_notes[performance_notes_index] = performance_notes_value}, 200 (success)

# Misc Auth Functions

GET request to /token/token_check

Success = {"message": f"Welcome, user {current_user}!", "advice": "It's dangerous to go alone, take this with you *hands over a *JWT*"}, 200 (success)