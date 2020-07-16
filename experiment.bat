@echo off 


if "%1"=="" (
echo "Please enter a participant number"
goto Done
)  

SET "var="&for /f "delims=0123456789" %%i in ("%1") do set var=%%i
if defined var (
echo "Please enter a numeric participant number"
goto Done
)


echo Participant Number: %1 
SET /A p=%1
::--------------------------------PRACTICE-------------------------------------
echo "Starting practice"
python synchDrawing.py --shape=circle --repeats=4 --practice --participantNumber=%p%
echo "Finished practice. Provide participant with experiment instruction."
python messageScreen.py --msg="Please wait for instructions from experimenter" --participantNumber=%p%

::--------------------------------PART 1--------------------------------------------
echo "Start part:1 block:1"
python synchDrawing.py --shape=circle --repeats=4 --participantNumber=%p%
echo "End part:1 block:1"
python messageScreen.py --msg="Please take a break and tap button to continue" --showContinue --participantNumber=%p% --questionnaire1="https://bangor.onlinesurveys.ac.uk/test_1-2"
echo "Start part:1 block:2"
python synchDrawing.py --shape=circle --repeats=4 --participantNumber=%p%
echo "End part:1 block:2"
python messageScreen.py --msg="Please take a break and tap button to continue" --showContinue --participantNumber=%p% --questionnaire1="https://bangor.onlinesurveys.ac.uk/test_1-2"
echo "Start part:1 block:3"
python synchDrawing.py --shape=circle --repeats=4 --participantNumber=%p%
echo "End part:1 block:3"
echo "Finished part 1 of the experiment. Provide participant with questionnaire."
python messageScreen.py --msg="Please take a break and tap button to continue" --showContinue  --participantNumber=%p% --questionnaire1="https://bangor.onlinesurveys.ac.uk/test_1-2" –questionnaire2=”https://bangor.onlinesurveys.ac.uk/test_1-2"

::--------------------------------PART 2------------------------------------------
echo "Start part:2 block:1"
python synchDrawing.py --shape=circle --repeats=4 --participantNumber=%p%
echo "End part:2 block:1"
python messageScreen.py --msg="Please take a break and tap button to continue" --showContinue --participantNumber=%p% --questionnaire1="https://bangor.onlinesurveys.ac.uk/test_1-2"
echo "Start part:2 block:2"
python synchDrawing.py --shape=circle --repeats=4 --participantNumber=%p%
echo "End part:2 block:2"
python messageScreen.py --msg="Please take a break and tap button to continue" --showContinue --participantNumber=%p% --questionnaire1="https://bangor.onlinesurveys.ac.uk/test_1-2"
echo "Start part:2 block:3"
python synchDrawing.py --shape=circle --repeats=4 --participantNumber=%p%
echo "End part:2 block:3"
echo "Finished part 2 of the experiment. Provide participant with questionnaire."
python messageScreen.py --msg="End of Task" --showContinue  --participantNumber=%p% --questionnaire1="https://bangor.onlinesurveys.ac.uk/test_1-2" –questionnaire2=”https://bangor.onlinesurveys.ac.uk/test_1-2"

::--------------------------------END------------------------------------------

:Done

echo "Done"