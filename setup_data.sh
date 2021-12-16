#/bin/bash
wget https://gist.githubusercontent.com/DaniDeniz/8dadbf249582bae1c570532838592214/raw/5d899ed753e360cd1e3db05094b696252bec0527/download_drive.py

echo "Start downloading Davis Hand Dataset..."

python3 download_drive.py --id 1zuPUSf94wnrlLUfCl5hrVOHhN7AaKbHv --destination ./DavisHandDataset-EventsData.zip

echo "Davis Hand Dataset download finished"

echo "Unzip events into two folders: AllEvents and TrackerEvents..."

unzip ./DavisHandDataset-EventsData.zip

echo "Unzip process finished"

python3 organize_dataset.py

echo "Process finished, Dataset ready"