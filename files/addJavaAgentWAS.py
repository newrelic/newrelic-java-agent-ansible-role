import sys

# Must be executed with wsadmin.sh.

# Get the matching JVM IDs
def findJvmId(name):
    ids = []
    servers = AdminTask.listServers("[-serverType APPLICATION_SERVER]").splitlines()
    for server in servers:
        serverName = AdminConfig.showAttribute(server,"name")
        if (serverName == name):
            ids.append(AdminConfig.list("JavaVirtualMachine",server))
    return ids


# Get current generic JVM arguments 
def getJvmArguments(jvm):
    args = AdminConfig.showAttribute(jvm,"genericJvmArguments")
    return str(args)

def addJavaagent(jvm, args, path):
    newArgs = args + " -javaagent:"+path
    print("Updated arguments: " + newArgs)
    print AdminConfig.modify(jvm,[["genericJvmArguments",newArgs]])
    print AdminConfig.save()

def syncAllNodes():
    print AdminNodeManagement.syncActiveNodes()

# JVM Name and location of Java agent must be passed as arguments
name = sys.argv[0]
path = sys.argv[1]
# Booleans are not supported in Jython for WAS 8.5.X
added = 0

jvms = findJvmId(name)
if len(jvms) == 0:
    print('Error - Unable to find matching JVM!')
    sys.exit(1)

for jvm in jvms:
    args = getJvmArguments(jvm)
    print("Previous arguments: " + args)
    if (args.find("javaagent") > -1):
        print("javaagent already defined")
    else:
        print("javaagent argument not defined - adding")
        addJavaagent(jvm, args, path)
        added = 1
if added > 0:
    print("Added javaagent argument on at least one server. Syncing nodes.")
    syncAllNodes()
else:
    print("javaagent already defined on all matching servers")
