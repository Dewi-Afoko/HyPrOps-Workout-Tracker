from unittest.mock import Mock
from lib.exercise import Exercise

def test_creating_exercise_sets_name():
    exercise1 = Exercise("Pull Up")
    assert exercise1.name == "Pull Up"

def test_creating_exercise_sets_variables_to_empty():
    exercise1 = Exercise("Pull Up")
    assert exercise1.name == "Pull Up"
    assert exercise1.type == []
    assert exercise1.muscles == []
    assert exercise1.equipment == []

def test_add_lift_type():
    exercise1 = Exercise("Pull Up")
    exercise1.add_lift_type("Compound")
    assert exercise1.type == ["Compound"]

def test_add_lift_types():
    exercise1 = Exercise("Pull Up")
    exercise1.add_lift_type("Compound")
    exercise1.add_lift_type("Calisthenics")
    assert exercise1.type == ["Compound", "Calisthenics"]

def test_add_muscle():
    exercise1 = Exercise("Pull Up")
    exercise1.add_muscle("Lats")
    assert exercise1.muscles == ["Lats"]

def test_add_muscles():
    exercise1 = Exercise("Pull Up")
    exercise1.add_muscle("Lats")
    exercise1.add_muscle("Forearms")
    assert exercise1.muscles == ["Lats", "Forearms"]

def test_add_equipment():
    exercise1 = Exercise("Bench Press")
    exercise1.add_equipment("Barbell")
    assert exercise1.equipment == ["Barbell"]

def test_add_equipments():
    exercise1 = Exercise("Bench Press")
    exercise1.add_equipment("Barbell")
    exercise1.add_equipment("Bench")
    assert exercise1.equipment == ["Barbell", "Bench"]

def test___eq___true():
    exercise1 = Exercise("Bench Press")
    exercise1.add_equipment("Barbell")
    exercise1.add_equipment("Bench")
    exercise2 = Exercise("Bench Press")
    exercise2.add_equipment("Barbell")
    exercise2.add_equipment("Bench")
    assert exercise1 == exercise2

def test___eq___false():
    exercise1 = Exercise("Bench Press")
    exercise1.add_equipment("Barbell")
    exercise1.add_equipment("Bench")
    exercise2 = Exercise("Bench Press")
    exercise2.add_equipment("Barbell")
    assert exercise1 != exercise2

def test___repr__():
    exercise1 = Exercise("Bench Press")
    exercise1.add_equipment("Barbell")
    exercise1.add_equipment("Bench")
    assert exercise1.__repr__() == "Exercise(Bench Press, [], [], ['Barbell', 'Bench'])"