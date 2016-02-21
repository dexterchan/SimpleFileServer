import os

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree


class PathItem:
    def __init__(self,name,relativePath,isFile):
        self.name=name
        self.relativePath=relativePath
        self.isFile=isFile
    
    def setURLPath(self, urlpath):
        self.UrlPath=urlpath

    def getURLPath(self):
        return self.UrlPath

def listPath(basepath, relativepath):
    abspath = os.path.join(basepath,relativepath)
    outputLst = []
    try:
        lst=os.listdir(abspath)
    except OSError:
        raise OSError
    else:
        for name in lst:
            fn=os.path.join(relativepath,name)
            abspath=os.path.join(basepath,fn)
            isFile=True
            if (os.path.isdir(abspath)):
                isFile=False
            else:
                isFile=True
            outputLst.append(PathItem(name,fn,isFile))
    return outputLst
            
