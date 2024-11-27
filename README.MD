## This isn't an actual read me, this is just so I can remember the last thing I did... 😅

# **Where We're At...**

- Workout components all functional
    - Creation
    - Adding exercises
        - Adding details to exercises
        - Marking exercise complete
    - Marking workouts as complete
    - Displaying all workouts
        - Click through for detailed view
        - This is where you add details/exercises
    - Logic relies on onClick and localStorage to return/edit correct values
        - localStorage set whenever exercise or workout clicked
            - Also when you click into a field on the details component

- State and Navigation added in some places, but not comprehensive
    - Need to start removing alerts/console logs from debugging

- Login and Registration complete
    - Might want to re-issue tokens outside of during login

- Navbar added with all relevant paths

# Known issues:

- Adding details to exercises not _quite_ right
    - Currently "Bodyweight" is a visual placeholder on the frontend only
        - Means adding more loading overwrites the first empty value, ie. replaces bodyweight with new loading

- Inconsistent styling
    - Aesthetics are a mess, I know this, we'll get back to it later

# Big decisions for next steps!

- Live tracker or workout planner first?
- When to add extra user data, ie. weight, etc.?
- Kotlin frontend. When?
    