from models import User, UserStats, Workout, SetDicts, PersonalData
from flask import Flask, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity

def tuple_checker(object):
    return isinstance(object, tuple)

def get_credentials(data):
    username = data.get('username')
    password = data.get('password')
    if username == None:
        return jsonify({'error': 'Username not provided'}), 400
    if password == None:
        return jsonify({'error': 'Password not provided'}), 400
    return {'username': username,
            'password': password}

def find_user_from_jwt():
    username = get_jwt_identity()
    user = User.objects(username=username).first()
    if not user:
        return jsonify({'error' : 'User not found'}), 400
    else:
        return user
    
def find_user_workouts_list():
    user = find_user_from_jwt()
    workouts = []
    for workout in user.workout_list:
        workout_dict = workout.to_dict()  
        workouts.append(workout_dict)

        if not workouts:
            return jsonify({'error' : 'No workouts found'}), 400
        
    return workouts

def find_single_workout(workout_id):
    workouts = find_user_workouts_list()
    for workout in workouts:
        if workout.id == workout_id:
            return workout
    if not workout:
            return jsonify({'error' : 'Workout not found'}), 400
    
def find_set_dicts(workout_id):
    workout = find_single_workout(workout_id)
    set_dicts = []
    for set in workout.set_dicts_list:
            set_dicts.append(set.to_dict())
            return jsonify({'error' : 'No sets not found'}), 400
    return set_dicts

def find_single_set_dict(workout_id, set_order):
    set_dicts = find_set_dicts(workout_id)
    for set in set_dicts:
        if set.set_order == set_order:
            return set
    return jsonify({'error' : 'No sets not found'}), 400
