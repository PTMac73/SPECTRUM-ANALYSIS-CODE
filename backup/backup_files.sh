#!/bin/bash
# Variables
OUT_DIR="/run/media/ptmac/PTMAC USB/Backup"
IN_DIR="/home/ptmac/Documents/"
LOG_DIR="/home/ptmac/Software/backup/backup-logs"
MAX_NUM_TRIES=11
NUM_TRIES=0

BACKUP_ICON="media-removable"
FAIL_ICON="emblem-important"

function add_leading_zero(){
	if (( $1 < 10 ))
	then
		echo "0${1}"
	else
		echo "${1}"
	fi
}


function seconds2hours(){
	tot_time=$1
	min=0
	hour=0
	sec=0
	if (( $tot_time > 59 ))
	then
		sec=$((tot_time%60))
		tot_time=$((tot_time/60))
		if (( $tot_time > 59 ))
		then
			min=$((tot_time%60))
			tot_time=$((tot_time/60))
			hour=$tot_time
		else
			min=$((tot_time))
		fi
	else
		sec=$((tot_time))
	fi

	# Now print it
	HOUR_STR=`add_leading_zero ${hour}`
	MIN_STR=`add_leading_zero ${min}`
	SEC_STR=`add_leading_zero ${sec}`

	echo "$HOUR_STR:$MIN_STR:$SEC_STR"
}

# Check that the directory exists
while [[ ! -d ${OUT_DIR} && $NUM_TRIES -lt $MAX_NUM_TRIES ]]
do
	NUM_TRIES=$((NUM_TRIES + 1))
	DATE_STR=`date +"%Y-%m-%d %H:%M:%S"`
	notify-send --urgency=critical --icon="${FAIL_ICON}" 'Backup FAILED. Directory not found.' "${DATE_STR} -- Will try again in 10 mins..."
	sleep 600
done

# Backup if it finds the directory
if [[ $NUM_TRIES -lt $MAX_NUM_TRIES ]]
then
	# Send notification
	notify-send --urgency=critical --icon="${BACKUP_ICON}" 'Backup STARTED'

	# Write the date string
	DATE_STR=`date +"%Y_%m_%d.%H_%M"`

	# Create a log file
	FILE="${DATE_STR}_backup.log"
	touch "${LOG_DIR}/${FILE}"

	# Run rsync
	START=$(date +%s)
	rsync -auP --delete --exclude=*.gz --exclude=iss000_run_*.gtd* --exclude=GEBMerged_run*.gtd_* --update --links --safe-links "${IN_DIR}" "${OUT_DIR}" >> "${LOG_DIR}/${FILE}"
	DUR=$(echo "$(date +%s) -$START" | bc )
	DUR_STR=`seconds2hours $DUR`

	# Send notification based on status of result
	if [[ $? -eq 0 ]]
	then
		notify-send --urgency=critical --icon="${BACKUP_ICON}" 'Backup COMPLETE' "Time taken: ${DUR_STR}"
	else
		notify-send --urgency=critical --icon="${FAIL_ICON}" "Backup FAILED. Unknown cause." "Time taken: ${DUR_STR}"
	fi
else
	# Send notification telling the user that it failed
	notify-send --urgency=critical --icon="${FAIL_ICON}" 'Backup FAILED' "Plug in your USB and run the backup_files.sh script to try again. Time taken: ${DUR_STR}"
fi


