import sys
import time

# Must be executed with wsadmin.sh and is typically invoked via Ansible.
# Arguments:
# * Server/JVM name (or all*)
# ** If all is used, we will attempt to include the javaagent flag on all application servers returned by wsadmin
# ** This can cause issues if application servers are instrumented and their hosts are not included in the play.
# ** If a javaagent argument is added and the JAR does not exist on that host, the application server will not start correctly.
# * add or replace - add the New Relic javaagent flag to existing generic JVM arguments or replace existing javaagent flags
# * Full path to the newrelic.jar location

# Get the matching JVM IDs
def findJvmId(name):
    ids = []
    servers = AdminConfig.list("Server").splitlines()
    for server in servers:
        serverType = AdminConfig.showAttribute(server,"serverType")
        if serverType == "APPLICATION_SERVER":
            if name.lower() == 'all':
                ids.append(AdminConfig.list("JavaVirtualMachine",server))
            else: 
                serverName = AdminConfig.showAttribute(server,"name")
                if (serverName.lower() == name.lower()):
                    ids.append(AdminConfig.list("JavaVirtualMachine",server))
    return ids

# Get current generic JVM arguments 
def getJvmArguments(jvm):
    args = AdminConfig.showAttribute(jvm,"genericJvmArguments")
    return str(args)

# Write a backup list of generic JVM arguments to the file system before making any changes
# The script will fail if we are unable to backup the current arguments
def backupArguments(name, jvm, args, path):
    epoch_time = int(time.time())
    backupPath = path.replace("newrelic.jar", "backupJVMArgs-" + str(name) + "-" + str(epoch_time))
    print("Backing up previous generic JVM arguments to: "+backupPath)
    f = open(backupPath, "w")
    f.write("JVM: "+jvm+ "\n")
    f.write("Previous generic arguments:\n")
    f.write(args + "\n")
    f.close()

def setJvmArguments(jvm, args):
    print AdminConfig.modify(jvm,[["genericJvmArguments",args]])
    print AdminConfig.save()

def addJavaagent(name, backupExists, jvm, args, path):
    added = 0
    if (args.find("newrelic.jar") > -1):
        print("New Relic javaagent already defined")
    else: 
        if backupExists == 0:
            backupArguments(name, jvm, args, path)
        print ("Adding New Relic javaagent argument")
        # Determine whether or not a space is needed before the javaagent argument
        added = 1
        if (len(args) > 0):
            args = args.rstrip()
            javaagentString = " -javaagent:"+path
        else:
            javaagentString = "-javaagent:"+path
        newArgs = args + "" + javaagentString
        print("Updated arguments: " + newArgs)
        setJvmArguments(jvm, newArgs)
    return added

# Find any existing javaagent arguments and replace them with the New Relic javaagent argument
def replaceJavaagent(name, jvm, args, path):
    modified = 0
    added = 0
    newArgs = ""
    if len(args) > 0:
        splitArgs = args.split("-")
        for arg in splitArgs:
            # Handling the first split at - being empty
            if len(arg) > 0: 
                if (arg.find("javaagent") > -1 and (arg.find("javaagent:"+str(path)) == -1)):
                    print("Non New Relic javaagent argument found. Removing: " +str(arg))
                    modified = 1
                    backupArguments(name, jvm, args, path)
                else:
                    newArgs = newArgs + "-" + str(arg)
    added = addJavaagent(name, modified, jvm, newArgs, path)
    # Was an argument removed but no new argument added? If so, we need to save the configuration.
    if (modified == 1 and added == 0):
        setJvmArguments(jvm, newArgs)
    return modified+added

# If any of the servers are a managed process (clustered), sync the node configuration.
def syncNodes(name):
    managed = 0
    servers = AdminControl.queryNames('type=Server,*').splitlines()
    for server in servers:
        # If we find a ManagedProcess, we will sync the node configuration
        if (server.find('processType=ManagedProcess') > -1):
            managed = 1
    if managed == 1:
        print("Clustered environment found - syncing nodes")
        print AdminNodeManagement.syncActiveNodes()
    else:
        print("Unmanaged process. No cluster. No need to sync node configurations from dmgr.")

# JVM name (or all), add or replace, and the location of Java agent JAR must be passed as arguments
name = sys.argv[0]
addOrReplace = sys.argv[1]
path = sys.argv[2]
# Booleans are not supported in Jython for WAS 8.5.X
changed = 0

jvms = findJvmId(name)
if len(jvms) == 0:
    print('Error - Unable to find matching JVM!')
    sys.exit(1)

for jvm in jvms:
    args = getJvmArguments(jvm)
    print("Previous arguments: " + args)

    if (addOrReplace.lower() == "replace"):
        print("Replacing existing javaagent arguments (if found)")
        changed += replaceJavaagent(name, jvm, args, path)
    else:
        changed += addJavaagent(name, 0, jvm, args, path)
if changed > 0:
    # Sync node configuration if clustered
    syncNodes(name)
    print("Added/replaced javaagent argument on at least one server.")
else:
    print("New Relic javaagent already defined on all matching servers")
