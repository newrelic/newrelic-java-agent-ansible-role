import sys

# Must be executed with wsadmin.sh.

# Get the JVM ID
def findJvmId(name):
    servers = AdminConfig.list("Server").splitlines()
    for server in servers:
        serverName = AdminConfig.showAttribute(server,"name")
        if (serverName == name):
            id = AdminConfig.list("JavaVirtualMachine",server)
            return id


# Get current generic JVM arguments 
def getJvmArguments(jvm):
    args = AdminConfig.showAttribute(jvm,"genericJvmArguments")
    return str(args)

def addJavaagent(jvm, args, path):
    newArgs = args + " -javaagent:"+path
    print("Updated arguments: " + newArgs)
    print AdminConfig.modify(jvm,[["genericJvmArguments",newArgs]])
    print AdminConfig.save()

# JVM Name and location of Java agent must be passed as arguments
name = sys.argv[0]
path = sys.argv[1]

jvm = findJvmId(name)
if jvm is None:
    print('Error - Unable to find matching JVM!')
    sys.exit(1)

args = getJvmArguments(jvm)
print("Previous arguments: " + args)
if (args.find("javaagent") > -1):
    print("javaagent already defined")
else:
    print("javaagent argument not defined - adding")
    addJavaagent(jvm, args, path)
