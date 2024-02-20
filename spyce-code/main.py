from controller import Controller


def main():
    spyce_controller = Controller(config_path='./spyce-code/config/config.json') 
    print(spyce_controller)



if __name__=="__main__":
    main()