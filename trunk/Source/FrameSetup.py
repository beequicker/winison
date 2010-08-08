#Boa:Frame:frameSetup

import wx
import os
import glob
import win32com.client
import platform
import shutil

def create(parent):
    return frameSetup(parent)

[wxID_FRAMESETUP, wxID_FRAMESETUPBUTTONBROWSE1, wxID_FRAMESETUPBUTTONBROWSE2,
 wxID_FRAMESETUPBUTTONDELETE, wxID_FRAMESETUPBUTTONGO,
 wxID_FRAMESETUPBUTTONLOAD, wxID_FRAMESETUPBUTTONSAVE,
 wxID_FRAMESETUPCHECKBOXINTERACTIVE, wxID_FRAMESETUPCHECKBOXQUIT,
 wxID_FRAMESETUPCOMBOBOXPROFILES, wxID_FRAMESETUPGAUGESAVED,
 wxID_FRAMESETUPSTATICTEXT1, wxID_FRAMESETUPSTATICTEXT2,
 wxID_FRAMESETUPSTATICTEXT3, wxID_FRAMESETUPTEXTOPTIONS,
 wxID_FRAMESETUPTEXTROOT1, wxID_FRAMESETUPTEXTROOT2,
] = [wx.NewId() for _init_ctrls in range(17)]

class frameSetup(wx.Frame):

    # paths assembled in LoadUp
    dot_unison      = None
    sendto          = None
    parent          = None
    loaded_prf_name = None

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMESETUP, name='frameSetup',
              parent=prnt, pos=wx.Point(294, 131), size=wx.Size(428, 465),
              style=wx.DEFAULT_FRAME_STYLE, title='Winison')
        self.SetClientSize(wx.Size(420, 431))
        self.SetBackgroundColour(wx.Colour(234, 234, 238))
        self.SetToolTipString('')
        self.Bind(wx.EVT_CLOSE, self.OnFrameSetupClose)

        self.buttonSave = wx.Button(id=wxID_FRAMESETUPBUTTONSAVE, label='Save',
              name='buttonSave', parent=self, pos=wx.Point(91, 31),
              size=wx.Size(48, 23), style=0)
        self.buttonSave.SetToolTipString('Save the data from below into the selected profile (or type a new name).')
        self.buttonSave.Bind(wx.EVT_BUTTON, self.OnButtonSave,
              id=wxID_FRAMESETUPBUTTONSAVE)

        self.buttonDelete = wx.Button(id=wxID_FRAMESETUPBUTTONDELETE,
              label='Delete', name='buttonDelete', parent=self,
              pos=wx.Point(141, 31), size=wx.Size(48, 23), style=0)
        self.buttonDelete.SetToolTipString('Delete selected profile.')
        self.buttonDelete.Bind(wx.EVT_BUTTON, self.OnButtonDelete,
              id=wxID_FRAMESETUPBUTTONDELETE)

        self.staticText1 = wx.StaticText(id=wxID_FRAMESETUPSTATICTEXT1,
              label='Local Root', name='staticText1', parent=self,
              pos=wx.Point(8, 71), size=wx.Size(50, 13), style=0)
        self.staticText1.SetToolTipString('')

        self.staticText2 = wx.StaticText(id=wxID_FRAMESETUPSTATICTEXT2,
              label='Remote Root', name='staticText2', parent=self,
              pos=wx.Point(8, 94), size=wx.Size(63, 13), style=0)
        self.staticText2.SetToolTipString('')

        self.textRoot1 = wx.TextCtrl(id=wxID_FRAMESETUPTEXTROOT1,
              name='textRoot1', parent=self, pos=wx.Point(80, 67),
              size=wx.Size(272, 21), style=0, value='')
        self.textRoot1.SetToolTipString('Path to the "local" root.')
        self.textRoot1.Bind(wx.EVT_TEXT, self.OnParameterChange,
              id=wxID_FRAMESETUPTEXTROOT1)

        self.textRoot2 = wx.TextCtrl(id=wxID_FRAMESETUPTEXTROOT2,
              name='textRoot2', parent=self, pos=wx.Point(80, 91),
              size=wx.Size(272, 21), style=0, value='')
        self.textRoot2.SetToolTipString('Path to the "remote" root.')
        self.textRoot2.Bind(wx.EVT_TEXT, self.OnParameterChange,
              id=wxID_FRAMESETUPTEXTROOT2)

        self.buttonBrowse1 = wx.Button(id=wxID_FRAMESETUPBUTTONBROWSE1,
              label='Browse', name='buttonBrowse1', parent=self,
              pos=wx.Point(355, 66), size=wx.Size(58, 23), style=0)
        self.buttonBrowse1.SetToolTipString('')
        self.buttonBrowse1.Bind(wx.EVT_BUTTON, self.OnButtonBrowse1,
              id=wxID_FRAMESETUPBUTTONBROWSE1)

        self.buttonBrowse2 = wx.Button(id=wxID_FRAMESETUPBUTTONBROWSE2,
              label='Browse', name='buttonBrowse2', parent=self,
              pos=wx.Point(355, 90), size=wx.Size(58, 23), style=0)
        self.buttonBrowse2.Bind(wx.EVT_BUTTON, self.OnButtonBrowse2,
              id=wxID_FRAMESETUPBUTTONBROWSE2)

        self.textOptions = wx.TextCtrl(id=wxID_FRAMESETUPTEXTOPTIONS,
              name='textOptions', parent=self, pos=wx.Point(8, 115),
              size=wx.Size(404, 309), style=wx.TE_MULTILINE | wx.HSCROLL,
              value='')
        self.textOptions.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Courier New'))
        self.textOptions.SetToolTipString('Additional Unison options.')
        self.textOptions.Bind(wx.EVT_TEXT, self.OnParameterChange,
              id=wxID_FRAMESETUPTEXTOPTIONS)

        self.comboBoxProfiles = wx.ComboBox(choices=[],
              id=wxID_FRAMESETUPCOMBOBOXPROFILES, name='comboBoxProfiles',
              parent=self, pos=wx.Point(42, 8), size=wx.Size(146, 21), style=0,
              value='')
        self.comboBoxProfiles.SetLabel('')
        self.comboBoxProfiles.SetToolTipString('Select a profile')
        self.comboBoxProfiles.Bind(wx.EVT_COMBOBOX, self.OnComboBoxProfiles,
              id=wxID_FRAMESETUPCOMBOBOXPROFILES)
        self.comboBoxProfiles.Bind(wx.EVT_TEXT, self.OnProfileKey,
              id=wxID_FRAMESETUPCOMBOBOXPROFILES)


        self.staticText3 = wx.StaticText(id=wxID_FRAMESETUPSTATICTEXT3,
              label='Profile', name='staticText3', parent=self, pos=wx.Point(8,
              13), size=wx.Size(30, 13), style=0)
        self.staticText3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        self.staticText3.SetToolTipString('')

        self.buttonLoad = wx.Button(id=wxID_FRAMESETUPBUTTONLOAD, label='Load',
              name='buttonLoad', parent=self, pos=wx.Point(41, 31),
              size=wx.Size(48, 23), style=0)
        self.buttonLoad.SetToolTipString('Load the selected profile.')
        self.buttonLoad.Bind(wx.EVT_BUTTON, self.OnButtonLoad,
              id=wxID_FRAMESETUPBUTTONLOAD)

        self.buttonGo = wx.Button(id=wxID_FRAMESETUPBUTTONGO, label='Go',
              name='buttonGo', parent=self, pos=wx.Point(191, 8),
              size=wx.Size(64, 46), style=0)
        self.buttonGo.SetToolTipString('Execute selected profile.')
        self.buttonGo.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Courier New'))
        self.buttonGo.SetBackgroundColour(wx.Colour(1, 150, 117))
        self.buttonGo.SetForegroundColour(wx.Colour(255, 255, 255))
        self.buttonGo.Bind(wx.EVT_BUTTON, self.OnButtonGo,
              id=wxID_FRAMESETUPBUTTONGO)

        self.checkBoxInteractive = wx.CheckBox(id=wxID_FRAMESETUPCHECKBOXINTERACTIVE,
              label='Interactive', name='checkBoxInteractive', parent=self,
              pos=wx.Point(257, 9), size=wx.Size(70, 13), style=0)
        self.checkBoxInteractive.SetValue(True)
        self.checkBoxInteractive.SetToolTipString('Check this if you want an interactive Unison sync (as opposed to automatically accepting changes)')

        self.checkBoxQuit = wx.CheckBox(id=wxID_FRAMESETUPCHECKBOXQUIT,
              label='Quit after launching', name='checkBoxQuit', parent=self,
              pos=wx.Point(257, 25), size=wx.Size(129, 13), style=0)
        self.checkBoxQuit.SetValue(True)
        self.checkBoxQuit.SetToolTipString('Check this if you want to shut down Winison when you press "Go"')

        self.gaugeSaved = wx.Gauge(id=wxID_FRAMESETUPGAUGESAVED,
              name='gaugeSaved', parent=self, pos=wx.Point(257, 41), range=7,
              size=wx.Size(155, 12), style=wx.GA_HORIZONTAL)
        self.gaugeSaved.SetToolTipString('This gauge shows whether the profile parameters shown below are saved to the selected profile.')

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.parent = parent

        # scan the system for the various profiles
        if self.LoadUp() == False: return




    def ClearGUI(self):
        """
        Clears out the GUI.
        """
        self.comboBoxProfiles.Clear()
        self.textRoot1.Clear()
        self.textRoot2.Clear()
        self.textOptions.Clear()

    def Error(self, s):
        """
        Clears all the GUI stuff out and displays an error in the
        preferences box.
        """
        print s
        self.ClearGUI()
        self.textOptions.SetValue(s)

    def PrfPathToName(self, prf_path):
        """
        Converts ...\\...\\*.prf to *
        """
        return os.path.split(prf_path)[-1].replace(".prf","")

    def PrfNameToPath(self, prf_name):
        """
        Converts profile name to a path.
        """
        return os.path.join(os.environ['HOMEDRIVE'],
                            os.environ['HOMEPATH'],
                            ".unison",
                            prf_name+".prf")

    def CreateShortcut(self, target, startin, path):
        """
        Creates a link to the specified target with startin directory. Saves
        the link to path
        """
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath =       target
        shortcut.WorkingDirectory = startin
        shortcut.save()

    def RemoveFile(self, path):
        """
        Tries to safely remove the file.
        """
        if os.path.exists(path): os.remove(path)


    def LoadUp(self):
        """
        This routine scans the user directory and the current directory for
        the various profile files of Unison, creates directories if they don't
        exist, and so forth. It clears out the GUI and repopulates it.
        """

        # clear out the GUI
        self.ClearGUI()

        # First see if the important directories exist!

        # User/.unison
        if not os.environ.has_key("HOMEDRIVE") or not os.environ.has_key("HOMEPATH"):
            self.Error("No HOMEDRIVE or HOMEPATH environment variable!\n\n"+str(os.environ.keys()))
            return False
        self.dot_unison = os.path.join(os.environ["HOMEDRIVE"],os.environ["HOMEPATH"],".unison")
        if not os.path.exists(self.dot_unison): os.mkdir(self.dot_unison)

        # User/SendTo
        if platform.release() in ['post2008Server']:
            # windows 7 or something similar!
            self.sendto = os.path.join(os.environ['APPDATA'],'Microsoft','Windows','SendTo')
            start_menu  = os.path.join(os.environ['APPDATA'],'Microsoft','Windows','Start Menu', 'Programs')
        else:
            # assume it's XP
            self.sendto = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "SendTo")
            start_menu  = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "Start Menu", "Programs")

        if not os.path.exists(self.sendto):
            self.Error("Path "+self.sendto+" does not exist! This is really weird.")
            return False

        # search for *.prf files
        prf_paths = glob.glob(os.path.join(self.dot_unison,"*.prf"))

        # populate the combo box
        for p in prf_paths:
            # get the name of the prefs and append it
            prf_name = self.PrfPathToName(p)
            self.comboBoxProfiles.Append(prf_name)



        # now load the preferences file.
        if os.path.exists("winison.cfg"):
            f = open("winison.cfg","r")
            lines = f.readlines()
            f.close()
            for line in lines:
                s = line.split("\t")
                if len(s)==2:
                    key = s[0].strip()
                    value = s[1].strip()
                    try:    exec("self."+key+".SetValue("+value+")")
                    except: print "Could not '"+"self."+key+".SetValue("+value+")'."

            # load whatever profile is selected
            self.OnButtonLoad(None)

        # if the prefs file doesn't exist, this is the first run.
        else:
            if wx.MessageBox("This appears to be the first time you've run Winison. Would you like a link to be added to the start menu?", "Add Winison to start menu?", wx.YES|wx.NO) == wx.YES:
                self.CreateShortcut(os.path.join(os.getcwdu(), "winison.exe"), os.getcwdu(), os.path.join(start_menu, "Winison.lnk"))

        # Look for a unison.exe.
        if not os.path.exists("unison.exe"):
            shutil.copy("my_version_of_unison", "unison.exe")



##################################
## EVENTS
##################################


    def OnButtonLoad(self, event):
        """
        Loads up all the settings associated with the selected Profile name.
        """
        self.textRoot1.Clear()
        self.textRoot2.Clear()
        self.textOptions.Clear()

        # Find the prf file and load it.
        prf_name = self.GetPrfName()
        if prf_name == "": return

        # read in all the lines
        f = open(self.PrfNameToPath(prf_name))
        lines = f.readlines()
        f.close()

        # now loop over the lines, filling in the GUI
        roots = 0
        for line in lines:

            # split the line by the "=" sign
            s = line.split("=")

            # if we have an important line:
            if len(s) == 2:
                # if we found a root argument fill the upper GUI
                if s[0].strip() == "root":
                    if   roots == 0: self.textRoot1.SetValue(s[1].strip())
                    elif roots == 1: self.textRoot2.SetValue(s[1].strip())
                    roots = roots+1

                # otherwise fill the lower GUI
                else:
                    self.textOptions.AppendText(line)
            else:
                self.textOptions.AppendText(line)

        # Save it. This makes sure what you see is correctly synced.
        self.OnButtonSave(None)

    def GetPrfName(self):
        """
        Get and clean up the Prf name.
        """
        # Get whatever garbage the user has typed in there.
        prf_name    = self.comboBoxProfiles.GetValue()

        # remove all the naughty characters
        naughty = [' ','\t', '\n', '\\', '/', '|', '*', '<', '>', ':', '"']
        for c in naughty: prf_name = prf_name.replace(c,'')

        return prf_name


    def OnButtonSave(self, event):
        """
        Saves the currently-visible data to the various system files and generates
        the appropriate windows batch files.
        """

        # reset the gauge
        self.gaugeSaved.SetValue(0)

        # Get whatever garbage the user has typed in there.
        prf_name = self.GetPrfName()
        if prf_name == '': return

        # if it's a new value, append it!
        if not prf_name in self.comboBoxProfiles.GetStrings():
            self.comboBoxProfiles.Append(prf_name)
            self.comboBoxProfiles.SetStringSelection(prf_name)

        # Write the profile file
        output_path = self.PrfNameToPath(prf_name)
        f = open(output_path, 'w')
        f.write('root = ' + self.textRoot1.GetValue() + '\n')
        f.write('root = ' + self.textRoot2.GetValue() + '\n')
        f.write(self.textOptions.GetValue())
        f.close()

        self.gaugeSaved.SetValue(1)

        # Write the FULL batch file for this profile
        f = open(os.path.join(os.getcwdu(), prf_name + " full.bat"), 'w')
        f.write('start /min /wait "pre-commands" "'+prf_name+' pre-commands.bat"\n')
        f.write("unison.exe " + prf_name + " -batch=true\n")
        f.write("if errorlevel 1 pause\n")
        f.write("exit\n")
        f.close()

        self.gaugeSaved.SetValue(2)

        # Write the background launcher for FULL
        f = open(prf_name + " full background.bat",'w')
        f.write('start /MIN /LOW "'+prf_name+'" "'+prf_name+' full'+'.bat"\n')
        f.write('exit\n')
        f.close()

        self.gaugeSaved.SetValue(3)

        # Write the interactive launcher for FULL
        f = open(prf_name + " full interactive.bat", 'w')
        f.write('start /min /wait "pre-commands" "'+prf_name+' pre-commands.bat"\n')
        f.write('unison.exe ' + prf_name + '\n')
        f.write('pause\n')
        f.close()

        self.gaugeSaved.SetValue(4)

        # Write the DIRECTORY batch file for this profile
        f = open(prf_name + " directory.bat", 'w')
        f.write('set a=%1\n')
        f.write('set b=%a:' + self.textRoot1.GetValue() + '\\=%\n')
        f.write('set c=%b:"=%\n') # damn that's some ugly syntax.
        f.write('start /min /wait "pre-commands" "'+prf_name+' pre-commands.bat"\n')
        f.write('unison.exe ' + prf_name + ' -batch=true -path "%c%"\n')
        f.write('if errorlevel 1 pause\n')
        f.write('exit')
        f.close()
        # and the shortcut
        self.CreateShortcut(os.path.join(os.getcwdu(), prf_name + " directory.bat"),
                            os.getcwdu(),
                            os.path.join(self.sendto, prf_name+' automatic.lnk'))

        self.gaugeSaved.SetValue(5)

        # Write the DIRECTORY interactive batch file
        f = open(prf_name + " directory interactive.bat", 'w')
        f.write('set a=%1\n')
        f.write('set b=%a:' + self.textRoot1.GetValue() + '\\=%\n')
        f.write('set c=%b:"=%\n') # damn that's some ugly syntax.
        f.write('start /min /wait "pre-commands" "'+prf_name+' pre-commands.bat"\n')
        f.write('unison.exe '+prf_name+' -path "%c%"\n')
        f.write('if errorlevel 1 pause\n')
        f.write('exit')
        f.close()
        # and the shortcut
        self.CreateShortcut(os.path.join(os.getcwdu(), prf_name + " directory interactive.bat"),
                            os.getcwdu(),
                            os.path.join(self.sendto, prf_name+' interactive.lnk'))

        self.gaugeSaved.SetValue(6)

        # also the pre-commands.bat file
        if not os.path.exists(prf_name + " pre-commands.bat"):
            f = open(prf_name + " pre-commands.bat", "w")
            f.write("\n\n\nexit\n")
            f.close()

        self.gaugeSaved.SetValue(7)
        self.loaded_prf_name = prf_name

    def OnButtonDelete(self, event):

        # Get whatever garbage the user has typed in there.
        prf_name    = self.comboBoxProfiles.GetValue()
        prf_names   = self.comboBoxProfiles.GetStrings()

        if prf_name in prf_names:
            # make sure they want to go forward with this.
            if wx.MessageBox("Are you sure you would like to delete everything to do with the unison profile '"+prf_name+"'? This action cannot be undone.",
                             "Confirm Delete: '"+prf_name+"'", wx.YES_NO) == wx.NO: return

            i = prf_names.index(prf_name)
            self.comboBoxProfiles.Delete(i)
            self.comboBoxProfiles.Select(0)
            self.OnComboBoxProfiles(None)
        else: return

        # now also remove the actual file
        self.RemoveFile(self.PrfNameToPath(prf_name))

        # now remove all the batch files
        self.RemoveFile(prf_name+" full.bat")
        self.RemoveFile(prf_name+" full background.bat")
        self.RemoveFile(prf_name+" full interactive.bat")
        self.RemoveFile(prf_name+" directory.bat")
        self.RemoveFile(prf_name+" directory interactive.bat")
        self.RemoveFile(prf_name+" pre-commands.bat")

        # and the links
        self.RemoveFile(os.path.join(self.sendto, prf_name+' interactive.lnk'))
        self.RemoveFile(os.path.join(self.sendto, prf_name+' automatic.lnk'))


    def OnButtonBrowse1(self, event):
        d = wx.DirDialog(self)
        if d.ShowModal() == 5100:
            self.textRoot1.SetValue(d.GetPath())
            self.gaugeSaved.SetValue(0)

    def OnButtonBrowse2(self, event):
        d = wx.DirDialog(self)
        if d.ShowModal() == 5100:
            self.textRoot2.SetValue(d.GetPath())
            self.gaugeSaved.SetValue(0)

    def OnFrameSetupClose(self, event=None):

        # get the profile name
        prf_name = self.GetPrfName()

        # if we're not saved, save
        if not self.gaugeSaved.GetValue() == self.gaugeSaved.GetRange() and not prf_name == '':
            if wx.MessageBox("Would you like to save the profile '"+prf_name+"' before quitting?",
               "Unsaved Changes", wx.YES|wx.NO): self.OnButtonSave(None)


        # define the controls we want to save
        savies = ["checkBoxQuit", "checkBoxInteractive", "comboBoxProfiles"]

        # save the preferences
        f = open("winison.cfg", "w")
        for savie in savies:
            value = eval("self."+savie+".GetValue()")
            if type(value) in [type(''), type(u'')]: value = "'"+value+"'"
            f.write(savie + "\t" + str(value) + "\n")
        f.close()

        wx.Exit()

    def OnButtonGo(self, event):

        # get the profile name
        prf_name = self.GetPrfName()
        if prf_name=='': return

        # if we're not saved, save
        if not self.gaugeSaved.GetValue() == self.gaugeSaved.GetRange():
            if wx.MessageBox("Would you like to save the profile '"+prf_name+"' before running?",
               "Unsaved Changes", wx.YES|wx.NO): self.OnButtonSave(None)

        # Depending on the check boxes, launch the appropriate sync file
        if self.checkBoxInteractive.GetValue(): wx.Execute(prf_name+" full interactive.bat")
        else:                                   wx.Execute(prf_name+" full.bat")

        # yeah. Quit if we're supposed to.
        if self.checkBoxQuit.GetValue(): self.OnFrameSetupClose(None)

    def OnComboBoxProfiles(self, event):

        # auto load when we select something
        self.OnButtonLoad(None)

    def OnParameterChange(self, event):
        self.gaugeSaved.SetValue(0)

    def OnProfileKey(self,event):
        if not self.GetPrfName() == self.loaded_prf_name:
            self.gaugeSaved.SetValue(0)












