class ModEntry:

    def __init__(self, name, path, is_enabled):
        self.modname = name
        self.fullpath = path
        self.enabled = is_enabled
    
    def get_name(self):
        return self.modname

    def get_enabled(self):
        return self.enabled

    def flip_enabled_status(self):
        self.enabled = not self.enabled

    #def print_entry(self):
    #    print('|{}\t\t|{}\t'.format(self.modname, 'Yes' if self.enabled else 'No'))
