import os
from os import listdir, mkdir
from os.path import isfile, isdir, join, splitext
import shutil
import re

def multijoin(xs, ys):
    if isinstance(xs, list):
        return [join(x, ys) for x in xs]
    elif isinstance(ys, list):
        return [join(xs, y) for y in ys]
    else:
        return join(xs, ys)

def get_file_names(folder, f = None):
    file_names = listdir(folder)
    if f is None: return file_names
    return [name for name in file_names if f(name)]

def get_file_paths(folder, f = None):
    return multijoin(folder, get_file_names(folder))

def get_file_count(folder):
    return len(listdir(folder))

def get_image_names(folder):
    return get_file_names(folder, lambda name: name.endswith(".jpg") or name.endswith(".png") or name.endswith(".JPG") or name.endswith(".PNG"))

def get_image_paths(folder):
    return multijoin(folder, get_image_names(folder))

def get_subfolder_names(folder, f = None):
    return get_file_names(folder, lambda name: isdir(join(folder, name)) and (f is None or f(name)))

def get_subfolder_paths(folder, f = None):
    return multijoin(folder, get_subfolder_names(folder, f))

def get_prefixed_sf_names(folder, prefix):
    return get_subfolder_names(folder, lambda name: name.startswith(prefix))

def get_prefixed_sf_paths(folder, prefix):
    return get_subfolder_paths(folder, lambda name: name.startswith(prefix))

def has_file(folder, name):
    return isfile(join(folder, name))

def have_file(folders, name):
    for folder in folders:
        if has_file(folder, name): return True
    return false

file_number_re = re.compile("^(.+) \\(([0-9]+)\\)$")
def next_file_path(path):
    actual_path, extension = splitext(path)
    file_number_match = file_number_re.match(actual_path)
    if not file_number_match:
        return actual_path + " (1)." + extension
    return file_number_match.group(0) + " (" + (int(file_number_match.group(1)) + 1) + ")." + extension



base = "D:\\sensus_classification"
# base = "/Users/wircho/Desktop/classes"
YES_ = "YES_"
NO_ = "NO_"

if not(isdir(join(base, "images"))): raise ValueError("No \"images\" folder found")

class Folder:
    def __init__(self, name, forced_base = None):
        self.name = name
        self.base = base if forced_base == None else forced_base
        self.path = base if self.name is None else join(self.base, self.name)
    def slash(self, name):
        return join(self.path, name)
    def has(self, name):
        if not self.exists(): return False
        return has_file(self.path, name)
    def exists(self):
        return isdir(self.path)
    def create(self):
        mkdir(self.path)
    def ensure(self):
        if not self.exists():
            self.create()
    def file_names(self, f = None):
        self.ensure()
        return get_file_names(self.path, f)
    def file_paths(self, f = None):
        self.ensure()
        return get_file_paths(self.path, f)
    def count(self):
        self.ensure()
        return get_file_count(self.path)
    def image_names(self):
        self.ensure()
        return get_image_names(self.path)
    def image_paths(self):
        self.ensure()
        return get_image_paths(self.path)
    def sub(self, name):
        return Folder(name, self.path)
    def subfolders(self, f = None):
        return [self.sub(name) for name in get_subfolder_names(self.path, f)]
    def prefixed_subfolders(self, prefix):
        return self.subfolders(lambda folder: folder.startswith(prefix))
    def yeses(self):
        return self.prefixed_subfolders(YES_)
    def noes(self):
        return self.prefixed_subfolders(NO_)
    def yes(self, cat):
        return self.sub(YES_ + cat.name)
    def no(self, cat):
        return self.sub(NO_ + cat.name)
    def reserve(self, name):
        reserved = self.sub("reserved") if self.name is None else Folder("reserved", self.base)
        self.copy(name, reserved)
    def unreserve(self, name):
        reserved = self.sub("reserved") if self.name is None else Folder("reserved", self.base)
        trash = self.sub("trash") if self.name is None else Folder("trash", self.base)
        #reserved.move(name, trash, True)
        reserved.remove(name)
    def is_reserved(self, name):
        reserved = self.sub("reserved") if self.name is None else Folder("reserved", self.base)
        return reserved.has(name)
    def remove(self, name):
        file_path = join(self.path, name)
        if isfile(file_path) and not isdir(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        #trash = self.sub("trash") if self.name is None else Folder("trash", self.base)
        #self.move(name, trash, True)
    def move(self, name, other, rename):
        other.ensure()
        src = self.slash(name)
        dst = other.slash(name)
        if isdir(src) or isdir(dst): exit()
        if not isfile(src): return
        while isfile(dst):
            if not rename: return
            dst = next_file_path(dst)
        try:
            shutil.move(src, dst)
        except:
            pass
    def copy(self, name, other):
        other.ensure()
        src = self.slash(name)
        dst = other.slash(name)
        if isdir(src) or isdir(dst): exit()
        if not isfile(src) or isfile(dst): return
        try:
            shutil.copyfile(src, dst)
        except:
            pass
            
    
top = Folder(None)
images = Folder("images")
all_image_names = images.image_names()
    
class Cat:
    def __init__(self, name):
        self.name = name
        self.yes = Folder(YES_ + name)
        self.no = Folder(NO_ + name)
        # self.num_yes = len(self.yes.image_names())
        # self.num_no = len(self.no.image_names())
    def result(self, name):
        other_yeses = [folder for folder in top.yeses() if folder.name != self.yes.name]
        if self.yes.has(name): return True
        if self.no.has(name): return False
        for other_yes in other_yeses:
            if other_yes.has(name): return False
        return None
        
all_categories = [
    Cat("odometer"),
    Cat("REGO_sticker"),
    Cat("REGO_plate"),
    Cat("VIN"),
    Cat("document"),
    Cat("mechanical"),
    Cat("exterior"),
    Cat("interior"),
    Cat("part"),
]
