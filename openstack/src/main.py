import sys




config_file_name = "/Users/debobrotodasrobin/Google Drive/kent univ/spring_2018/cloud_infra/term_project_open_stack/openstack/gcp_resources/config_scripts/local.config"
default_machine_name = ""
user_choice_list = ["1. Enter config file: ", 
                    "2. Enter machine name to connect: ",
                    "3. Exit "]

def main():
    
    infra = None

    while (True):
        print(user_choice_list)
        user_input = input()
        input_as_list = user_input.split(' ')
        if input_as_list[0] == "1":
            config_file_name = input()
        elif input_as_list[0] == "2" :
            default_machine_name = input()
        elif input_as_list[0] == "3":
            print("Exiting program!!")
            sys.exit(0)
        else:
            print("Invalid choice!! Select 1,2,3, etc.. Try again!!!")
            



main()