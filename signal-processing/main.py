import matplotlib.pyplot as plt
import time
from set_serial import set_ser

def main_algo(goal_study_time, study_time_completed = 0):

    if goal_study_time == 0:
        return None 
    # call serial.py for sets of every 5 minutes
    while goal_study_time > 0:
        begin_time = time.time()
        print("noyay")
        waves_binary = set_ser(3000) # 300 = 30 seconds
        print("yay")
        end_time = time.time()
        time_taken = round(end_time - begin_time, 2)
        goal_study_time -= time_taken
        study_time_completed += time_taken
        # 300 readings is 30 seconds: 3000 for demo, skip 600


    special_val = 0
    length_of_wavelist = 0
    for i in waves_binary:
        special_val += i
        length_of_wavelist += 1
    special_val = special_val/length_of_wavelist

    state = ""
    if special_val <= (4/10): # 4:6
        state = "unfocused"
    elif special_val <= (5/10):
        state = "slightly focused"
    elif special_val <= (7/10):
        state = "mildly focused"
    else:
        state = "focused"
    

    # if yes: dont do anything, if no: return study_time/4
    if state == "unfocused":
        time.sleep((study_time_completed*60)/4)
        main_algo(goal_study_time)
    else: # focused
        main_algo(goal_study_time, study_time_completed)
main_algo(2)