from models import User, Workout, SetDicts
from flask import Flask, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity

def check_for_error(result): #FUNCTIONALITY Checks whether the tuple has a length of two and the second item is a number, ie. a status code.
    return isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], int)

def get_credentials(data):
    username = data.get('username')
    password = data.get('password')
    
    if username is None:
        return {'error': 'Username not provided'}, 400
    
    if password is None:
        return {'error': 'Password not provided'}, 400
    
    return {'username': username, 'password': password}, 200


def find_user_from_jwt():
    username = get_jwt_identity()
    user = User.objects(username=username).first()
    if not user:
        return {'error' : 'User not found'}, 404
    else:
        return user
    
def find_user_workouts_list():
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    workouts = Workout.objects(user_id=user)
    workouts = list(workouts)
    if not workouts:
        return {'error' : 'No workouts found'}, 404

    return workouts

def workouts_as_dict(workouts):
    try:
        workout_dicts = [workout.to_dict() for workout in workouts]
        return workout_dicts
    except AttributeError:
        return {'error' : 'No workouts found'}, 404



def find_single_workout(workout_id):
    workouts = find_user_workouts_list()
    if check_for_error(workouts):
        return workouts
    for workout in workouts:
        if str(workout.id) == workout_id:
            return workout
    return {'error' : 'Workout not found'}, 404
    
def find_set_dicts(workout_id):
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout
    set_dicts = []
    for set in workout.set_dicts_list:
            set_dicts.append(set.to_dict())
            return {'error' : 'No sets not found'}, 404
    return set_dicts

def find_single_set_dict(workout_id, set_order):
    set_dicts = find_set_dicts(workout_id)
    if check_for_error(set_dicts):
        return set_dicts
    for set in set_dicts:
        if set.set_order == set_order:
            return set
    return {'error' : 'No sets not found'}, 404


