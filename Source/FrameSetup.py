#Boa:Frame:frameSetup

import wx
import os
import glob
import win32com.client
import platform

def create(parent):
    return frameSetup(parent)

[wxID_FRAMESETUP, wxID_FRAMESETUPBUTTONBROWSE1, wxID_FRAMESETUPBUTTONBROWSE2,
 wxID_FRAMESETUPBUTTONDELETE, wxID_FRAMESETUPBUTTONLOAD,
 wxID_FRAMESETUPBUTTONSAVE, wxID_FRAMESETUPCOMBOBOXPROFILES,
 wxID_FRAMESETUPSTATICTEXT1, wxID_FRAMESETUPSTATICTEXT2,
 wxID_FRAMESETUPSTATICTEXT3, wxID_FRAMESETUPTEXTOPTIONS,
 wxID_FRAMESETUPTEXTROOT1, wxID_FRAMESETUPTEXTROOT2,
] = [wx.NewId() for _init_ctrls in range(13)]

class frameSetup(wx.Frame):

    # paths assembled in LoadUp
    dot_unison = None
    sendto     = None

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMESETUP, name='frameSetup',
              parent=prnt, pos=wx.Point(67, 35), size=wx.Size(430, 490),
              style=wx.DEFAULT_FRAME_STYLE, title='Unison Setup')
        self.SetClientSize(wx.Size(420, 455))
        self.SetBackgroundColour(wx.Colour(234, 234, 238))
        self.SetToolTipString('')

        self.buttonSave = wx.Button(id=wxID_FRAMESETUPBUTTONSAVE, label='Save',
              name='buttonSave', parent=self, pos=wx.Point(315, 7),
              size=wx.Size(48, 23), style=0)
        self.buttonSave.Bind(wx.EVT_BUTTON, self.OnButtonSave,
              id=wxID_FRAMESETUPBUTTONSAVE)

        self.buttonDelete = wx.Button(id=wxID_FRAMESETUPBUTTONDELETE,
              label='Delete', name='buttonDelete', parent=self,
              pos=wx.Point(365, 7), size=wx.Size(48, 23), style=0)
        self.buttonDelete.Bind(wx.EVT_BUTTON, self.OnButtonDelete,
              id=wxID_FRAMESETUPBUTTONDELETE)

        self.staticText1 = wx.StaticText(id=wxID_FRAMESETUPSTATICTEXT1,
              label='Root 1', name='staticText1', parent=self, pos=wx.Point(8,
              59), size=wx.Size(32, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAMESETUPSTATICTEXT2,
              label='Root 2', name='staticText2', parent=self, pos=wx.Point(8,
              83), size=wx.Size(32, 13), style=0)

        self.textRoot1 = wx.TextCtrl(id=wxID_FRAMESETUPTEXTROOT1,
              name='textRoot1', parent=self, pos=wx.Point(48, 56),
              size=wx.Size(304, 21), style=0, value='')

        self.textRoot2 = wx.TextCtrl(id=wxID_FRAMESETUPTEXTROOT2,
              name='textRoot2', parent=self, pos=wx.Point(48, 80),
              size=wx.Size(304, 21), style=0, value='')

        self.buttonBrowse1 = wx.Button(id=wxID_FRAMESETUPBUTTONBROWSE1,
              label='Browse', name='buttonBrowse1', parent=self,
              pos=wx.Point(355, 55), size=wx.Size(58, 23), style=0)
        self.buttonBrowse1.SetToolTipString('')
        self.buttonBrowse1.Bind(wx.EVT_BUTTON, self.OnButtonBrowse1,
              id=wxID_FRAMESETUPBUTTONBROWSE1)

        self.buttonBrowse2 = wx.Button(id=wxID_FRAMESETUPBUTTONBROWSE2,
              label='Browse', name='buttonBrowse2', parent=self,
              pos=wx.Point(355, 79), size=wx.Size(58, 23), style=0)
        self.buttonBrowse2.Bind(wx.EVT_BUTTON, self.OnButtonBrowse2,
              id=wxID_FRAMESETUPBUTTONBROWSE2)

        self.textOptions = wx.TextCtrl(id=wxID_FRAMESETUPTEXTOPTIONS,
              name='textOptions', parent=self, pos=wx.Point(8, 104),
              size=wx.Size(404, 344), style=wx.TE_MULTILINE | wx.HSCROLL,
              value='')

        self.comboBoxProfiles = wx.ComboBox(choices=[],
              id=wxID_FRAMESETUPCOMBOBOXPROFILES, name='comboBoxProfiles',
              parent=self, pos=wx.Point(48, 8), size=wx.Size(215, 21), style=0,
              value='')
        self.comboBoxProfiles.SetLabel('')

        self.staticText3 = wx.StaticText(id=wxID_FRAMESETUPSTATICTEXT3,
              label='Profile', name='staticText3', parent=self, pos=wx.Point(8,
              13), size=wx.Size(30, 13), style=0)
        self.staticText3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))

        self.buttonLoad = wx.Button(id=wxID_FRAMESETUPBUTTONLOAD, label='Load',
              name='buttonLoad', parent=self, pos=wx.Point(265, 7),
              size=wx.Size(48, 23), style=0)
        self.buttonLoad.Bind(wx.EVT_BUTTON, self.OnButtonLoad,
              id=wxID_FRAMESETUPBUTTONLOAD)

    def __init__(self, parent):
        self._init_ctrls(parent)

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
            self.sendto = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "SendTo")
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

        # select the first one




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

        # if it's a new value, append it!
        if not prf_name in self.comboBoxProfiles.GetStrings():
            self.comboBoxProfiles.Append(prf_name)

        # Write the profile file
        output_path = self.PrfNameToPath(self.comboBoxProfiles.GetValue())
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
        f.write('unison.exe jackattack -batch=true -path "%c%"\n')
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
        f.write('unison.exe jackattack -path "%c%"\n')
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















