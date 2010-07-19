#Boa:Frame:frameSetup

import wx
import os
import glob
import win32com.client
import platform

def create(parent):
    return frameSetup(parent)

[wxID_FRAMESETUP, wxID_FRAMESETUPBUTTONBROWSE1, wxID_FRAMESETUPBUTTONBROWSE2, 
 wxID_FRAMESETUPBUTTONDELETE, wxID_FRAMESETUPBUTTONGO, 
 wxID_FRAMESETUPBUTTONLOAD, wxID_FRAMESETUPBUTTONSAVE, 
 wxID_FRAMESETUPCHECKBOXINTERACTIVE, wxID_FRAMESETUPCHECKBOXQUIT, 
 wxID_FRAMESETUPCOMBOBOXPROFILES, wxID_FRAMESETUPSTATICTEXT1, 
 wxID_FRAMESETUPSTATICTEXT2, wxID_FRAMESETUPSTATICTEXT3, 
 wxID_FRAMESETUPTEXTOPTIONS, wxID_FRAMESETUPTEXTROOT1, 
 wxID_FRAMESETUPTEXTROOT2, 
] = [wx.NewId() for _init_ctrls in range(16)]

class frameSetup(wx.Frame):

    # paths assembled in LoadUp
    dot_unison     = None
    sendto         = None
    parent         = None
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMESETUP, name='frameSetup',
              parent=prnt, pos=wx.Point(314, 128), size=wx.Size(428, 465),
              style=wx.DEFAULT_FRAME_STYLE, title='Unison Setup')
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

        self.textRoot2 = wx.TextCtrl(id=wxID_FRAMESETUPTEXTROOT2,
              name='textRoot2', parent=self, pos=wx.Point(80, 91),
              size=wx.Size(272, 21), style=0, value='')
        self.textRoot2.SetToolTipString('Path to the "remote" root.')

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
        self.textOptions.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Courier New'))
        self.textOptions.SetToolTipString('Additional Unison options.')

        self.comboBoxProfiles = wx.ComboBox(choices=[],
              id=wxID_FRAMESETUPCOMBOBOXPROFILES, name='comboBoxProfiles',
              parent=self, pos=wx.Point(42, 8), size=wx.Size(146, 21), style=0,
              value='')
        self.comboBoxProfiles.SetLabel('')
        self.comboBoxProfiles.SetToolTipString('Select a profile')

        self.staticText3 = wx.StaticText(id=wxID_FRAMESETUPSTATICTEXT3,
              label='Profile', name='staticText3', parent=self, pos=wx.Point(8,
              13), size=wx.Size(30, 13), style=0)
        self.staticText3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        self.staticText3.SetToolTipString('')

        self.buttonLoad = wx.Button(id=wxID_FRAMESETUPBUTTONLOAD, label='Load',
              name='buttonLoad', parent=self, pos=wx.Point(41, 31),
              size=wx.Size(48, 23), style=0)
        self.buttonLoad.SetToolTipString('Load the selected profile into the lower fields.')
        self.buttonLoad.Bind(wx.EVT_BUTTON, self.OnButtonLoad,
              id=wxID_FRAMESETUPBUTTONLOAD)

        self.buttonGo = wx.Button(id=wxID_FRAMESETUPBUTTONGO, label='Go',
              name='buttonGo', parent=self, pos=wx.Point(191, 8),
              size=wx.Size(64, 46), style=0)
        self.buttonGo.SetToolTipString('Execute selected profile as a background process.')
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
        self.checkBoxInteractive.SetToolTipString('Check this if you want an interactive Unison sync (as opposed to automatic)')

        self.checkBoxQuit = wx.CheckBox(id=wxID_FRAMESETUPCHECKBOXQUIT,
              label='Quit after launching', name='checkBoxQuit', parent=self,
              pos=wx.Point(257, 25), size=wx.Size(129, 13), style=0)
        self.checkBoxQuit.SetValue(True)
        self.checkBoxQuit.SetToolTipString('Check this if you want to shut down Winison when you press "Go"')

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
        else:
            # assume it's XP
            self.sendto         = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "SendTo")
            
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
                    try:    exec("self."+key+"("+value+")")
                    except: print "Could not '"+"self."+key+"("+value+")'."


    
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
        prf_name = self.comboBoxProfiles.GetValue()
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


    def OnButtonSave(self, event):
        """
        Saves the currently-visible data to the various system files and generates
        the appropriate windows batch files.
        """

        # Get whatever garbage the user has typed in there.
        prf_name    = self.comboBoxProfiles.GetValue()

        # remove all the naughty characters
        naughty = [' ','\t', '\n', '\\', '/', '|', '*', '<', '>', ':', '"']
        for c in naughty: prf_name = prf_name.replace(c,'')

        # if it's a new value, append it!
        if not prf_name in self.comboBoxProfiles.GetStrings():
            self.comboBoxProfiles.Append(prf_name)
            self.comboBoxProfiles.SetStringSelection(prf_name)

        # Write the profile file
        output_path = self.PrfNameToPath(prf_name)
        f = open(output_path, 'w')
        f.write('root = ' + self.textRoot1.GetValue() + '\n')
        f.write('root = ' + self.textRoot2.GetValue() + '\n')
        f.write(self.textOptions.GetValue() + '\n')
        f.close()

        # Write the FULL batch file for this profile
        f = open(os.path.join(os.getcwdu(), prf_name + " full.bat"), 'w')
        f.write("start /min /wait pre-commands.bat\n")
        f.write("unison.exe " + prf_name + " -batch=true\n")
        f.write("if errorlevel 1 pause\n")
        f.write("exit\n")
        f.close()

        # Write the background launcher for FULL
        f = open(prf_name + " full background.bat",'w')
        f.write('start /MIN /LOW "'+prf_name+'" "'+prf_name+' full'+'.bat"\n')
        f.write('exit\n')
        f.close()

        # Write the interactive launcher for FULL
        f = open(prf_name + " full interactive.bat", 'w')
        f.write('start /min /wait pre-commands.bat\n')
        f.write('unison.exe ' + prf_name + '\n')
        f.write('pause\n')
        f.close()

        # Write the DIRECTORY batch file for this profile
        f = open(prf_name + " directory.bat", 'w')
        f.write('set a=%1\n')
        f.write('set b=%a:' + self.textRoot1.GetValue() + '\\=%\n')
        f.write('set c=%b:"=%\n') # damn that's some ugly syntax.
        f.write('start /min /wait pre-commands.bat\n')
        f.write('unison.exe ' + prf_name + ' -batch=true -path "%c%"\n')
        f.write('if errorlevel 1 pause\n')
        f.write('exit')
        f.close()
        # and the shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(self.sendto, prf_name+' automatic.lnk'))
        shortcut.Targetpath =           os.path.join(os.getcwdu(), prf_name + " directory.bat")
        shortcut.WorkingDirectory =     os.getcwdu()
        shortcut.save()

        # Write the DIRECTORY interactive batch file
        f = open(prf_name + " directory interactive.bat", 'w')
        f.write('set a=%1\n')
        f.write('set b=%a:' + self.textRoot1.GetValue() + '\\=%\n')
        f.write('set c=%b:"=%\n') # damn that's some ugly syntax.
        f.write('start /min /wait pre-commands.bat\n')
        f.write('unison.exe '+prf_name+' -path "%c%"\n')
        f.write('if errorlevel 1 pause\n')
        f.write('exit')
        f.close()
        # and the shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(self.sendto, prf_name+' interactive.lnk'))
        shortcut.Targetpath =           os.path.join(os.getcwdu(), prf_name + " directory interactive.bat")
        shortcut.WorkingDirectory =     os.getcwdu()
        shortcut.save()





    def OnButtonDelete(self, event):
        # Get whatever garbage the user has typed in there.
        prf_name    = self.comboBoxProfiles.GetValue()
        prf_names   = self.comboBoxProfiles.GetStrings()

        if prf_name in prf_names:
            i = prf_names.index(prf_name)
            self.comboBoxProfiles.Delete(i)

        # now also remove the actual file
        os.remove(self.PrfNameToPath(prf_name))

        # now remove all the batch files
        os.remove(prf_name+" full.bat")
        os.remove(prf_name+" full background.bat")
        os.remove(prf_name+" full interactive.bat")
        os.remove(prf_name+" directory.bat")
        os.remove(prf_name+" directory interactive.bat")

        # and the links
        os.remove(os.path.join(self.sendto, prf_name+' interactive.lnk'))
        os.remove(os.path.join(self.sendto, prf_name+' automatic.lnk'))

    def OnButtonBrowse1(self, event):
        d = wx.DirDialog(self)
        if d.ShowModal() == 5100:
            self.textRoot1.SetValue(d.GetPath())

    def OnButtonBrowse2(self, event):
        d = wx.DirDialog(self)
        if d.ShowModal() == 5100:
            self.textRoot2.SetValue(d.GetPath())

    def OnFrameSetupClose(self, event):
        
        # define the controls we want to save
        values = ["checkBoxQuit.GetValue", 
                  "checkBoxInteractive.GetValue"]
                 
        strings = ["comboBoxProfiles.GetStringSelection"]
        
        # save the preferences
        f = open("winison.cfg", "w")
        for savie in values:
            f.write(savie.replace(".Get",".Set") + 
                    "\t"+str(eval("self."+savie+"()"))+"\n")
        for savie in strings:
            f.write(savie.replace(".Get",".Set") +
                    "\t'"+str(eval("self."+savie+"()"))+"'\n")
        f.close()
        
        wx.Exit()

    def OnButtonGo(self, event):
        event.Skip()















