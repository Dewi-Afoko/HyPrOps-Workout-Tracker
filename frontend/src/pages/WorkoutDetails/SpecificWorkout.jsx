import AddSetToWorkout from "../../components/WorkoutAddSet"
import WorkoutDetailsById from "../../components/WorkoutDetailsById"


export function SpecificWorkout() {
    const workoutId = localStorage.getItem('workout_id')

    return(
        <div>
<WorkoutDetailsById workoutId={workoutId}/>
        </div>
    )
}