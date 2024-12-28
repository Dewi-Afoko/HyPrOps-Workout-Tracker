
### USER FUNCTIONS ###

# Log in

POST request to /api/login

Body = {username: username, password: password}
Success = {'message' : 'Login successful, welcome $username', 'token' : $access_token}, 200 (success)
Failure = {"error": "Invalid login credentials"}, 401 (access denied),
        {"error" : "Username not provided}, 400 (bad request),
        {"error" : "Password not provided}, 400 (bad request)


# Create a user:

POST request to /api/users

Body = {username: username, password: password}
Success = {"messgage" : "user.username successfully registered!"}, 201 (created)
Failure = {"error": "Username already exists"}, 409 (conflict),
         {"error": "Username not provided"}, 400 (bad request),
         {"error": "Password not provided"}, 400 (bad request)

# Return all users:

GET request to /api/users

Success = {"message" : [User.to_dict for User in database]}, 200 (success)
Failure = {"error": "No users found!"}, 404 (not found)

# Add PersonalData to user:

POST request to /api/users/add_personal_data

All fields optional, will only update if value provided
Body = {
        "name" : name,
        "dob" : str(%Y/%m/%d),
        "height" : height,
        "weight" : weight
}
Success = {"message" : "Personal data updated"}, 201 (created)

### WOKOUT FUNCTIONS ###

# Return users workouts:

GET request to /api/workouts

Success = {"message": "Here are your workouts :", "workouts" : [workout.to_dict()]}, 200 (success)
Failure = {"error" : "User not found"}, 404 (not found),
        {"error": "No workouts found"}, 404 (not found)


# Return single workout:

GET request to /api/workouts/<workout_id>

Success = {"message": "Here are the details for workout ID: $workout_id", "workout" : workout.to_dict()}, 200 (success)
Failure = {"error" : "User not found"}, 404 (not found),
        {"error": "No workouts found"}, 404 (not found),
        {"error": "Workout not found"}, 404 (not found)

# Create workout:

POST request to /api/workouts

Success = {"message" : "$workout.workout_name created by $user.username:}, 201 (created)
Failure = {"error": User not found}, 404 (not found)
        {"error": "You need to name your workout"}, 400 (bad request)



# Add notes to workout

PATCH request to /api/workouts/<workout_id>/add_notes

Body = {"notes" : notes}
Success = {"message" : "$notes added to workout notes"}, 200 (succes)
Failures = User not found: 404, No workouts found: 404,  Workout not found, 404

# Delete notes from workout by index position

DELETE request to /api/workouts/<workout_id>/delete_note/<note_index>

Success = {"message": "Note successfully deleted"}, 200 (success)
Failure = API_functions responses

# Toggle workout complete

PATCH request to /api/workouts/<workout_id>/mark_complete

Success = {"message" : "Workout marked as $status"}, 200 (success)
Failures = User not found: 404, No workouts found: 404,  Workout not found, 404

# Add UserStats to workout

PUT request to /api/workouts/<workout_id>/add_stats

-- Weight is pulled from PersonalData --
Requires PersonalData to exist!

Body = {
        "sleep_score" : sleep_score,
        "sleep_quality" : sleep_quality, (subjective)
        "notes" : notes
        }

Success = {"message" : "Stats added to workout"}, 201 (created)
Failures = {"error" : "No personal data found"}, 404 (not found),
        {"error" : "User stats not created"}, 400

# Add SetDict to workout

POST request to /workouts/<workout_id>/add_set

Body = {
        exercise_name: exercise name,
        set_type: set_type,
        reps: reps,
        focus: focus,
        rest: rest,
        notes: notes,
        loading: loading,
        }
Success = {"message" : "Set info for $set_dict.exercise_name created and added to $workout.workout_name}, 201 (created)
Failures =  {"error" : "Failure to create set dictionary"}, 400 (bad request),
        {"error" : "You need to specify an exercise}, 400 (bad request)


# Toggle SetDict complete by position in workout

PATCH request to /api/workouts/<workout_id>/<set_order>/mark_complete

Success = {"message" : "Set marked (in)complete"}, 200 (success)
Failures = User not found: 404, No workouts found: 404,  Workout not found, 404

# Add/overwrite notes to/in SetDict

PATCH request to /api/workouts/<workout_id>/<set_order>/add_notes

Body = {"notes" : notes}
Success = {"message" : "Notes added to set"}, 201 (created)
Failures = API function failures

# Delete SetDict notes

DELETE request to /api/workouts/<workout_id>/<set_order>/delete_notes

Success = {"message" : "Notes deleted"}, 200
Failures = API function failures