#!/usr/bin/env python
"""
   Module ftnnml contains the classes used to manipulate fortran namelist files
   @author: Stephane Chamberland <stephane.chamberland@ec.gc.ca>
"""
import re,sys

__VERSION__     = '1.0.0'
__LASTUPDATED__ = '2015-02-27'

isListType   = lambda x: type(x) in (type([]),type((1,)))
isStringType = lambda x: type(x) == type("")
cleanName    = lambda x: x.lower().replace('\n',' ').strip()

class FtnNmlObj(object):
    """Fortran Namlist container base class (need to be subclassed)
    """
    allowedSubClass = None
    (splitPattern, matchStartPattern, matchEndPattern)  = (None, None, None)

    @classmethod
    def encode(thisclass,data):
        """Encode a strng before parsing"""
        return data
    
    @classmethod
    def decode(thisclass,data):
        """Decode what have been encoded with encode"""
        return data
    
    @classmethod
    def _parseSubContent(thisclass,mystr):
        """Deffer parsing to allowedSubClass"""
        mystr2 = thisclass.decode(mystr)
        return (thisclass.allowedSubClass.parseToList(mystr2) \
            if thisclass.allowedSubClass \
            else mystr2)

    @classmethod
    def parseToList(thisclass,mystr):
        """Parse string"""
        mystr2 = thisclass.encode(mystr)
        myitemList = [mystr2]
        if thisclass.splitPattern:
            myitemList = [item.replace("\x01",'\n') for item in re.split(thisclass.splitPattern,mystr2)]
        (myitem, mySubClassObj, listdata) = ('', None, [])
        for myline in myitemList:
            (m0, m1) = (None, None)
            if thisclass.matchStartPattern:
                m0 = re.match(thisclass.matchStartPattern,myline)
            if m0:
                if mySubClassObj:
                    mySubClassObj.set(thisclass._parseSubContent(myitem))
                    listdata.append(mySubClassObj)
                elif len(myitem) > 0:
                    listdata.append(thisclass.decode(myitem))
                (myitem, mySubClassObj) = ('', thisclass(''))
                for mykey in m0.groupdict().keys():
                    if mykey in ('strStart','name'):
                        mySubClassObj.rename(m0.group(mykey))
                    else:
                        mySubClassObj.prop[mykey] = m0.group(mykey)
            else:
                if thisclass.matchEndPattern:
                    m1 = re.match(thisclass.matchEndPattern,myline)
                if m1 and mySubClassObj:
                    junk = ''
                    for mykey in m1.groupdict().keys():
                        if    mykey == 'data': myitem += m1.group(mykey)
                        elif  mykey == 'junk': junk   += m1.group(mykey)
                        else: mySubClassObj.prop[mykey] = m1.group(mykey)
                    mySubClassObj.set(thisclass._parseSubContent(myitem))
                    listdata.append(mySubClassObj)
                    if junk: listdata.append(thisclass.decode(junk))
                    (myitem, mySubClassObj) = ('', None)
                else:
                    myitem += myline
        if mySubClassObj:
            mySubClassObj.set(thisclass._parseSubContent(myitem))
            listdata.append(mySubClassObj)
        elif len(myitem) > 0:
            listdata.append(thisclass.decode(myitem))
        return listdata

    @classmethod
    def prepStr(thisclass,mystr,clean=False,uplowcase=None):
        changeCase = lambda x: x
        if uplowcase: 
            changeCase = lambda x: x.lower()
            if isStringType(uplowcase) and uplowcase[0].lower() == 'u':
                changeCase = lambda x: x.upper()                
        return changeCase(mystr.lstrip() if clean else mystr)

    def __init__(self,name):
        (self.name, self.data) = (name, [])
        self.prop = { #Start SepS Sep1 data End SepE
            'strStart' : name,
            'strSepS'  : '',
            'strSep1'  : '',
            'strEnd'   : '',
            'strSepE'  : '',
           }

    def rename(self,name):
        """Properly set name of object (please avoid obj.name = 'name')"""
        (self.name, self.prop['strStart']) = (cleanName(name), name)

    def get(self,name=None):
        """Return sub object with given name
           return the list of contained objects otherwise"""
        if not name: return self.data
        try:
            return self.data[self.keyIndex(name)]
        except:
            sys.stderr.write('Known Keys:'+repr(self.keys()))
            raise KeyError(" (%s) Oops! get, Key not found: %s" % (self.__class__.__name__,name))

    def set(self,namedata,data=None):
        """Set sub object data with given name
           replace the list of contained objects otherwise"""
        name = (namedata if data else None)
        if not data: data = namedata
        if name: self.get(name).set(data)
        else:    self.data = (data if isListType(data) else [data])

    def add(self,data=None):
        if not isinstance(data,self.allowedSubClass):
            raise TypeError(" (%s) Oops! add, provided data is of wrong type: %s(accepting: %s)" % (self.__class__.__name__,str(type(data)),str(self.allowedSubClass)))
        if cleanName(data.name) in self.keys():
            raise KeyError(" (%s) Oops! add, Key already exists: %s" % (self.__class__.__name__,data.name))
        self.data.append(data)
    
    def rm(self,name=None):
        """Delete sub object with given name
           delete all contained objects otherwise"""
        if not name:
            self.data = []
        else:
            try:
                del self.data[self.keyIndex(name)]
            except:
                raise KeyError(" (%s) Oops! rm, Key not found: %s" % (self.__class__.__name__,name))

    def keyIndex(self,name):
        (name2, myindex) = (cleanName(name), -1)
        for item in self.data:
            myindex += 1
            if isinstance(item,FtnNmlObj) and item.name == name2:
                return myindex
        raise KeyError(" (%s) Oops! keyIndex, Key not found: %s" % (self.__class__.__name__,name))
       
    def keys(self):
        """Return list of keys (contained objects names)"""
        return [item.name for item in self.data if isinstance(item,FtnNmlObj) and item.name]

    def __repr__(self):
        return "%s(%s,%s,%s,%s,d=%s,%s,%s)" % \
            (self.__class__.__name__,repr(self.name),\
             repr(self.prop['strStart']),\
             repr(self.prop['strSepS']),\
             repr(self.prop['strSep1']),\
             repr(self.data),\
             repr(self.prop['strEnd']),
             repr(self.prop['strSepE'])\
                )

    def __str__(self):
        return self.toStr()
          
    def startStr(self,clean=False,uplowcase=None):
        return self.prepStr(self.prop['strStart']+self.prop['strSepS'],clean,uplowcase)
    def sepStr(self,clean=False,uplowcase=None):
        return self.prepStr(self.prop['strSep1'],clean,uplowcase)
    def endStr(self,clean=False,uplowcase=None):
        return self.prepStr(self.prop['strEnd']+self.prop['strSepE'],clean,uplowcase)

    def _myToStr(self,data,clean=False,uplowcase=None,updnsort=None):
        if isinstance(data,FtnNmlObj):
            return data.toStr(clean,uplowcase,updnsort)
        else:
            return self.prepStr(str(data),clean,uplowcase)
            
    def toStr(self,clean=False,uplowcase=None,updnsort=None):
        """Return String representation of the FtnNml Object, recursively"""
        if updnsort: clean=True
        data = (self.data if isListType(self.data) else [self.data])
        if clean: data = [s for s in data if type(s) != type(' ')]
        return self.startStr(clean,uplowcase) \
            + self.sepStr(clean,uplowcase) \
            + ''.join([self._myToStr(s,clean,uplowcase,updnsort) for s in data]) \
            + self.endStr(clean,uplowcase)\

    
class FtnNmlVal(FtnNmlObj):
    """Fortran Namlist value container
    """

    @classmethod
    def parseToList(thisclass,mystr):
        if not mystr: return ['']
        m = re.match(r'^([\s\t\n]*)([\w\W]+?)([\s\t\n,]*)$',mystr,re.I)
        if m:
            return [s for s in [str(m.group(1)),thisclass(str(m.group(2))),str(m.group(3))] if s]
        else:
            return [thisclass(str(mystr))]

    def __init__(self,value):
        FtnNmlObj.__init__(self,'v')
        self.data = value

    def __repr__(self):
        return "%s(d=%s)" % (self.__class__.__name__,repr(self.data))

    def toStr(self,clean=False,uplowcase=None,updnsort=None):
        data = (self.data[0] if isListType(self.data) else self.data)
        if clean: return str(data).replace('\n','')
        else:     return str(data)
        
    def rename(self,name):
        pass
    

class FtnNmlKeyVal(FtnNmlObj):
    """Fortran Namlist key=value container
    """
    
    allowedSubClass = FtnNmlVal
    splitPattern      = r'([\s\t]*\w+[\s\t]*=[\s\t]*)'
    matchStartPattern = r'^(?P<strStart>[\s\t]*\w+[\s\t]*)(?P<strSep1>=[\s\t]*)$'
    matchEndPattern   = r'^(?P<data>[\w\W]+)(?P<strEnd>[,\n])(?P<junk>[,\n\t\s]*)$'

    @classmethod
    def encode(thisclass,data):
        return re.sub(r'("[^"]+?"|\'[^\']+?\')', lambda m: m.group(0).replace("=", "\x00"), data.replace('\n',"\x01"))
    
    @classmethod
    def decode(thisclass,data):
        return data.replace("\x00","=").replace("\x01",'\n')

    def __init__(self,name,data=None):
        FtnNmlObj.__init__(self,name)
        self.prop['strSep1'] = '='
        self.prop['strEnd']  = ',\n'
        if data: self.set(data)

    def startStr(self,clean=False,uplowcase=None):
        if clean: return self.prepStr(self.name,clean,uplowcase)
        else:     return FtnNmlObj.startStr(self,clean,uplowcase)
        
    def sepStr(self,clean=False,uplowcase=None):
        if clean: return '='
        else:     return FtnNmlObj.sepStr(self,clean,uplowcase)
        
    def endStr(self,clean=False,uplowcase=None):
        if clean: return '\n'
        else:     return FtnNmlObj.endStr(self,clean,uplowcase)


class FtnNmlSection(FtnNmlObj):
    """Fortran Namlist 'namelist' container
    """
    
    allowedSubClass = FtnNmlKeyVal
    splitPattern      = r'([^\n]*\n)'
    matchStartPattern = r'^(?P<strStart>[\s\t]*&[^\s\t]+[\s\t]*)(?P<strSepS>\n)$'
    matchEndPattern   = r'^(?P<strEnd>[\s\t]*/[\s\t]*)(?P<strSepE>\n)$'

    def __init__(self,name):
        FtnNmlObj.__init__(self,name)
        self.prop['strStart'] = '&'+self.name
        self.prop['strSepS']  = '\n'
        self.prop['strEnd']   = '/'
        self.prop['strSepE']  = '\n'

    def rename(self,name):
        ## if re.match(self.matchStartPattern,name): #TODO
        if re.match('(&|[^&\w]&)',name):
            self.prop['strStart'] = name
        else:
            self.prop['strStart'] = '&'+name.lstrip().replace('\n','')
        self.name = cleanName(self.prop['strStart'].replace('&',''))


class FtnNmlFile(FtnNmlObj):
    """Fortran Namlist file container
    """

    allowedSubClass = FtnNmlSection
    
    @classmethod
    def parseToList(thisclass,mystr):
        return thisclass._parseSubContent(mystr)
        
    def __init__(self,name,fromFile=True):
        FtnNmlObj.__init__(self,name)
        self.prop['strStart'] = ''
        if fromFile: self.read(name)

    def parse(self,mystr):
        self.data = self.__class__.parseToList(mystr)

    def read(self,filename):
        """Read and parse file"""
        rawdata = ""
        try:
            fd = open(filename,"rb")
            try:     rawdata = "".join(fd.readlines())
            finally: fd.close()
        except IOError:
            raise IOError(" Oops! File does not exist or is not readable: %s" % (filename))
        self.parse(rawdata)

    def write(self,filename,clean=False,uplowcase=None,updnsort=None):
        """Write nml to file"""
        try:
            fd = open(filename,"wb")
            try:
                fd.write(self.toStr(clean,uplowcase,updnsort))
            except IOError:
                raise IOError(" Oops! Cannot wrtie to file: %s" % (filename))
            finally:
                fd.close()
        except IOError:
            raise IOError(" Oops! Cannot open file: %s" % (filename))
        
        

if __name__ == '__main__':
    #TODO: base class on list or dict
    #TODO: itf consistenncy (name,data) in set,get,rename,rm,add,__init__
    #TODO: data should be converted to list if not already
    #TODO: implement sort
    #TODO: doctests

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    filename = 'gem_settings.nml'
    b = FtnNmlFile(filename)
    print b
    print repr(b)

    #T: get
    print '---- List of nml'
    mynmls = b.keys()
    print filename+': ',', '.join(mynmls)
    print '---- List of var per nml'
    for nmlkey in mynmls:
        nml = b.get(nmlkey)
        mykeys = nml.keys()
        print '&'+nml.name+': '+', '.join(mykeys)
    print '---- List of values'
    for nmlkey in mynmls:
        nml = b.get(nmlkey)
        mykeys = nml.keys()
        for varkey in mykeys:
            kv = nml.get(varkey)
            val = kv.get('v')
            #valstr = str(val) #equivalent to: val.toStr()
            valstr = val.toStr(clean=True)
            print '&'+nml.name+'/'+varkey+'='+valstr
    
    #T: set 
    print '---- Change value'
    val = b.get('gem_cfgs').get('lctl_debug_l').get('v')
    print '&gem_cfgs/lctl_debug_l= '+str(val)
    val.set('.T.')
    print '&gem_cfgs/lctl_debug_l= '+str(val)
    print '---- Change var name'
    kv = b.get('gem_cfgs').get('hyb')
    print [kv.name,kv.prop['strStart']]
    kv.rename('levels')
    print [kv.name,kv.prop['strStart']]
    print '---- Change nml name'
    nml = b.get('gem_cfgs')
    print [nml.name,nml.prop['strStart']]
    nml.rename('sps_cfgs')
    print [nml.name,nml.prop['strStart']]
    
    #T: del
    print '---- Delete nml var'
    nml = b.get('sps_cfgs')
    print '&'+nml.name+': '+', '.join(nml.keys())
    nml.rm('sol_type2_s')
    nml.rm('etiket')
    print '&'+nml.name+': '+', '.join(nml.keys())
    print '---- Delete nml'
    print filename+': ',', '.join(b.keys())
    b.rm('grid_gu')
    print filename+': ',', '.join(b.keys())
        
    #T: add
    print repr(b)
    print '---- Add nml var'
    nml = b.get('sps_cfgs')
    print '&'+nml.name+': '+', '.join(nml.keys())
    nml.add(FtnNmlKeyVal('newvar',FtnNmlVal(1)))
    nml.add(FtnNmlKeyVal('n2',FtnNmlVal(4)))
    print '&'+nml.name+': '+', '.join(nml.keys())
    print '---- Add nml'
    print filename+': ',', '.join(b.keys())
    b.add(FtnNmlSection('mytoto'))
    print filename+': ',', '.join(b.keys())
    nml = b.get('mytoto')
    nml.add(FtnNmlKeyVal('totavar',FtnNmlVal('w')))
    
    print '----'
    print b
    print b.toStr(clean=True)
    print repr(b)
    
    ## ## import doctest
    ## ## doctest.testmod()
    ## ## verbose = 0
    ## ## a = FtnNmlFile('gem_settings.nml')


# -*- Mode: C; tab-width: 4; indent-tabs-mode: nil -*-
# vim: set expandtab ts=4 sw=4:
# kate: space-indent on; indent-mode cstyle; indent-width 4; mixedindent off;