import os
os.chdir('kafka')
print('Starting zookeeper')
os.system('bin\windows\zookeeper-server-start config\zookeeper.properties')