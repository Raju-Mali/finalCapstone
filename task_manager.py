# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATE_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding= "utf-8") as default_file:
        pass

with open("tasks.txt", 'r', encoding= "utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATE_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATE_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
''' This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding= "utf-8") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r', encoding= "utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

''' Below function request information from user and provide exception handling.
This function enable refactoring code simply by replacing -
'input' with 'req_info' to take benefit of exception handling '''
def req_info(req_ST):
    while True:
        try:
            req = input(req_ST)
            break
        except EOFError:
            print("\nApplied Keyboard shortcut are not available during this request.\n")
        except KeyboardInterrupt:
            print("\nSomething went wrong, Please try again.\n")
    return req

# Initial log In req.
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = req_info("Username: ")
    curr_pass = req_info("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


''' Add a new user to the user.txt file '''
def reg_user():
    while True:
        new_username = req_info("\nNew Username: ")
        if new_username in username_password.keys():
            print("This username already exists, Please try again.")
            continue
        elif len(new_username) == 0:
            print("Username is blank. Please enter a username.")
            continue
        else:
            break

    # - Request input of a new password
    while True:
        new_password = req_info("New Password: ")
        if len(new_password) == 0:
            print("\nPassword is blank. Please try again.\n")
            continue

        # - Request input of password confirmation.
        while True:
            confirm_password = req_info("Confirm Password: ")
            if len(new_password) == 0:
                print("\nPassword is blank. Please try again.\n")
                continue
            elif new_password != confirm_password:
                print("\nPasswords do not match\n")   

            else:
                break
        break

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w", encoding= "utf-8") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))


''' Below function allow a user to add a new task to 'task.txt' file
    Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task. '''
def add_task():
    while True:
        task_username = req_info("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = req_info("Title of Task: ")
        task_description = req_info("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATE_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
            except EOFError:
                print("Applied Keyboard shorts are not available during this request.")
            except KeyboardInterrupt:
                print("Something went wrong, Please try again.")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w", encoding= "utf-8") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATE_STRING_FORMAT),
                    t['assigned_date'].strftime(DATE_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        break

''' Below function is copy of line 156 to 169 from above function.
This function will serve to write out changes made to 'task_list'  to 'task.txt' in 'view_mine' function.
This way task.txt file is updated as the changes are made.
'''
def save_from_task_list():
    with open("tasks.txt", "w", encoding= "utf-8") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATE_STRING_FORMAT),
                t['assigned_date'].strftime(DATE_STRING_FORMAT),
                "Yes" if t['completed'] == True else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

''' Below function reads the task from 'task.txt' file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
'''
def view_all():
    print("\nList of all of the available tasks:\n")
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATE_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATE_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n{t['description']}\n"
        print(disp_str)

''' Below function Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
        
Addition to above:
    - This function now allows user to select specific task.
    - Mark task as completed by changing 'task_list[completed]' to True,
    which in turn changes the text to "Yes".
    - Allows user to edit task by changing username and due date.
'''
def view_mine():

    # Just incase the list is long and error message is not visible to user because of auto scroll.
    # 'Error_message' will hold error message from this iteration and print it near input of next iteration.
    error_message = ""

    while True:
        # Variables for printouts of list and menu that follows.
        # 'vm' is abbreviation for View_Mine
        vm_count_total = 0
        vm_count_completed = 0
        vm_user_sel = ""

        # To create relationship between the task user selects and index of selection in task_list.
        vm_task_index = {} # Task number that user to select : Task_list index of task number.
        vm_task_count = 0
        vm_task_list_id = -1
        for c_t in task_list:
            if c_t['username'] == curr_user:
                vm_count_total += 1
            if c_t['completed'] == True and c_t['username']== curr_user:
                vm_count_completed += 1
        
        # Returns user to main menu if non of the task are assigned to user.
        if vm_count_total == 0:
            print("\nThere are no tasks currently assigned to you.\n")
            break

        # Lets user know that all of the task are completed.
        elif vm_count_completed == vm_count_total:
            error_message += "\nAll of the tasks assigned to you are completed.\n"
        
        # Uses for loop and if statements to count various values.
        # Prints out the list of Task available to user. 
        print("\nComplete list of all of the tasks assigned to you:\n"
              +"- " * 35 +"\n")
        for t in task_list:
            vm_task_list_id += 1
            if t['username'] == curr_user:
                # Uploads detail in to vm_task_index
                vm_task_count += 1
                vm_task_index[vm_task_count] = vm_task_list_id

                # print list of task assigned to the user.
                # created a helper function to reduce code repetition below.
                def output_list():
                    vm_task_completed = "No" if t['completed'] == False else "Yes"
                    disp_str = f"{'Task ' + str(vm_task_count) + ' of ' + str(vm_count_total) + ':' :<17}"
                    disp_str += f"{t['title']}\n"
                    disp_str += f"Assigned to: \t {t['username']}\n"
                    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATE_STRING_FORMAT)}\n"
                    disp_str += f"Due Date: \t {t['due_date'].strftime(DATE_STRING_FORMAT)}\n"
                    disp_str += f"Completed: \t {vm_task_completed}\n"
                    disp_str += f"\nTask Description: \n{t['description']}\n"
                    disp_str += "-" * 70
                    print(disp_str)
                output_list()
        print("\033[1m"+ error_message + "\033[0m")

        # Request user input to select a task.
        try:
            vm_user_sel = int(input("Options for List of tasks above:\n"
                                +" - Enter Task number to make changes - e.g. '1' for Task 1.\n"
                                +" - Enter '-1' to return to main menu.\n"
                                +"\nPlease enter corresponding task number or '-1' to return to main menu:\n"))
        except ValueError:
            error_message = "Please only enter numbers, please try again.\n"
        except KeyboardInterrupt:
            error_message = "Applied keyboard entry not available during this request.\n"
        except EOFError:
            error_message = "Applied keyboard shortcut not available during this request.\n"
        if vm_user_sel == -1:
            break
        elif vm_user_sel not in vm_task_index.keys():
            error_message = "Your entry was not recognized. Please try again.\n"
            continue

        # Prints out the details of selected task, once the selection has been made \
        # using the help function output_list()
        while True:
            print("\nYou have selected Task " + str(vm_user_sel) + ".\n")
            t = task_list[vm_task_index[vm_user_sel]]
            output_list()
            
            # Request input from user giving option to edit and mark as completed.
            # If mark as completed is selected - changes 'task_list[completed]' to True.
            print("\nOptions for selected Task:\n"
                  +f"{'C':<5}{'to mark the task as completed'}\n"
                  +f"{'E':<5}{'to edit changes to the task'}\n")
            vm_sel_option = req_info("Please select and enter a letter from above menu:\n")
            if task_list[vm_task_index[vm_user_sel]]['completed'] == True:
                error_message = "\nBecause selected has is already completed, you cannot make changes to it.\n"
                error_message += "Please select a different task.\n"
                break
            elif vm_sel_option.lower() == "c":
                task_list[vm_task_index[vm_user_sel]]['completed'] = True
                error_message = "Previously selected task has now been marked as completed.\n"
                save_from_task_list()
                break

            # If edit task is selected, below block of code give additional Options for user to select from.
            elif vm_sel_option.lower() == "e":
                while True:
                    print("\nOptions for editing Task:\n"
                    +f"{'R':<5}{'to reassign to the task to another user. '}\n"
                    +f"{'D':<5}{'to change the due date.'}\n")
                    vm_edit_option = req_info("\nPlease select and enter a letter from above menu:\n")

                    # Below block of code allows user to change username in the dictionary 'Task_list'
                    # and updates the 'tasks.txt' using function 'save_from_task_list'
                    if vm_edit_option.lower() == "r":
                        while True:
                            t = task_list[vm_task_index[vm_user_sel]]
                            vm_edit_username = req_info("\nPlease enter the name from existing pool of users.\n")
                            if vm_edit_username == t['username']:
                                print("This task is already assigned to you\n")
                                break
                            elif vm_edit_username not in username_password.keys():
                                print("\n" + str(vm_edit_username) + "does not exit in the existing pool of users.\n")
                                continue
                            else:
                                task_list[vm_task_index[vm_user_sel]]['username'] = vm_edit_username
                                save_from_task_list()
                                error_message = "\nSelected username has been updated for previously selected task.\n"
                                error_message += "Therefore will not be visible in above list.\n"
                                break

                    # Below block of code allows user to change 'due_date' in the dictionary 'Task_list'
                    # and updates the 'tasks.txt' using function 'save_from_task_list'
                    elif vm_edit_option.lower() == "d":
                        while True:
                            try:
                                task_due_date = input("\nDue date of task (YYYY-MM-DD): ")
                                due_date_time = datetime.strptime(task_due_date, DATE_STRING_FORMAT)
                                break
                            except ValueError:
                                print("Invalid datetime format. Please use the format specified\n")
                            except EOFError:
                                print("Something went wrong, please try again.\n")
                            except KeyboardInterrupt:
                                print("Applied keyboard shortcut not available during this request.\n")
                        task_list[vm_task_index[vm_user_sel]]['due_date'] = due_date_time
                        save_from_task_list()
                        error_message = "Due date has been amended for previously selected task\n"
                    elif vm_edit_option.lower() != "r" and "d":
                        print("Invalid selection. Please try again.\n")
                        continue
                    break
                break
            elif vm_sel_option.lower() != "c" and "e":
                print("Invalid selection. Please try again.\n")
                continue

''' Below function take information from dictionary 'task_list', Uses for loops to count required information.
and records that information in to two dictionaries. Writes stats to 'task_overview.txt' and 'user_overview.txt' files. '''
def report():
    #'t_o_' is abbreviation for task_overview.
    t_o_completed = 0
    t_o_incomplete = 0
    t_o_over_due = 0

    # Using for Loop and if statements to do all the counting. 
    for t_o_i in task_list:
        if t_o_i['completed'] == True:
            t_o_completed += 1 
        if t_o_i['completed'] == False:
            t_o_incomplete += 1 
        if t_o_i['completed'] == False and t_o_i['due_date'] < datetime.today():
            t_o_over_due += 1
    
    # Below dictionary will hold stats in a organized manner. 
    t_o = {}
    t_o['total'] = t_o_completed + t_o_incomplete
    t_o['completed'] = t_o_completed
    t_o['uncompleted'] = t_o_incomplete
    t_o['over_due'] = t_o_over_due
    if t_o["total"] == 0: # To Avoid 'Zero Division error' in below code.
        t_o['p_incomplete'] = 0
        t_o['p_over_due'] = 0
    else:
        t_o['p_incomplete'] = t_o_incomplete / t_o['total'] * 100
        t_o['p_over_due'] = t_o_over_due / t_o['total'] * 100

    # Below code will write information from above 't_o' dictionary to 'Task_Overview.txt' file. 
    with open('task_overview.txt', 'w', encoding= "utf-8") as t_o_report:
        t_o_report.write("Overview of all of the task to date:\n\n")
        t_o_report.write(f"{'Total number task on record:':<46}")
        t_o_report.write(f"{t_o['total']}\n")
        t_o_report.write(f"{'Total number of completed tasks:':<46}")
        t_o_report.write(f"{t_o['completed']}\n")
        t_o_report.write(f"{'Total number of uncompleted task:':<46}")
        t_o_report.write(f"{t_o['uncompleted']}\n")
        t_o_report.write(f"{'Total number incomplete and overdue tasks:':<46}")
        t_o_report.write(f"{t_o['over_due']}\n")
        t_o_report.write(f"{'The percentage of tasks that are incomplete:':<46}")
        t_o_report.write(f"{t_o['p_incomplete']:.0f}{' %'}\n")
        t_o_report.write(f"{'The percentage of tasks that are overdue.:':<46}")
        t_o_report.write(f"{t_o['p_over_due']:.0f}{' %'}\n")

    # u_o is abbreviation for User_Overview. 
    # Below code with write overall stats for 'user_overview.txt'
    with open('user_overview.txt', 'w', encoding= "utf-8") as u_o_report:
        u_o_report.write("User overview report:\n\n")
        u_o_report.write(f"{'Total number registered user:':<40}{len(username_password.keys())}\n")
        u_o_report.write(f"{'Total number task on record:':<40}{t_o['total']}\n")
        u_o_report.write("- -" * 15 +  "\n\n")
        u_o_report.write("\nUser overview report per user:\n")
    u_o_report.close()

    # u_o is abbreviation for User Overview.
    # This dictionary will hold all the data in manner, that is easy to access accurately.
    u_o = {}
    # For loop to go through each user. 
    for u_o_user in username_password.keys():
        u_o[u_o_user] = {'total' : 0}
        u_o[u_o_user]['completed'] = 0
        u_o[u_o_user]['incomplete'] = 0
        u_o[u_o_user]['over_due'] = 0

        # Using for loop and If statement to do all of the counting \
        # and appending the information to 'user_overview.txt'.
        for u_o_i in task_list:
            if u_o_i['username'] == u_o_user:
                u_o[u_o_user]['total'] += 1
            if u_o_i['username'] == u_o_user and u_o_i['completed'] == True:
                u_o[u_o_user]['completed'] += 1
            if u_o_i['username'] == u_o_user and u_o_i['completed'] == False:
                u_o[u_o_user]['incomplete'] += 1
            if u_o_i['username'] == u_o_user \
            and u_o_i['due_date'] < datetime.today() \
            and u_o_i['completed'] == False:
                u_o[u_o_user]['over_due'] += 1
        if u_o[u_o_user]['total'] == 0: # To avoid 'Zero Division error' in below code.
            u_o[u_o_user]['p_total'] = 0
            u_o[u_o_user]['p_completed'] = 0
            u_o[u_o_user]['p_incomplete'] = 0
            u_o[u_o_user]['p_over_due'] = 0
        else:
            u_o[u_o_user]['p_total'] = u_o[u_o_user]['total'] / t_o['total'] * 100
            u_o[u_o_user]['p_completed'] = u_o[u_o_user]['completed'] / u_o[u_o_user]['total'] * 100
            u_o[u_o_user]['p_incomplete'] = u_o[u_o_user]['incomplete'] / u_o[u_o_user]['total'] * 100
            u_o[u_o_user]['p_over_due'] = u_o[u_o_user]['over_due'] / u_o[u_o_user]['total'] * 100

        # to add to the files -  below code will append the following to the user_overview.txt file. 
        with open('user_overview.txt', 'a', encoding= "utf-8") as u_o_report:
            u_o_report.write(f"{'For user '}{u_o_user}{':'}\n\n")

            u_o_report.write(f"{'Total number of task assigned to user:':50}")
            u_o_report.write(f"{u_o[u_o_user]['total']}\n")

            u_o_report.write(f"{'Total percentage of task assigned to user:':<50}")
            u_o_report.write(f"{u_o[u_o_user]['p_total']:.0f}{' %'}\n")

            u_o_report.write(f"{'Total percentage of completed task for user:':<50}")
            u_o_report.write(f"{u_o[u_o_user]['p_completed']:.0f}{' %'}\n")

            u_o_report.write(f"{'Total percentage of task user must complete:':<50}")
            u_o_report.write(f"{u_o[u_o_user]['p_incomplete']:.0f}{' %'}\n")
            
            u_o_report.write(f"{'Total percentage of task incomplete and overdue:':<50}")
            u_o_report.write(f"{u_o[u_o_user]['p_over_due']:.0f}{' %'}\n\n")
            u_o_report.write("-" * 60 +  "\n\n")

    with open('user_overview.txt', 'a', encoding= "utf-8") as u_o_report:
        u_o_report.write("----- End of Report -----")
    u_o_report.close()

    print("Please see 'Task_Overview.txt' and 'User_Overview.txt' for report")

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = req_info('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()    

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr'and curr_user == 'admin':
        report()               
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        
        if not os.path.exists("tasks.txt"):
            with open("tasks.txt", "w") as ds_task_file:
                pass
        with open("tasks.txt", 'r',  encoding= "utf-8") as ds_task_file:
            num_tasks = len(ds_task_file.read().split("\n"))
            ds_task_file.close()

        if not os.path.exists("user.txt"):
            with open("user.txt", "w", encoding= "utf-8") as ds_user_file:
                ds_user_file.write("admin;password")
        with open("user.txt", 'r', encoding= "utf-8") as ds_user_file:
            num_users = len(ds_user_file.read().split("\n"))
            ds_user_file.close()
            
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("\nYou have made a wrong choice, Please Try again\n")