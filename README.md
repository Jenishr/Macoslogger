# Macoslogger
MacOs logs transfer to syslog server.
To configure the MAC OS X to forward logs to a syslog server,
1. Download the file on Server MAC OS machine.
2. Save Macoslogger.zip file and extract the contents of the file to the folder.
3. Go to Utility folder and open the Terminal.
4. Change the directory to where <Extracted MAC_OS_X_Integrator Folder Name> is located.
5. Make sure the below file has executable permission.
<Extracted MAC_OS_X_Integrator Folder Name>/MACLogger integrator.sh
 6. If not executable, use below command to make it executable.
chmod a+x MAClogger/etintegrator
7. Click etintegrator in <Extracted MAC_OS_X_Integrator Folder Name>
8. Enter the password for User SYSAdmin
NOTE: This user has Admin privilege to collect audit logs from the MAC OS. Hence this user account will be
created in all the machine where you are installing the MACAgent with the same credentials. It is recommended
to provide a strong password.
9. Re-enter the same password provided above for verification purpose.
10.Provide the syslog server IP Address.
11.Provide the EventTracker manager syslog port.
12.Once configuration is completed close the terminal window.
13.Check the <Extracted MAC_OS_X_Integrator Folder Name> folder MACAGENT.pkg file that will be
created.
Run the below command using admin privilege.
Sudo installer -pkg MACAGENT.pkg -target /

Open terminal and enter the below command to check whether the following files were created.
Sudo ls /Users/SYSAdmin/Integrator/
Check whether the cron job was created under the user SYSAdmin.
Sudo crontab -u SYSAdmin -l

After Everything verified.. logs will send to syslog server you have configured
