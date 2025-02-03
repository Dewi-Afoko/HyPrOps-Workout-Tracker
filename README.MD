# This isn't an actual read me, this is just so I can remember the last thing I did... 😅

# Next Steps!

We're splitting into two development branches:

    - Branch 1: New features
        - Exercise DB, User Record Embedded Document

    - Branch 2: Django Migration
        - Learn enough Django to build Branch 1 in a way that's easy to convert from flask

## Update!
Exciting news, the MVP/Alpha is built and ready to use! I'll use it for my workouts this week, use that as an opportunity to find any bugs, then clean up code, documentation and any bug fixes next week! 🍾

### Alpha Testing UI Improvements:
    - Live Tracking Page Created
        - Next Five Sets component added to feed 
            - Refactored display to be more useful
            - Displays to the left of the screen
        - Added Last Five Sets component
            - Returns most relevant data
            - Displays to the right of the screen
        - Countdown timer based on rest intervals displays once set marked complete
            - Default value/timer completion now displays "Time to start your next set!"
        - Split view of complete/incomplete sets, updates dynamically once set marked complete
            - Edit sets by clicking the exercise name in either complete or incomplete table
                - Modal now launches for the individual field selected

### v3 - Three Model Version

    - Reduced complexity by moving to three models
    - TDD principles followed
    - Backend now has all functionality required to have meaningful application once API routes and frontend refactored
    - Implement Flask-RESTX and Swagger for namespaces and API documentation ✅
    - Create functional JavaScript/React web frontend ✅
    - Create interactive tables for workouts and sets ✅


## Next Goals

    - Create a user-friendly interface ✅
        - Split workouts into complete and incomplete feeds ✅
        - Copy/Use workout as template ✅

