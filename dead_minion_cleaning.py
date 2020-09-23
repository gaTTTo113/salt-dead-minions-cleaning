import os
import re
from datetime import date

# reading output from salt's ping
minions_status = re.split('\n', os.popen('salt \'*\' test.ping').read())
minions_status.remove("")

# parsing output from salt's ping, separating true and false answers
# for moment of writing this script,
# first string always was name of minion and next was answer from ping
this_is_minions_name = True
answered_true = []
answered_false = []
# minions list here
minions_names = []

for message in minions_status:
    if this_is_minions_name:
        minions_names.append(message)
    else:
        if message == '    True':
            answered_true.append(minions_names[minions_names.__len__() - 1][:-1])
        else:
            # all types failed here
            answered_false.append(minions_names[minions_names.__len__() - 1][:-1])
    this_is_minions_name = not this_is_minions_name

# collecting minions answered false
new_minions_to_delete = []
try:
    potential_to_delete = re.split('\n', open('potential_minions_to_delete', 'r').read())
except:
    potential_to_delete = []

# if false minion is already on list pass it
for minion in answered_false:
    for minion_to_delete in potential_to_delete:
        minion_to_delete = re.split(' ', minion_to_delete)
        if minion_to_delete[0] == minion:
            continue
        else:
            if new_minions_to_delete.__contains__(minion):
                continue
            else:
                new_minions_to_delete.append(minion)

for minion in new_minions_to_delete:
    potential_to_delete.append(minion + ' 0')

# if true minion appeared in list of potential to delete
# remove it from list
for minion_true in answered_true:
    for minion_to_delete in potential_to_delete:
        minion_to_delete = re.split(' ', minion_to_delete)
        if minion_to_delete[0] == minion_true:
            potential_to_delete.remove(minion_to_delete[0] + ' ' + minion_to_delete[1])

# separating dead/not dead
dead_minions = []
# not_dead_yet means server dosn't respond, but wasn't listed before/or in time period
not_dead_yet = []
for new_minion_to_delete in new_minions_to_delete:
    for minion_to_delete in potential_to_delete:
        minion_to_delete = re.split(' ', minion_to_delete)
        if minion_to_delete[0] == new_minion_to_delete:
            not_dead_yet.append(minion_to_delete[0] + ' ' + minion_to_delete[1])
            minion_to_delete[1] = str(int(minion_to_delete[1]) + 1)
            if re.search(minion_to_delete[0] + ' \d', str(dead_minions)):
                continue
            else:
                dead_minions.append(minion_to_delete[0] + " " + minion_to_delete[1])

for minion in not_dead_yet:
    for minion_to_delete in dead_minions:
        if minion == minion_to_delete:
            dead_minions.remove(minion)

if dead_minions.__contains__(''):
    dead_minions.remove('')

# deleting dead minions from salt master
deleted = []
for minion in dead_minions:
    minion = re.split(" ", minion)
    if int(minion[1]) >= 30:
        os.system('salt-key -d \'' + minion[0] + '\' -y')
        deleted.append(minion[0])
        dead_minions.remove(minion[0] + " " + minion[1])

# saving logs
if len(deleted) != 0:
    output_file = open('deleted_minions_' + str(date.today()), 'w')
    for minion in deleted:
        for letter in minion:
            output_file.write(letter)
        output_file.write('\n')
    output_file.close()

# preparing for next iteration
potential_to_delete_file = open('potential_minions_to_delete', 'w')
for minion in dead_minions:
    for letter in minion:
        potential_to_delete_file.write(letter)
    potential_to_delete_file.write('\n')
potential_to_delete_file.close()
