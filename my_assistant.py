from datetime import datetime
import time
import threading
import os 

current_focus = []
times_postponed = 0
break_time = False
break_interval = 30 
break_duration = 1
rest_time = 23 #works on few values because I am lazy
theme_script_path = "/home/sam/Coding/theme_script.sh"
light_wallpaper_path = "shotwell //usr/share/backgrounds/brad-huchteman-stone-mountain.jpg" 
dark_wallpaper_path = "shotwell ///home/sam/Downloads/MacOS-3D-4K-Dark.jpg"

def process_input(input_string):
    
    command = input_string.split(" ")[0]
    if command == "cf":
        current_focus.append(input_string[len(command)+1:])
    elif command == "did":
        current_focus[int(input_string[len(command)+1:])] = "DID"+current_focus[int(input_string[len(command)+1:])] 
    elif command == "postpone":
        current_focus[int(input_string[len(command)+1:])] = "POSTPONED"+current_focus[int(input_string[len(command)+1:])] 
    elif command == "dd":
        current_focus.pop(int(input_string[len(command)+1:]))
    elif command == "clear":
        current_focus.clear()

    elif command == "postpone":
        #postpone() which is called using a new local thread or process
        print("feature yet to be implemented")
    elif command == "continue":
        #thread.restart() this requires making the thread a global variable or maybe that won't work. See below
        print("feature yet to be implemented")

    elif command == "exit":
        input_string = input("Consider entering what you learnt today. Press Enter to exit.\n")
        if input_string:
            learning_log = open("learning_log.txt", "a")
            learning_log.write(datetime.today().strftime("%d/%m/%Y")+", "+input_string+"\n")
            learning_log.close()
        exit()

    else:
        inbox_file = open("inbox_file.txt", "a")
        inbox_file.write(input_string+"\n")
        inbox_file.close()

    print("Current focus")
    for i in range(0, len(current_focus)):
        print(i, ":", current_focus[i]) 

    process_input(input())

def start_breaks():
    print("Break in", break_interval, "minutes")
    time.sleep(break_interval*60)
    print("It is break time. Start work again in", break_duration, "minutes")
    break_time = True
    current_time = int(datetime.now().strftime("%H"))
    if current_time >= 18:
        os.system(dark_wallpaper_path)
    else:
        os.system(light_wallpaper_path)
    time.sleep(break_duration*60)
    print("Break is over. Time to continue")
    break_time = False
    break_thread = threading.Thread(target=start_breaks, daemon = True)
    break_thread.start()
    
def check_for_work_hours():
    current_time = int(datetime.now().strftime("%H"))

    if current_time >= rest_time:
        print("Time to stop working. It is time to rest now. Continue tomorrow")
        time.sleep(1*60) #interval to remind again
        work_hours_check_thread = threading.Thread(target=check_for_work_hours, daemon = True)
        work_hours_check_thread.start()

    if current_time < rest_time:
        time_left_str = str((datetime.strptime(str(rest_time), "%H") - datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")))
        time_left_array = time_left_str.split(":")
        time_left = 3600*int(time_left_array[0])+60*int(time_left_array[1])+int(time_left_array[2]) 
#        print(time_left)
        time.sleep(time_left)
        work_hours_check_thread = threading.Thread(target=check_for_work_hours, daemon = True)
        work_hours_check_thread.start()
 
def schedule_theme_change():
    current_time = int(datetime.now().strftime("%H"))

    if current_time >= 19:
        os.system(theme_script_path)
    else:
        time_left_str = str((datetime.strptime(str(19), "%H") - datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")))
        time_left_array = time_left_str.split(":")
        time_left = 3600*int(time_left_array[0])+60*int(time_left_array[1])+int(time_left_array[2]) 
#        print(time_left)
        time.sleep(time_left)
        theme_change_thread = threading.Thread(target = schedule_theme_change, daemon = True)
        theme_change_thread.start()


if __name__ == "__main__":
    print("Welcome buddy")
 
    break_thread = threading.Thread(target=start_breaks, daemon = True)
    break_thread.start()
    
#    work_hours_check_thread = threading.Thread(target=check_for_work_hours, daemon = True)
#    work_hours_check_thread.start()
    
    theme_change_thread = threading.Thread(target = schedule_theme_change, daemon = True)
    theme_change_thread.start()

    process_input(input())

#Now let's start with the design
#What are the features?

#inbox -> file, persistant ####
#different types of entries in inbox -> file, persistant ####
#distraction journal i.e high priority in inbox -> file, persistant ####
#scheduled breaks -> defined in code
#current focus -> list, non persistant ####

#now let's start with inbox ####
#inbox -> name, type, priority, url, start_date,  ####

#type -> video, search, to-do, web_article ####

#priority -> low, medium, high ####

#input data using this format for clarity ####
#video url ####
#video url name ####
#search name ####
#todo name ####
#todo name ####
#read later url ####
#read later url name ####
#distraction name ####
#distraction url name ####

#break time ####
#postpone minutes (tells you how many times you have already postponed the breaks)
#break is over ####
#continue (it basically reschedules the break from this moment if it was longer than defined)

#cf name ####
#did index ####
#postpone index ####
#dd index ####
#clear (empties the list) ####

#The thing about threads is that there doesn't seem to be an elegant way to stop or restart them.
#There is something called process in python that seems to be advanced version of threads with stop and restart support. 
#Maybe I shoud just switch to processes.

#Some useful links
# https://realpython.com/intro-to-python-threading/
# https://stackoverflow.com/questions/15729498/how-to-start-and-stop-thread
# https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
# https://medium.com/@bfortuner/python-multithreading-vs-multiprocessing-73072ce5600b
