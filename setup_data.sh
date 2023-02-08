#/bin/bash
echo "Start downloading Davis Hand Dataset..."

wget -O DavisHandDataset-EventsData.zip https://drive.ugr.es/index.php/s/rLq5wVayaoj8yff/download

echo "Davis Hand Dataset download finished"

echo "Unzip events into two folders: AllEvents and TrackerEvents..."

unzip ./DavisHandDataset-EventsData.zip

echo "Unzip process finished"

python3 organize_dataset.py

echo "Process finished, Dataset ready"
