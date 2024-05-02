import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
from Employee import EmployeeGUI
from Event import EventGUI
from Client import ClientGUI
from Suppliers import SupplierGUI
from GuestVenue import GuestGUI, VenueGUI


class MainApplication:
    """
    Main application class responsible for initializing and organizing the GUI components
    """
    def __init__(self, root):
        """
        Initialize the main application
        - root window of the application
        """
        self.root = root
        self.root.title("Management System") # Set the title of the window
        self.data_manager = DataManager() # Initialize the DataManager instance

        # Create a Notebook widget for organizing tabs
        self.tab_control = ttk.Notebook(root)

        # Create tabs for different functionalities
        self.employee_tab = ttk.Frame(self.tab_control)
        self.event_tab = ttk.Frame(self.tab_control)
        self.client_tab = ttk.Frame(self.tab_control)
        self.supplier_tab = ttk.Frame(self.tab_control)
        self.guest_tab = ttk.Frame(self.tab_control)
        self.venue_tab = ttk.Frame(self.tab_control)

        # Add tabs to the Notebook
        self.tab_control.add(self.employee_tab, text='Employees')
        self.tab_control.add(self.event_tab, text='Events')
        self.tab_control.add(self.client_tab, text='Clients')
        self.tab_control.add(self.supplier_tab, text='Suppliers')
        self.tab_control.add(self.guest_tab, text='Guests')
        self.tab_control.add(self.venue_tab, text='Venues')

        # Initialize GUI components for each tab
        self.employee_gui = EmployeeGUI(self.employee_tab, self.data_manager)
        self.event_gui = EventGUI(self.event_tab, self.data_manager)
        self.client_gui = ClientGUI(self.client_tab, self.data_manager)
        self.supplier_gui = SupplierGUI(self.supplier_tab, self.data_manager)
        self.guest_gui = GuestGUI(self.guest_tab, self.data_manager)
        self.venue_gui = VenueGUI(self.venue_tab, self.data_manager)

        self.tab_control.pack(expand=1, fill="both") #pack the Notebook widget


if __name__ == "__main__":
    root = tk.Tk() #create the root window
    app = MainApplication(root) #instance of the MainApplication class
    root.mainloop() #event loop
