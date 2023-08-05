# run use case

Runs the specified action

## Input Data

- Path: Script location relative to ~/webhook-actions/
- Data: Additional data that is needed to run the script

## Output Data

- Enum of script running successfully, script not found, or script failed

## Primary Course

1. Run the script in the specfied location

## Exception Cases

- Return script not found if it's not found
