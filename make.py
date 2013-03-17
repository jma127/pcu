import os

import globals
import helper
import pattern
import settings

# Problem Creation Engine

def make ():
    print 'Creating {} source file for problem {}'.format(settings.langexts[globals.getext()], globals.getprob())
    template = helper.read(os.path.join(globals.templatedir, globals.getmode() + '.' + globals.getext()))
    if template is None:
        print '{}.{} template file not found (add it to templates folder)'.format(globals.getmode(), globals.getext())
        return False
    helper.write(os.path.join(globals.working, globals.getsrc()), pattern.convert(template))
    print 'Source file created: ' + globals.getsrc()
    return True
