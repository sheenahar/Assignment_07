#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# SHarms, 2022-Nov-18, Edited file
# SHARMS, 2022-Nov 27, Edited to add exception handling
#------------------------------------------#
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'pickle1.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def del_Row(intIDDel, lstTbl):
        """Function to remove files from table
        Reads through rows for the input ID
        Deletes row if input ID is found
        Returns:
            None"""
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
            blnCDRemoved = True
            break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
    
    @staticmethod 
    def add_cd(strID, strTitle, strArtist, lstTbl):
        """Function adds data to dictionary row
        Appends to list
        Returns:
            None."""
        try:
            intID = int(strID)
        except ValueError:
            print("\nYou did not enter a numeric ID. The entry was cancelled.\n")
        else:
            dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
            lstTbl.append(dicRow)

class FileProcessor:
    """Processing the data to and from binary file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            objFile = open(file_name, 'rb')
            table.clear()
            data = pickle.load(objFile)
            for row in data:
                table.append(row)
            #print(table)
        except:
            print("Before you begin, the runfile is missing. Locate it if you want to load or save inventory.")
        else:
            objFile.close()

    @staticmethod
    def write_file(strfileName, lstTbl):
        """Writes from list of dicts to a binary file.
        Args:
            strfileName: file name
            lstTbl: list of lists
        Returns:
            None"""
        objFile = open(strFileName, 'wb')
        pickle.dump(lstTbl, objFile)
        objFile.close()

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user
        Args:
            None.
        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection
        Args:
            None.
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def cd_Data():
        """Asks user for cd data inputs
        Args:
            None.
        Returns:
            None.
            """
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        DataProcessor.add_cd(strID, strTitle, strArtist, lstTbl)
        IO.show_inventory(lstTbl)
        
    @staticmethod
    def del_Choice():
        """Asking user what they want to delete from the inventory.
        Args:
            None.
        Returns:
            None.
            """
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError:
            print("That is not a numeric ID.")
        except:
            print("There was an error. Please begin again")
        # 3.5.2 search thru table and delete CD
        else:
            DataProcessor.del_Row(intIDDel, lstTbl)
            IO.show_inventory(lstTbl)
            
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.3 process add a CD
    elif strChoice == 'a':
        IO.cd_Data()
        continue  # start loop back at top.
        
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        IO.del_Choice()
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
                FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
            continue  # start loop back at top.
        
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')

