import fire


class TochCli(object):

    def configure(self):
        apikey = input("Enter api key:: ")
        #self.__test()
        print ("Api key saved")

    
    
    def __test(self):
        print ("test")
    

def main():
    
    fire.Fire(TochCli)


if __name__ == "__main__":
    print("Wellcome to tochCLI version 0.1.0")
    main()
    


