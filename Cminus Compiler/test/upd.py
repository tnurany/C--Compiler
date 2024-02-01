#!/usr/bin/python3
import sys
import re
import os
for f in sys.argv[1:len(sys.argv)]:
    lines = []
    num = 1
    base,suffix = os.path.splitext(f)
    with open(f) as inf:
        for line in inf:
            if (num == 21):
                lines.append(line)
                lines.append('import subprocess\n')
            elif (num == 26):
                lines.append('        fn = "../input/'+base+'.cm"\n')
                lines.append('        self.assertEqual(cminus_parser.compile_program(fn),"Success");\n')

                lines.append('        asm = fn.replace("input","output").replace(".cm",".s")\n')
                lines.append('        run = asm.replace(".s","")\n')
                lines.append('        cmd = ["/usr/bin/gcc","-o",run,asm]\n')
                lines.append('        status = subprocess.run(cmd)\n')
                lines.append('        self.assertEqual(status.returncode,0)\n')
                lines.append(' \n')
                lines.append('        out = asm.replace(".s",".out")\n')
                lines.append('        f = open(out,"w")\n')
                lines.append('        cmd = [run]\n')
                lines.append('        status = subprocess.run(cmd,stdout=f)\n')
                lines.append('        f.close() \n')
                lines.append('        self.assertGreaterEqual(status.returncode, 0)\n')
                lines.append(' \n')
                lines.append('        orig = out.replace("output","orig").replace(".out",".orig")\n')
                lines.append('        cmd = ["/usr/bin/diff","-w","-B","-b",out,orig]\n')
                lines.append('        status = subprocess.run(cmd)\n')
                lines.append('        self.assertEqual(status.returncode,0)\n')
            else:
                lines.append(line)
            num += 1 
        inf.close()
    with open(f,'w') as outf:
        for line in lines:
            outf.write(line)
        outf.close()

