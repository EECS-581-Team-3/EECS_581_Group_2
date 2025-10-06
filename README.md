Operations
For graphical interface:
    Run gui.py file through your prefered Python launcher
    To run through the command line, run the following command
        'python <file-path>/gui.py'

    User controls:
        'New Game' button
            Left click: resets game state and display to new game conditions, based on custom parameters set by user
        'Custom' button:
            Launches Custom Difficulty dialog box
            Lets player set board size within limits of 4 to 20, inclusive
            Lets player set number of mines within limits of 1 to number of cells - 1 (board size squared - 1), inclusive
            Apply: saves changes to parameters, resets game state and display to new parameters
            Cancle: closes dialog box without saving or resetting
        Board cells:
            Left click: reveals cell, whether cell contains a mine or not
            Right click: flags or unflags cell

For terminal interface:
    Run main.py file through your prefered Python launcher
    To run through the command line, run the following command
        'python <file-path>/main.py'

    User controls:
        Follow terminal prompts


Environmental requirements
Python version: Python3
Modules:
    random - for mine placement
    tkinter - for GUI
    os - for terminal interface, to clear terminal between changes in game state (optional)

*Documentation for the changes made by Group 3 can be found in the Main branch as "Group 3 Project 2 Master Document."
