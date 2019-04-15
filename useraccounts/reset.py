'''
This script to reset migrations and delete database for this project.
NOTE: This file must placed into the django project folder
'''
import os, shutil, glob
# Stopping paramter
check=True
# loop for input corection
while check==True:
    # check whether user want to continue or not
    print('This will delete all migraions include your database.')
    con = input('Do you want to continue [y/n]:')
    # alaysis the answer
    if con=='n':
        # quit
        print('Thank you or using reset script.')
        check=False
    elif con=='y':
        # get the project path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # get a list of all files and folders the project contains
        content = os.listdir(BASE_DIR)
        # create a new list for folders only
        dirs=list()
        # filter the list of all content to get the folders only
        for dir in content:
            if os.path.isdir(os.path.join(BASE_DIR, dir)):
                dirs.append(dir)
        # clean up all folders
        for dir in dirs:
            # clean __pycache__ in all folders
            try:
                shutil.rmtree(dir+'/'+'__pycache__')
                print("Folder __pycache__ in "+ dir + ' has been removed!')
            except:
                pass
            # clean __pycache__ in all migrations folders
            try:
                shutil.rmtree(dir+'/'+'migrations'+'/'+'__pycache__')
                print("Folder __pycache__ in "+ dir + ' /migations has been removed!')
            except:
                pass
            #delete all migrations files except __init__.py
            try:
                FolderPath=os.path.join(BASE_DIR,dir,'migrations')
                FolderContent=os.listdir(FolderPath)
                for file in FolderContent:
                    if not file=='__init__.py':
                        os.remove(os.path.join(FolderPath,file))
                        print(FolderPath+file+' has been removed')
            except:
                pass
            # delete .sqlite3 file
            try:
                for file in glob.glob("*.sqlite3"):
                    os.remove(file)
                    print(file+' has been removed')
            except:
                pass
        print('\nYour project has been reset.\nPlease migrate again before use.')
        check=False
    else:
        print("Invalid input. please input 'y' or 'n'.\n")
quit()
