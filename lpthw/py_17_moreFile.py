# --coding:utf-8--
from sys import argv
from os.path import exists

script, source_file, sink_file = argv

print("Copying from %s to %s " % (source_file, sink_file))

# we could do these two on one line too, how?

input_file = open(source_file)
indata = input_file.read()

print("The input file has %d bytes long." % len(indata))

print("Does the output file exists? %r " % exists(sink_file))

print("Ready, hit RETURN to continue, CTRL-C to abort.")

input()

output_file = open(sink_file, mode='w+')
output_file.write(indata)
print("Finish!")
output_file.close()
input_file.close()
