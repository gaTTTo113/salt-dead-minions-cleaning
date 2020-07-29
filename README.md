# Salt dead minions cleaning
This script automates deleting not working machines from minions list of your salt-master.
Logic: collecting all not-responding machines per day to the file (potential_minions_to_delete),
after machine name adding a number representing not-active days of this particular machine, if the number cross 30 – deleting the machine from minions list of current salt-master.

# How to use:
Create cronjob for the script and not forget to add sudo rights.
Simply use:

### sudo crontab -e

This runs a command at 2:00 AM:

### 0 2 * * * python your_directory/dead_minion_cleaning.py

