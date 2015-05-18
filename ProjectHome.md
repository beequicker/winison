# Note #
I have stopped development of this project because the exact solution (protocol and everything) I have been wishing for has finally surfaced:

[BitTorrent Sync](http://labs.bittorrent.com/experiments/sync.html)

It is not as customizable as Unison, but they did it right: versioning, encryption, private cloud, no server setup and it works in the background without me thinking about it. I have been wondering why bittorrent hasn't been used this way for almost 10 years.

That being said...

# Introduction #
Why didn't I call this "unidows"?

<img src='http://sites.google.com/site/jacksankey/files/winison_screenshot.png?attredirects=0' align='right' width='300px'>

Winison is a Windows GUI front-end to <a href='http://www.cis.upenn.edu/~bcpierce/unison/'>Unison, the greatest synchronization program ever</a>. Winison can manage profiles, generate the annoyingly-complicated windows batch files that simplify life, and also create windows "Send To" links enabling you to synchronize individual files or folders from within Windows. It's main purpose is to remove the need for you to learn Windows batch scripting (icky) or dig through your system to find your ".unison" and "Send To" folders. You will still need to learn how to use <a href='http://www.cis.upenn.edu/~bcpierce/unison/'>Unison</a> however :).<br>
<br>
<h3>Features</h3>
<ul><li>Create, edit, save, load, delete, and/or run Unison profiles from a centralized interface.<br>
</li><li>Right-click a sub-folder and send it to Unison for synchronizing (awesome).<br>
</li><li>All of the sweet synchronizing features included with <a href='http://www.cis.upenn.edu/~bcpierce/unison/'>Unison</a>, such as two-way synchronization of file changes (i.e. delta sync) and backing up older versions of overwritten files.</li></ul>

<h3>What's included in the self-extracting package</h3>
<ul><li>winison.exe, written in <a href='http://www.python.org/'>python</a> and compiled with <a href='http://www.pyinstaller.org/'>pyinstaller</a>.<br>
</li><li>A working version of Unison (Unison v2.32.94), should you not already have one.<br>
</li><li>Source code, in case you want to monkey with it.</li></ul>

<h3>Installation</h3>
<ul><li><a href='http://code.google.com/p/winison/downloads/list'>Download</a> the self-extracting package.<br>
</li><li>Extract the package into a directory of your choosing. If "unison.exe" already exists in this directory, it will not be overwritten, and Winison will use it. Otherwise, it will use the default version included with the package.<br>
</li><li>Run winison.exe. It will take care of the rest.</li></ul>

Basically, the download includes everything you need to begin synchronizing folders. To get a feel for it, I would recommend first creating two test folders somewhere on your computer. In Winison, select them as roots, type a profile name in Winison's "Profile" menu, and then clicking the "Save" button. This will create all the windows batches and "Send To" links. In Winison, try running the profile in interactive mode. Finally, (after quitting Winison) try clicking a sub-folder inside your "Local Root" directory, selecting "Send To", and then the profile you just saved. This will tell Unison to only sync the selected folder.<br>
<br>
Note that in general running a sync will open a windows command shell showing the sync's progress. If everything goes according to plan, the command shell will automatically close itself. If there are any errors or questions, the command shell will stay open for you to inspect.<br>
<br>
At this point you should be all set and I would recommend perusing the <a href='http://www.cis.upenn.edu/~bcpierce/unison/download/releases/stable/unison-manual.html'>Unison manual</a> to get a feel for what it can do.<br>
<br>
<h3>A note about Windows 7 / Vista</h3>

Winison prefers to write files to its own program directory. If you install Winison into the "Programs", it will not work because it is a protected system directory. Installing Winison in a non-protected directory will solve this problem. I may fix this in a future release, but haven't had time yet.<br>
<br>
<h1>My configuration</h1>

The rest of this page describes my personal backup scheme, in which I have several windows machines synchronizing via a central Unix (Mac Mini) server at my house.<br>
<br>
<h3>My favorite Unison settings</h3>

<pre><code>backup         = Name * <br>
backuplocation = central <br>
backupdir      = Backups <br>
maxbackups     = 37 <br>
retry          = 20 <br>
logfile        = unison.log<br>
perms          = 0 <br>
<br>
ignore         = Name */.svn/*<br>
ignore         = Name */.~lock*<br>
ignore         = Name *.pyc<br>
ignore         = Name desktop.ini<br>
ignore         = Name *.DS_Store<br>
<br>
ignore         = BelowPath */.dropbox*<br>
ignore         = Name */Icon?<br>
forcepartial   = BelowPath Dropbox/* -&gt; D:\Documents<br>
<br>
sshargs        = '-o ServerAliveInterval=10'<br>
</code></pre>

The first lines tell Unison to keep 37 previous copies of any files that are overwritten or deleted, with the same directory structure as the root, starting in the folder "Backups", sets up the log file and solves a problem I was having with permissions. The next bundle of lines tells it what files to ignore, such as Dropbox hidden files, svn hidden files, openoffice lock files, and that annoying windows file desktop.ini that I don't like.<br>
<br>
The "forcepartial" line is about my current Dropbox configuration. I want to make my own versioned backups of the Dropbox folder every week in case something gets (annoyingly) removed by someone else and I don't notice for 30 days. All of the machines but the Unison server (described below) have Dropbox installed in my documents folder, and each of the non-server machines pushes the latest version into the server, which will make versioned backups of files that have changed or disappeared. If the server had Dropbox in the documents folder, no changes would ever be propagated because Dropbox almost instantly synchronizes all the machines.<br>
<br>
The last line fixed a connectivity issue I was having.<br>
<br>
<h3>OpenSSH for securely synchronizing to a remote server</h3>

There are a million and three ways to configure Unison, SSH, servers, disks, web addresses... Here all I can do is tell you what works well for me.<br>
<br>
My sshd server is currently a mac mini with a big fat hard drive, the correct version of unison installed, and <a href='http://www.dyndns.org/'>dyndns</a> or <a href='https://secure.logmein.com/products/hamachi/'>hamachi</a> so I can connect even when I'm on the other side of the planet and the cable company changes my home ip address. If this sounds like babble, ignore it; the point is somewhere on the internet is an ssh server with a matching version of Unison.<br>
<br>
I have a few windows client machines I want to synchronize with each other while also backing up everything on this server. In order to make this work, on each machine I<br>
<ul><li>Installed Cygwin with OpenSSH, and added "C:\cygwin\bin" to the Windows PATH variable (Control Panels -> System -> Advanced System Settings)<br>
</li><li>Installed Winison and ran it.<br>
</li><li>Created and saved a profile with settings very similar to those shown above (and in the screenshot). "Local Root" is my documents directory, and "Remote Root" is the ssh server path (something like ssh://yourusername@your.server.com:12345/Documents).</li></ul>

At this point I can run the full synchronization using Winison, or I can right-click a sub-directory, select "Send To" and synchronize this directory alone.<br>
<br>
Note that especially for over-the-internet backups, I highly recommend starting with identical directories before running unison the first time. Unison is extremely smart about not wasting bandwidth, and a full update of 50 GB could take a long, long time. OpenSSH comes with <a href='http://en.wikipedia.org/wiki/Secure_copy'>scp</a>, which is one route to initially upload. Otherwise it's all about the external hard drives. It is also possible to use Unison's "copyprog" and "copythreshold" variables to specify an alternative program to use for transferring large files. I suspect one could use scp as the alternative, but I haven't messed with this because I don't need to.<br>
<br>
<h3>Automatic log-on</h3>

The above setup requires me to enter my ssh password every time I want to connect. To enable automatic log-on, I had to generate rsa keys, monkey with the server a bit, and transported my private key to each client machine. What you need in the end is<br>
<ul><li>A private rsa key in your CYGWIN user's .ssh directory (e.g. C:\cygwin\home\yourusername\.ssh)<br>
</li><li>A corresponding public key appended to your server's user .ssh/authorized_keys file (e.g. /home/yourusername/.ssh/authorized_keys)<br>
</li><li>The ssh server configured to accept public key authentication.</li></ul>

I chose to generate my rsa keys on the server. Logged in with my username, I had a session that looked like this:<br>
<br>
<pre><code>&gt; ssh-keygen -t rsa<br>
Generating public/private rsa key pair.<br>
Enter file in which to save the key (/home/myusername/.ssh/id_rsa):<br>
Created directory '/home/myusername/.ssh'.<br>
Enter passphrase (empty for no passphrase):<br>
Enter same passphrase again: <br>
Your identification has been saved in /home/myusername/.ssh/id_rsa.<br>
Your public key has been saved in /home/myusername/.ssh/id_rsa.pub.<br>
The key fingerprint is:<br>
[ ... a string of stuff ... ]<br>
<br>
&gt; cat ~/.ssh/id_rsa.pub &gt;&gt; ~/.ssh/authorized_keys<br>
&gt; chmod 0600 ~/.ssh/authorized_keys<br>
</code></pre>

This business generated a new public/private key pair and added the public key to a list of authorized keys. Note I used no passphrase, and just pressed enter a bunch of times. The chmod step was surprisingly important.<br>
<br>
Then, the sshd server had to be configured to accept these auto-logins, so I made sure the file /etc/ssh/sshd_config contained the following lines:<br>
<br>
<pre><code>RSAAuthentication yes<br>
PubkeyAuthentication yes<br>
AuthorizedKeysFile .ssh/authorized_keys<br>
</code></pre>

Finally, I had to find a way to get the id_rsa file into each of the windows users .ssh directories (i.e. C:\cygwin\home\myusername\.ssh\). <b>This file is your private key (i.e. your password), so don't leave copies lying around!</b>

Since cygwin ssh comes with scp, I used that to download and set the correct permissions of your private key:<br>
<br>
<pre><code>&gt; scp myusername@my.server.com:.ssh/id_rsa /home/myusername/.ssh/id_rsa<br>
&gt; chmod 0600 /home/myusername/.ssh/id_rsa<br>
</code></pre>

Anyway, at this point it all worked for me. I use <a href='http://support.microsoft.com/kb/308569'>windows scheduler</a> to run the full background backup every night. All my computers are synchronized and backed up with file versioning. Changes in one computer are easily transfered to the other. Awesome.<br>
<br>
Enjoy!<br>
<br>
-Jack<br>
<br>
<br>
<br>
<h1>Uninstalling</h1>

I personally dislike Windows installers and I am against modifying the Windows registry. To uninstall this program, just run Winison, delete all the profiles, and then delete the Winison folder. Unison itself may have created a folder ".unison" in your user directory, but this is just where it stores the profiles. It is a small amount of data that you're free to delete. If something odd happens during this uninstallation, note that the only other files created by Winison exist in your user's "Start Menu" and "SendTo" directories.