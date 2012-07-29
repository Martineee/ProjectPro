from tkinter import *
from tkinter import ttk

import sqlite3

class ProjectProGUI:
    def __init__(self, parent):
        """Initialiserer ProjectProGUI objekt"""
        
        #--- Parent window
        self.parent = parent
        self.parent.title('Projektoversigt - ProjectPro v1.1')
        
        #--- Mainframe
        self.mainframe = ttk.Frame(parent)
        self.mainframe.grid(column = 0, row = 0)

        #--- Frame til projekt ideer delen
        self.idearsFrame = ttk.Labelframe(self.mainframe, text='Projektideer')
        self.idearsFrame.grid(column = 0, row = 0)

        #--- Frame til selve ideerne
        self.idearListFrame = ttk.Frame(self.idearsFrame)
        self.idearListFrame.grid(column = 0, row = 0)

        projects = getProjectsList()
        self.framesNContent = {'frames': [], 'entrys': [], 'labels': [],
                               'priority': [index for index in range(len(projects))]}
        self.idearnames = []
        self.idearChecks = []
        #rowNum = 0

        self.showIdears(projects)

        """for row in projects:  # make append able to reuse this
            self.idearnames.append(StringVar())
            self.idearnames[-1].set(row[1])
            self.idearChecks.append(StringVar())
            self.idearChecks[-1].set('0')

            self.framesNContent['frames'].append(ttk.Frame(self.idearListFrame))
            self.framesNContent['frames'][-1].grid(column = 0, row = rowNum)
            
            self.framesNContent['entrys'].append(ttk.Entry(self.framesNContent['frames'][-1], width = 25, textvariable = self.idearnames[rowNum]))
            self.framesNContent['entrys'][-1].grid(column = 0, row = 0)
            self.framesNContent['entrys'][-1].grid_remove()

            self.framesNContent['labels'].append(ttk.Label(self.framesNContent['frames'][-1], width = 25, textvariable = self.idearnames[rowNum]))
            self.framesNContent['labels'][-1].grid(column = 0, row = 0)

            self.framesNContent['entrys'][-1].bind("<Return>", lambda event, rowNum = rowNum: self.editLabel(event.widget, self.framesNContent['labels'][rowNum]))
            self.framesNContent['labels'][-1].bind("<Button-1>", lambda event, rowNum = rowNum: self.editLabel(event.widget, self.framesNContent['entrys'][rowNum]))

            ttk.Checkbutton(self.framesNContent['frames'][-1], variable = self.idearChecks[rowNum]).grid(column = 1, row = 0)

            rowNum += 1"""
            
        """#--- TEST: Husk menu (arbejder på ændring til mere åbenlys mulighed en højreklik)
        menu = Menu(self.idearsFrame)
        for i in ('One', 'Two', 'Three'):

            menu.add_command(label=i)
        self.testLabel.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))"""

        #--- Frame til prioriteringknapper
        self.idearsPrioPanel = ttk.Frame(self.idearsFrame, borderwidth = 5)
        self.idearsPrioPanel.grid(column = 1, row = 0)

        #--- Prioriteringsknapper og label
        ttk.Button(self.idearsPrioPanel, text = "^\n  \\", width = 5, command = lambda: self.prioriter(direction = -1)).grid(column = 0, row = 0, sticky = "w")
        ttk.Label(self.idearsPrioPanel, text = "Prioriter\nop eller\nned").grid(column = 0, row = 1, sticky = "w")
        ttk.Button(self.idearsPrioPanel, text = "  /\nv", width = 5, command = lambda: self.prioriter(direction = 1)).grid(column = 0, row = 2, sticky = "w")
        
        #--- Frame til knap panel
        self.idearsButtonPanel = ttk.Frame(self.idearsFrame, borderwidth = 5)
        self.idearsButtonPanel.grid(column = 0, row = 1, sticky = "e")

        #--- Forbered, tilføj og slet knap
        self.idearsPrepareButton = ttk.Button(self.idearsButtonPanel, text = "Forbered valgt ide")
        self.idearsPrepareButton.grid(column = 0, row = 0, sticky = "e")
        self.idearsAppendButton = ttk.Button(self.idearsButtonPanel, text = "Tilføj ny ide", command = self.appendIdear)
        self.idearsAppendButton.grid(column = 1, row = 0, sticky = "e")
        self.idearsRemoveButton = ttk.Button(self.idearsButtonPanel, text = "Slet valgte ideer")
        self.idearsRemoveButton.grid(column = 2, row = 0, sticky = "e")

		
		
    def showIdears(self, *projects, rowNum = 0): # Kommet til
        for row in projects:  # make append able to reuse this
            self.idearnames.append(StringVar())
            self.idearnames[-1].set(row[1])
            self.idearChecks.append(StringVar())
            self.idearChecks[-1].set('0')

            self.framesNContent['frames'].append(ttk.Frame(self.idearListFrame))
            self.framesNContent['frames'][-1].grid(column = 0, row = rowNum)
            
            self.framesNContent['entrys'].append(ttk.Entry(self.framesNContent['frames'][-1], width = 25, textvariable = self.idearnames[rowNum]))
            self.framesNContent['entrys'][-1].grid(column = 0, row = 0)
            self.framesNContent['entrys'][-1].grid_remove()

            self.framesNContent['labels'].append(ttk.Label(self.framesNContent['frames'][-1], width = 25, textvariable = self.idearnames[rowNum]))
            self.framesNContent['labels'][-1].grid(column = 0, row = 0)

            self.framesNContent['entrys'][-1].bind("<Return>", lambda event, rowNum = rowNum: self.editLabel(event.widget, self.framesNContent['labels'][rowNum]))
            self.framesNContent['labels'][-1].bind("<Button-1>", lambda event, rowNum = rowNum: self.editLabel(event.widget, self.framesNContent['entrys'][rowNum]))

            ttk.Checkbutton(self.framesNContent['frames'][-1], variable = self.idearChecks[rowNum]).grid(column = 1, row = 0)

            rowNum += 1

			
			
    def saveNameChange(self, toRemove, toGrid):
        raise Exception('TODO: Implement saveNameChange')


		
    def editLabel(self, toRemove, toGrid):
        toRemove.configure(state = 'disabled')
        toRemove.grid_remove()
        toGrid.grid()
        toGrid.configure(state = 'normal')
        for idearName in self.idearnames:
            print(idearName.get())

			
			
    def prioriter(self, event = None, *, direction): # op
        for checkStatus in self.idearChecks:
            if checkStatus.get() == '1':
                nr = self.idearChecks.index(checkStatus)
                prioritet = self.framesNContent['priority'][nr]
                try:
                    bytMedNr = self.framesNContent['priority'].index(prioritet + direction)
                except ValueError:
                    return None
                break
        #byt om på skærmen
        frame1Col = self.framesNContent['frames'][nr].grid_info()['column']
        frame1Row = self.framesNContent['frames'][nr].grid_info()['row']
        frame2Col = self.framesNContent['frames'][bytMedNr].grid_info()['column']
        frame2Row = self.framesNContent['frames'][bytMedNr].grid_info()['row']
        self.framesNContent['frames'][nr].grid_remove()
        self.framesNContent['frames'][bytMedNr].grid_remove()
        self.framesNContent['frames'][nr].grid(column = int(frame2Col), row = int(frame2Row))
        self.framesNContent['frames'][bytMedNr].grid(column = int(frame1Col), row = int(frame1Row))
        #byt om i frame listen
        self.framesNContent['priority'][nr], self.framesNContent['priority'][bytMedNr] = self.framesNContent['priority'][bytMedNr], self.framesNContent['priority'][nr]
        #byt om i databasen
        showProjectsTabel()
        print("Hvor navnet er", self.idearnames[nr], "skiftes til", self.framesNContent['priority'][nr])
        print("Hvor navnet er", self.idearnames[bytMedNr], "skiftes til", self.framesNContent['priority'][bytMedNr])
        cur.execute("UPDATE Projects SET Priority = '%s' WHERE Name = '%s'" % (self.framesNContent['priority'][bytMedNr], self.idearnames[bytMedNr].get()))
        cur.execute("UPDATE Projects SET Priority = '%s' WHERE Name = '%s'" % (self.framesNContent['priority'][nr], self.idearnames[nr].get()))
        showProjectsTabel()

		
		
    def appendIdear(self, event = None):
        """Tilføjer ide til projektoversigt"""
        tWin = Toplevel(self.parent)
        nWindow = AppendIdearWindow(tWin)
        tWin.mainloop()

        

class AppendIdearWindow:
    def __init__(self, parent):
        """Initialiserer AppendIdearWindow objekt"""

        #--- Parent window
        self.parent = parent
        self.parent.title('Tilføj ny projektide')

        #--- Settings
        labelLength = 12

        #--- Mainframe
        self.mainframe = ttk.Frame(self.parent)
        self.mainframe.grid(column = 0, row = 0, columnspan = 1, rowspan = 3, padx = 10, pady = 7)

        #--- Frame til projektnavn og filadresse
        self.requiredframe = ttk.Frame(self.mainframe)
        self.requiredframe.grid(column = 0, row = 0, pady = 10)

        #--- Navn label samt entry
        self.nNameLabel = ttk.Label(self.requiredframe, text = "Navn: ", width = labelLength)
        self.nNameLabel.grid(column = 0, row = 0, sticky = "w", pady = 2)

        self.nName = StringVar()
        self.nNameEntry = ttk.Entry(self.requiredframe, width = 25, textvariable = self.nName)
        self.nNameEntry.grid(column = 1, row = 0, pady = 2)

        #--- Filadresse label samt entry
        self.nFiladdLabel = ttk.Label(self.requiredframe, text = "Filaddresse: ", width = labelLength)
        self.nFiladdLabel.grid(column = 0, row = 1, sticky = "w", pady = 2)

        self.nFiladd = StringVar()
        self.nFiladdEntry = ttk.Entry(self.requiredframe, width = 25, textvariable = self.nFiladd)
        self.nFiladdEntry.grid(column = 1, row = 1, pady = 2)

        #--- Frame til evt. husk
        self.rememberframe = ttk.Labelframe(self.mainframe, text = "Husk (valgfrit)")
        self.rememberframe.grid(column = 0, row = 1, sticky = "we", pady = 5)

        #--- Opg label samt entry
        self.huskOpgLabel = ttk.Label(self.rememberframe, text = "Opgave: ", width = labelLength)
        self.huskOpgLabel.grid(column = 0, row = 0, sticky = "w", pady = 2)

        self.nHuskOpg = StringVar()
        self.nHuskOpgEntry = ttk.Entry(self.rememberframe, width = 25, textvariable = self.nHuskOpg)
        self.nHuskOpgEntry.grid(column = 1, row = 0, columnspan = 5, pady = 2)

        # Deadline label
        self.huskFristLabel = ttk.Label(self.rememberframe, text = "Frist: ")
        self.huskFristLabel.grid(column = 0, row = 1, sticky = "w", pady = 2)

        # Deadline frame
        self.fristFrame = ttk.Frame(self.rememberframe)
        self.fristFrame.grid(column = 1, row = 1, pady = 2, sticky = "w")

        # Deadline entries
        self.nHuskFristDate, self.nHuskFristMonth, self.nHuskFristYear = StringVar(), StringVar(), StringVar()
        
        self.nHuskFristEntryD = ttk.Entry(self.fristFrame, width = 2, textvariable = self.nHuskFristDate)
        self.nHuskFristEntryD.grid(column = 0, row = 0)

        self.slash = ttk.Label(self.fristFrame, width = 1, text = "/")
        self.slash.grid(column = 1, row = 0)        
        
        self.nHuskFristEntryM = ttk.Entry(self.fristFrame, width = 2, textvariable = self.nHuskFristMonth)
        self.nHuskFristEntryM.grid(column = 2, row = 0)

        self.slash2 = ttk.Label(self.fristFrame, width = 1, text = "/")
        self.slash2.grid(column = 3, row = 0)
        
        self.nHuskFristEntryY = ttk.Entry(self.fristFrame, width = 2, textvariable = self.nHuskFristDate)
        self.nHuskFristEntryY.grid(column = 4, row = 0)

        # Button frame
        self.buttonPanel = ttk.Frame(self.mainframe)
        self.buttonPanel.grid(column = 0, row = 2, pady = 7)

        # Add button
        self.append = ttk.Button(self.buttonPanel, text = "Tilføj", command = self.append)
        self.append.grid(column = 0, row = 0, padx = 7)
		
		# Cancel button
        self.cancel = ttk.Button(self.buttonPanel, text = "Annuler", command = self.close)
        self.cancel.grid(column = 1, row = 0, padx = 7)

		
		
    def append(self):
        cur.execute("SELECT Priority FROM Projects ORDER BY Priority ASC")
        rows = cur.fetchall()
        if rows:
            priority = rows[-1][0] + 1
        else:
            priority = 0
        cur.execute("INSERT INTO Projects (Name, Dataaddress, Stage, Priority) VALUES('%s', '%s', 0, '%s')" % (self.nName.get(), self.nFiladd.get(), priority))

        showProjectsTabel()
        # Kommet til
        mainWindow.idearnames.append(self.nName)
        mainWindow.idearChecks.append(StringVar())
        mainWindow.idearChecks[-1].set('0')

        mainWindow.framesNContent['frames'].append(ttk.Frame(mainWindow.idearListFrame))
        mainWindow.framesNContent['frames'][-1].grid(column = 0, row = priority)
            
        mainWindow.framesNContent['entrys'].append(ttk.Entry(mainWindow.framesNContent['frames'][-1], width = 25, textvariable = mainWindow.idearnames[priority]))
        mainWindow.framesNContent['entrys'][-1].grid(column = 0, row = 0)
        mainWindow.framesNContent['entrys'][-1].grid_remove()

        mainWindow.framesNContent['labels'].append(ttk.Label(mainWindow.framesNContent['frames'][-1], width = 25, textvariable = mainWindow.idearnames[priority]))
        mainWindow.framesNContent['labels'][-1].grid(column = 0, row = 0)

        mainWindow.framesNContent['entrys'][-1].bind("<Return>", lambda event, rowNum = priority: mainWindow.editLabel(event.widget, mainWindow.framesNContent['labels'][priority]))
        mainWindow.framesNContent['labels'][-1].bind("<Button-1>", lambda event, rowNum = priority: mainWindow.editLabel(event.widget, mainWindow.framesNContent['entrys'][priority]))

        ttk.Checkbutton(mainWindow.framesNContent['frames'][-1], variable = mainWindow.idearChecks[priority]).grid(column = 1, row = 0)

        mainWindow.framesNContent['priority'].append(priority)
                
        self.close()

		
		
    def close(self):
        self.parent.destroy()


def createDatabase():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cur.fetchall()
    if not rows:
        cur.execute("CREATE TABLE Projects(ID INTEGER PRIMARY KEY, Name VARCHAR, Dataaddress VARCHAR, Stage INT, Priority INT)")
        cur.execute("CREATE TABLE Reminders(ID INTEGER PRIMARY KEY, ProjectID INT, Name VARCHAR, Deadline1 DATETIME NOT NULL, Deadline2 DATETIME NOT NULL)")


		
def showProjectsTabel():
    for row in getProjectsList():
        print(row)
    print("------------------------------\n")


	
def getProjectsList():
    cur.execute("SELECT * FROM Projects ORDER BY Priority ASC")
    return cur.fetchall()
    


# Establish database connection
con = sqlite3.connect('ProjectPro.db')

with con:
    cur = con.cursor()
    createDatabase()
    root = Tk()
    mainWindow = ProjectProGUI(root)
    root.mainloop()
