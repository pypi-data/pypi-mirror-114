import click


class TochCli(object):

    
    def __test(self):
        print ("test")
    
@click.command()
def configure():
    apikey = input("Enter api key:: ")
    print ("Api key saved")



def main():
    #configure()
    pass


if __name__ == "__main__":
    print("Wellcome to tochCLI version 0.1.0")
    
    main()
    


