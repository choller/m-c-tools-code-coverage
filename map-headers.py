#!/usr/bin/python

import os, sys

def main(argv):
  from optparse import OptionParser
  o = OptionParser()
  o.add_option('-m', '--map-string', dest="map_string", default="dist/include/",
      help="Try to map files containing STRING", metavar="STRING")
  o.add_option('-b', '--base-string', dest="base_string", default="try-lnx64-dbg/build/",
      help="Truncate path up to (including) STRING", metavar="STRING")
  o.add_option('-d', '--directory', dest="base_dir",
      help="Base directory for relative paths", metavar="STRING")
  o.add_option('-o', '--output', dest="outfile",
      help="File to output data to FILE", metavar="FILE")
  (opts, args) = o.parse_args(argv)

  files = {}


  # Store it to output
  if opts.outfile != None:
    print >> sys.stderr, "Writing to file %s" % opts.outfile
    outfd = open(opts.outfile, 'w')
  else:
    outfd = sys.stdout

  infd = open(args[0], 'r')
  for line in infd:
    if line.startswith("SF:"):
      filename = line.split(':')[1].strip()
      idx = filename.find(opts.base_string)
      if idx >= 0:
        filename = filename[idx+len(opts.base_string):]
      
      if opts.base_dir != None and filename[0] != os.sep:
        filename = os.path.join(opts.base_dir, filename)
        
      if filename.find(opts.map_string) == -1:
        files[filename] = 1
  infd.close()

  infd = open(args[0], 'r')
  for line in infd:
    if line.startswith("SF:"):
      filename = line.split(':')[1].strip()
      mapidx = filename.find(opts.map_string)
      mapped = False
      if mapidx != -1:
        #basename = filename[mapidx+len(opts.map_string):]
        basename = os.path.basename(filename)
        for key in files.iterkeys():
          if key.endswith(os.sep + basename):
            mapped = True
            outfd.write("SF:" + key + "\n")
            break

      if not mapped:
        idx = filename.find(opts.base_string)
        if idx >= 0:
          filename = filename[idx+len(opts.base_string):]

        if opts.base_dir != None and filename[0] != os.sep:
	  filename = os.path.join(opts.base_dir, filename)

        outfd.write("SF:" + filename + "\n")
          
    else:
      outfd.write(line)


  outfd.close()

if __name__ == '__main__':
  main(sys.argv[1:])
