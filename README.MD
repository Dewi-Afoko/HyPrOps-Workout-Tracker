# This isn't an actual read me, this is just so I can remember the last thing I did... 😅

### Update:
New backend TDDed, DRY and RESTful AF! 
Currently: Refactoring frontend components


## **Where We're At...**

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

- Split view for individual workout with exercise tables in complete/incomplete columns

- Deletion of all details (individually or collectively) and exercises possible

- State and Navigation added in some places, but not comprehensive
    - Need to start removing alerts/console logs from debugging

- Login and Registration complete
    - Might want to re-issue tokens outside of during login

- Navbar added with all relevant paths

## Known issues:

- Adding details to exercises not _quite_ right
    - ~~Currently "Bodyweight" is a visual placeholder on the frontend only~~ Zero is zero!
        - Means adding more loading overwrites the first empty value, ie. replaces bodyweight with new loading
            - This logic is still a problem
                - Potentially looking at a redesign of data structures of workouts
                - Want to be able to mark a set as complete.

- Deleting fields doesn't always have intended effect, depending on length of other arrays
    - Solve with nested dictionaries?

- Inconsistent styling
    - Aesthetics are a mess, I know this, we'll get back to it later

## Big decisions for next steps!

- Live tracker or workout planner first?
- When to add extra user data, ie. weight, etc.?
- Kotlin frontend. When?
    
