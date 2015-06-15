#!/usr/bin/env python
# . s.ssmuse.dot /ssm/net/hpcs/201402/02/base /ssm/net/hpcs/201402/02/intel13sp1u2 /ssm/net/rpn/libs/15.2

"""
 Librmn Fstd grid helper functions

 @author: Stephane Chamberland <stephane.chamberland@ec.gc.ca>
"""
from . import RMNError
import numpy  as _np
from math import sqrt
from . import const as _rc
from . import base as _rb
from . import interp as _ri
from . import llacar as _ll

def decodeIG2dict(grtyp,ig1,ig2,ig3,ig4):
    """Decode encode grid values into a dict with meaningful labels
    
    params = decodeIG2dict(grtyp,ig1,ig2,ig3,ig4)
    
    Args:
        grtyp  : type of geographical projection (one of 'A', 'B', 'E', 'G', 'L', 'N', 'S')
        ig1    : first encode grid descriptor (int)
        ig2    : second encode grid descriptor (int)
        ig3    : third encode grid descriptor (int)
        ig4    : fourth encode grid descriptor (int)
    Returns:
        {
            'grtyp'  : type of geographical projection (one of 'Z','#','Y','U')
            'ig1'    : first encode grid descriptor (int)
            'ig2'    : second encode grid descriptor (int)
            'ig3'    : third encode grid descriptor (int)
            'ig4'    : fourth encode grid descriptor (int)
            'xg1'    : first decode grid descriptor (float)
            'xg2'    : second decode grid descriptor (float)
            'xg3'    : third decode grid descriptor (float)
            'xg4'    : fourth decode grid descriptor (float)
            ...
            list of other parameters is grtyp dependent
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    (xg1,xg2,xg3,xg4) = _rb.cigaxg(grtyp,ig1,ig2,ig3,ig4)
    params = decodeXG2dict(grtyp,xg1,xg2,xg3,xg4)
    params.update({
        'grtyp' : grtyp,
        'ig1' : ig1,
        'ig2' : ig2,
        'ig3' : ig3,
        'ig4' : ig4
        })
    return params


def decodeXG2dict(grtyp,xg1,xg2,xg3,xg4):
    """Put decode grid values into a dict with meaningful labels

    params = decodeXG2dict(grtyp,xg1,xg2,xg3,xg4)
    
    Args:
        grtyp  : type of geographical projection (one of 'A', 'B', 'E', 'G', 'L', 'N', 'S')
        xg1    : first decode grid descriptor (float)
        xg2    : second decode grid descriptor (float)
        xg3    : third decode grid descriptor (float)
        xg4    : fourth decode grid descriptor (float)
    Returns:
        {
            'grtyp'  : type of geographical projection (one of 'A', 'B', 'E', 'G', 'L', 'N', 'S')
            'xg1'    : first decode grid descriptor (float)
            'xg2'    : second decode grid descriptor (float)
            'xg3'    : third decode grid descriptor (float)
            'xg4'    : fourth decode grid descriptor (float)
            ...
            list of other parameters is grtyp dependent
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    grtyp = grtyp.strip().upper()
    params = {
        'grtyp' : grtyp,
        'xg1' : xg1,
        'xg2' : xg2,
        'xg3' : xg3,
        'xg4' : xg4
        }
    if grtyp.strip().upper() == 'L':
        params.update({
            'lat0' : xg1,
            'lon0' : xg2,
            'dlat' : xg3,
            'dlon' : xg4
            })
    elif grtyp == 'E':
        params.update({
            'xlat1' : xg1,
            'xlon1' : xg2,
            'xlat2' : xg3,
            'xlon2' : xg4
            })
    ## elif grtyp == 'F': #TODO
    ## elif grtyp == 'A': #TODO
    ## elif grtyp == 'B': #TODO
    elif grtyp== 'G':
        params.update({
            'glb'      : (int(xg1) == 0),
            'north'    : (int(xg1) != 2),
            'inverted' : (int(xg2) == 1)
            })
    elif grtyp in ('N','S'):
        params.update({
            'pi'   : xg1,
            'pj'   : xg2,
            'd60'  : xg3,
            'dgrw' : xg4,
            'north' : (params['grtyp'] == 'N')
            })        
    else:
        raise RMNError('decodeXG2dict: Grid type not yet supported %s' % (params['grtyp']))
    return params


def decodeGrid(gid):
    """Produce grid params dict as defGrid* fn, decoded from provided ezscint Id

    gridParams = decodeGrid(gid)
    
    Args:
        gid : ezscint grid-id (int)
    Returns:
        {
            'id'    : grid id, same as input arg
            'shape'  : (ni,nj) # dimensions of the grid
            'ni'     : first dimension of the grid
            'nj'     : second dimension of the grid
            'grtyp'  : type of geographical projection (one of 'Z','#','Y','U')
            'ig1'    : first grid descriptor
            'ig2'    : second grid descriptor
            'ig3'    : third grid descriptor
            'ig4'    : fourth grid descriptor
            'grref'  : grid ref type (one of 'A', 'B', 'E', 'G', 'L', 'N', 'S')
            'ig1ref' : first grid descriptor of grid ref
            'ig2ref' : second grid descriptor of grid ref
            'ig3ref' : third grid descriptor of grid ref
            'ig4ref' : fourth grid descriptor of grid ref
            ...
            list of other parameters is grtyp dependent,
            See defGrid_* specific function for details
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
     """
    params = _ri.ezgxprm(gid)
    params['nsubgrids'] = 1
    params['subgridid'] = [gid]
    params['grtyp'] = params['grtyp'].strip().upper()
    params['grref'] = params['grref'].strip().upper()
    if not params['grtyp'] in ('Z','#','Y','U'):
        params.update(decodeIG2dict(params['grtyp'],params['ig1'],params['ig2'],params['ig3'],params['ig4']))
    elif not params['grtyp'] in ('U'):
        params2 = decodeIG2dict(params['grref'],params['ig1ref'],params['ig2ref'],params['ig3ref'],params['ig4ref'])
        for k in ('grtyp','ig1','ig2','ig3','ig4'):
            del params2[k]
        params.update(params2)
        if params['grref'] == 'E':
            axes = _ri.gdgaxes(gid)
            params.update({
                'ax'    : axes['ax'],
                'ay'    : axes['ay']
                })
            (params['tag1'],params['tag2']) = getIgTags(params)
            params['tag3'] = 0
            (params['ig1'],params['ig2']) = (params['tag1'],params['tag2'])
            if params['grtyp'] in ('Z','#'):
                params.update({
                    'lat0' : axes['ay'][0,0],
                    'lon0' : axes['ax'][0,0],
                    'dlat' : axes['ay'][0,1] - axes['ay'][0,0],
                    'dlon' : axes['ax'][1,0] - axes['ax'][0,0]
                    })
            if params['grtyp'] in ('#'):
                (params['i0'],params['j0']) = (1,1)
                (params['ig3'],params['ig4']) = (1,1)
                (params['lni'],params['lnj']) = (params['ni'],params['nj'])
                params['lshape'] = params['shape']
            else:
                (params['ig3'],params['ig4']) = (params['tag3'],0)
        else:
            raise RMNError('decodeGrid: Grid type not yet supported %s(%s)' % (params['grtyp'],params['grref']))
    else:
        params['nsubgrids'] = _ri.ezget_nsubgrids(gid)
        params['subgridid'] = _ri.ezget_subgridids(gid)
        params['subgrid'] = []
        for gid2 in params['subgridid']:
            params['subgrid'].append(decodeGrid(gid2))
        for k in ('xlat1','xlon1','xlat2','xlon2','dlat','dlon','lat0','lon0'):
            params[k] = params['subgrid'][0][k]
        params['overlap'] = -45. - params['subgrid'][0]['lat0']
        params['version'] = params['ig1ref']
        params['axyname'] = '^>'
        params['axy'] = yyg_pos_rec(params['xlat1'],params['xlon1'],params['xlat2'],params['xlon2'],params['subgrid'][0]['ax'],params['subgrid'][0]['ay'])
    return params


def getIgTags(params):
    """Use grid params and CRC to define 2 grid tags
    
    (tag1,tag2) = setIgTags(params)
    
    Args:
        params     : grid parameters given as a dictionary (dict)
          {
            'xlat1' : lat of grid center in degrees (float)
            'xlon1' : lon of grid center in degrees (float)
            'xlat2' : lat of a 2nd ref. point in degrees (float)
            'xlon2' : lon of a 2nd ref. point in degrees (float)
            'ax'    : grid x-axes (numpy.ndarray)
            'ay'    : grid y-axes (numpy.ndarray)
         }
    Returns:
        (int,int) : 2 grid tags
    Raises:
        TypeError    on wrong input arg types
        EzscintError on any other error
    """
    a = params['ax'][:,0].tolist()
    a.extend(params['ay'][0,:].tolist())
    a.extend([params['xlat1'],params['xlon1'],params['xlat2'],params['xlon2']])
    a = [int(x*1000.) for x in a]
    aa = _np.array(a,dtype=_np.uint32)
    crc = _rb.crc32(0, aa)
    return (
        int(32768 + (crc       & 0xffff)),
        int(32768 + (crc >> 16 & 0xffff))
            )


def encodeGrid(params):
    """Define an FSTD grid with the provided parameters

    gridParams = encodeGrid(params)
    
    Args:
       params: grid parameters given as a dictionary (dict)
               at least 'grtyp' must be defined
               other parameters is grtyp dependent,
               See defGrid_* specific function for details
    Returns:
        {
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : grid dim along the x-axis (int)
            'nj'    : grid dim along the y-axis (int)
            'grtyp' : grid type (str)
            ...
            list of other parameters is grtyp dependent,
            See defGrid_* specific function for details
         }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    try:
        params['grtyp'] = params['grtyp'].strip().upper()
    except:
        raise RMNError('encodeGrid: grtyp must be provided')
    try:
        params['grref'] = params['grref'].strip().upper()
    except:
        params['grref'] = params['grtyp']
    if params['grtyp'] == 'L':
        return defGrid_L(params)
    elif params['grtyp'] == 'E':
        return defGrid_E(params)
    elif params['grtyp'] == 'G':
        return defGrid_G(params)
    elif params['grtyp'] in ('N','S'):
        return defGrid_PS(params)
    elif params['grtyp'] == 'U':
        return defGrid_YY(params)
    elif params['grtyp'] == 'Z' and  params['grref'] == 'E':
        return defGrid_ZE(params)
    elif params['grtyp'] == '#' and  params['grref'] == 'E':
        return defGrid_diezeE(params)
    else:
        raise RMNError('encodeGrid: Grid type not yet supported %s(%s)' % (params['grtyp'],params['grref']))
        
    
def defGrid_L(ni,nj=None,lat0=None,lon0=None,dlat=None,dlon=None,setGridId=True):
    """Defines an FSTD LatLon (cylindrical equidistant) Grid (LAM)

    gridParams = defGrid_L(ni,nj,lat0,lon0,dlat,dlon,setGridId)
    gridParams = defGrid_L(ni,nj,lat0,lon0,dlat,dlon)
    gridParams = defGrid_L(params,setGridId)
    gridParams = defGrid_L(params)

    Args:
        ni, nj     : grid dims (int)
        lat0, lon0 : lat, lon of SW grid corner in degrees (float)
        dlat, dlon : grid resolution/spacing along lat, lon axes in degrees (float)
        setGridId  : Flag for creation of gid, ezscint grid id (True or False)
        params     : above parameters given as a dictionary (dict)
    Returns:
        {
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : grid dim along the x-axis (int)
            'nj'    : grid dim along the y-axis (int)
            'grtyp' : grid type (str)
            'lat0'  : lat of SW grid corner in degrees (float)
            'lon0'  : lon of SW grid corner in degrees (float)
            'dlat'  : grid resolution/spacing along lat axe in degrees (float)
            'dlon'  : grid resolution/spacing along lon axe in degrees (float)
            'ig1'   : grid parameters, encoded (int)
            'ig2'   : grid parameters, encoded (int)
            'ig3'   : grid parameters, encoded (int)
            'ig4'   : grid parameters, encoded (int)
            'id'    : ezscint grid-id if setGridId==True, -1 otherwise (int)
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    params = {
        'ni'   : ni,
        'nj'   : nj,
        'lat0' : lat0,
        'lon0' : lon0,
        'dlat' : dlat,
        'dlon' : dlon
        }
    if isinstance(ni,dict):
        params.update(ni)
        try:
            setGridId = ni['setGridId']
        except:
            pass
    for k in ('ni','nj'):
        v = params[k]
        if not isinstance(v,int):
            raise TypeError('defGrid_L: wrong input data type for %s, expecting int, Got (%s)' % (k,type(v)))
        if v <= 0:
            raise ValueError('defGrid_L: grid dims must be >= 0, got %s=%d' % (k,v))
    for k in ('lat0','lon0','dlat','dlon'):
        v = params[k]
        if isinstance(v,int): v = float(v)
        if not isinstance(v,float):
            raise TypeError('defGrid_L: wrong input data type for %s, expecting float, Got (%s)' % (k,type(v)))
        params[k] = v
    params['grtyp'] = 'L'
    ig1234 = _rb.cxgaig(params['grtyp'],params['lat0'],params['lon0'],
                        params['dlat'],params['dlon'])
    params['ig1'] = ig1234[0]
    params['ig2'] = ig1234[1]
    params['ig3'] = ig1234[2]
    params['ig4'] = ig1234[3]
    params['id'] = _ri.ezqkdef(params) if setGridId else -1
    params['shape'] = (params['ni'],params['nj'])
    return params


def defGrid_E(ni,nj=None,xlat1=None,xlon1=None,xlat2=None,xlon2=None,setGridId=True):
    """Defines an FSTD Global, rotated, LatLon (cylindrical equidistant) Grid

    gridParams = defGrid_E(ni,nj,xlat1,xlon1,xlat2,xlon2,setGridId)
    gridParams = defGrid_E(ni,nj,xlat1,xlon1,xlat2,xlon2)
    gridParams = defGrid_E(params,setGridId)
    gridParams = defGrid_E(params)

    Args:
        ni, nj      : grid dims (int)
        xlat1,xlon1 : lat, lon of the grid center in degrees (float)
                      This defines, in rotated coor., (rlat,rlon) = (0.,180.)
                      on the rotated equator
                      The grid is defined, in rotated coor on
                      rlat: -90. to +90. degrees
                      rlon:   0. to 360. degrees
        xlat2,xlon2 : lat, lon of a 2nd ref. point in degrees (float)
                      This point is considered to be on the rotated equator,
                      east of xlat1,xlon1 (it thus defines the rotation)
        setGridId   : Flag for creation of gid, ezscint grid id (True or False)
        params      : above parameters given as a dictionary (dict)
    Returns:
        {
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : grid dim along the x-axis (int)
            'nj'    : grid dim along the y-axis (int)
            'grtyp' : grid type (str)
            'xlat1' : lat of grid center in degrees (float)
            'xlon1' : lon of grid center in degrees (float)
            'xlat2' : lat of a 2nd ref. point in degrees (float)
            'xlon2' : lon of a 2nd ref. point in degrees (float)
            'ig1'   : grid parameters, encoded (int)
            'ig2'   : grid parameters, encoded (int)
            'ig3'   : grid parameters, encoded (int)
            'ig4'   : grid parameters, encoded (int)
            'id'    : ezscint grid-id if setGridId==True, -1 otherwise (int)
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    params = {
        'ni'    : ni,
        'nj'    : nj,
        'xlat1' : xlat1,
        'xlon1' : xlon1,
        'xlat2' : xlat2,
        'xlon2' : xlon2
        }
    if isinstance(ni,dict):
        params.update(ni)
        try:
            setGridId = ni['setGridId']
        except:
            pass
    for k in ('ni','nj'):
        v = params[k]
        if not isinstance(v,int):
            raise TypeError('defGrid_E: wrong input data type for %s, expecting int, Got (%s)' % (k,type(v)))
        if v <= 0:
            raise ValueError('defGrid_E: grid dims must be >= 0, got %s=%d' % (k,v))
    for k in ('xlat1','xlon1','xlat2','xlon2'):
        try:
            v = params[k]
        except:
            raise TypeError('defGrid_E: provided incomplete grid description, missing: %s' % k)
        if isinstance(v,int): v = float(v)
        if not isinstance(v,float):
            raise TypeError('defGrid_E: wrong input data type for %s, expecting float, Got (%s)' % (k,type(v)))
        params[k] = v
    params['grtyp'] = 'E'
    ig1234 = _rb.cxgaig(params['grtyp'],params['xlat1'],params['xlon1'],
                        params['xlat2'],params['xlon2'])
    params['ig1'] = ig1234[0]
    params['ig2'] = ig1234[1]
    params['ig3'] = ig1234[2]
    params['ig4'] = ig1234[3]
    params['id'] = _ri.ezqkdef(params) if setGridId else -1
    params['shape'] = (params['ni'],params['nj'])
    return params


def defGrid_ZE(ni,nj=None,lat0=None,lon0=None,dlat=None,dlon=None,xlat1=None,xlon1=None,xlat2=None,xlon2=None,setGridId=True):
    """Defines an FSTD LAM, rotated, LatLon (cylindrical equidistant) Grid

    gridParams = defGrid_ZE(ni,nj,lat0,lon0,dlat,dlon,xlat1,xlon1,xlat2,xlon2,setGridId)
    gridParams = defGrid_ZE(ni,nj,lat0,lon0,dlat,dlon,xlat1,xlon1,xlat2,xlon2)
    gridParams = defGrid_ZE(params,setGridId)
    gridParams = defGrid_ZE(params)

    Args:
        ni, nj      : grid dims (int)
        lat0, lon0 : lat, lon of SW grid corner in degrees (rotated coor.) (float)
        dlat, dlon : grid resolution/spacing along lat, lon on rotated axes in degrees (float)
        xlat1,xlon1 : lat, lon of the grid center in degrees (float)
                      This defines, in rotated coor., (rlat,rlon) = (0.,180.)
                      on the rotated equator
                      The grid is defined, in rotated coor on
                      rlat: -90. to +90. degrees
                      rlon:   0. to 360. degrees
        xlat2,xlon2 : lat, lon of a 2nd ref. point in degrees (float)
                      This point is considered to be on the rotated equator,
                      east of xlat1,xlon1 (it thus defines the rotation)
        setGridId   : Flag for creation of gid, ezscint grid id (True or False)
        params      : above parameters given as a dictionary (dict)
    Returns:
        {
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : grid dim along the x-axis (int)
            'nj'    : grid dim along the y-axis (int)
            'grtyp' : grid type (Z) (str)
            'tag1'  : grid tag 1 (int)
            'tag2'  : grid tag 2 (int)
            'ig1'   : grid tag 1 (int), =tag1
            'ig2'   : grid tag 2 (int), =tag2
            'ig3'   : grid tag 3 (int)
            'ig4'   : grid tag 4, unused (set to 0) (int)
            'grref' : ref grid type (E) (str)
            'ig1ref' : ref grid parameters, encoded (int)
            'ig2ref' : ref grid parameters, encoded (int)
            'ig3ref' : ref grid parameters, encoded (int)
            'ig4ref' : ref grid parameters, encoded (int)
            'lat0'  : lat of SW grid corner in degrees (rotated coor.) (float)
            'lon0'  : lon of SW grid corner in degrees (rotated coor.) (float)
            'dlat'  : grid resolution/spacing along lat axe in degrees (float)
            'dlon'  : grid resolution/spacing along lon axe in degrees (float)
            'xlat1' : lat of grid center in degrees (float)
            'xlon1' : lon of grid center in degrees (float)
            'xlat2' : lat of a 2nd ref. point in degrees (float)
            'xlon2' : lon of a 2nd ref. point in degrees (float)
            'ax'    : points longitude, in rotated coor. (numpy,ndarray)
            'ay'    : points latitudes, in rotated coor. (numpy,ndarray)
            'id'    : ezscint grid-id if setGridId==True, -1 otherwise (int)
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    params = {
        'ni'    : ni,
        'nj'    : nj,
        'lat0' : lat0,
        'lon0' : lon0,
        'dlat' : dlat,
        'dlon' : dlon,
        'xlat1' : xlat1,
        'xlon1' : xlon1,
        'xlat2' : xlat2,
        'xlon2' : xlon2
        }
    if isinstance(ni,dict):
        params.update(ni)
        try:
            setGridId = ni['setGridId']
        except:
            pass
    params['grtyp'] = 'Z'
    params['grref'] = 'E'
    for k in ('ni','nj'):
        v = params[k]
        if not isinstance(v,int):
            raise TypeError('defGrid_ZE: wrong input data type for %s, expecting int, Got (%s)' % (k,type(v)))
        if v <= 0:
            raise ValueError('defGrid_ZE: grid dims must be >= 0, got %s=%d' % (k,v))
    for k in ('lat0','lon0','dlat','dlon'):
        v = params[k]
        if isinstance(v,int): v = float(v)
        if not isinstance(v,float):
            raise TypeError('defGrid_ZE: wrong input data type for %s, expecting float, Got (%s)' % (k,type(v)))
        params[k] = v
    for k in ('xlat1','xlon1','xlat2','xlon2'):
        try:
            v = params[k]
        except:
            raise TypeError('defGrid_ZE: provided incomplete grid description, missing: %s' % k)
        if isinstance(v,int): v = float(v)
        if not isinstance(v,float):
            raise TypeError('defGrid_ZE: wrong input data type for %s, expecting float, Got (%s)' % (k,type(v)))
        params[k] = v
    ig1234 = _rb.cxgaig(params['grref'],params['xlat1'],params['xlon1'],
                        params['xlat2'],params['xlon2'])
    params['ig1ref'] = ig1234[0]
    params['ig2ref'] = ig1234[1]
    params['ig3ref'] = ig1234[2]
    params['ig4ref'] = ig1234[3]

    params['ax'] = _np.empty((params['ni'],1),dtype=_np.float32,order='FORTRAN')
    params['ay'] = _np.empty((1,params['nj']),dtype=_np.float32,order='FORTRAN')
    for i in xrange(params['ni']):
        params['ax'][i,0] = params['lon0'] + float(i)*params['dlon']
    for j in xrange(params['nj']):
        params['ay'][0,j] = params['lat0'] + float(j)*params['dlat']

    params['ig1'] = ig1234[0]
    params['ig2'] = ig1234[1]
    params['ig3'] = ig1234[2]
    params['ig4'] = ig1234[3]
    
    params['id'] = _ri.ezgdef_fmem(params) if setGridId else -1

    (params['tag1'],params['tag2']) = getIgTags(params)
    params['tag3'] = 0
    
    (params['ig1'],params['ig2']) = (params['tag1'],params['tag2'])
    (params['ig3'],params['ig4']) = (params['tag3'],0)
    params['shape'] = (params['ni'],params['nj'])    
    return params


def defGrid_diezeE(ni,nj=None,lat0=None,lon0=None,dlat=None,dlon=None,xlat1=None,xlon1=None,xlat2=None,xlon2=None,lni=None,lnj=None,i0=None,j0=None,setGridId=True):
    """Defines an FSTD LAM, rotated, LatLon (cylindrical equidistant) Grid

    gridParams = defGrid_E(ni,nj,lat0,lon0,dlat,dlon,xlat1,xlon1,xlat2,xlon2,lni,lnj,i0,j0,setGridId)
    gridParams = defGrid_diezeE(ni,nj,lat0,lon0,dlat,dlon,xlat1,xlon1,xlat2,xlon2,lni,lnj,i0,j0)
    gridParams = defGrid_diezeE(params,setGridId)
    gridParams = defGrid_diezeE(params)

    Args:
        lni, lnj   : local grid tile dims (int)
        i0,   j0   : local tile position of first point in the full grid (int)
                     (Fotran convention, first point start at index 1)
        ni,   nj   : Full grid dims (int)
        lat0, lon0 : lat, lon of SW Full grid corner in degrees (rotated coor.) (float)
        dlat, dlon : grid resolution/spacing along lat, lon on rotated axes in degrees (float)
        xlat1,xlon1 : lat, lon of the grid center in degrees (float)
                      This defines, in rotated coor., (rlat,rlon) = (0.,180.)
                      on the rotated equator
                      The grid is defined, in rotated coor on
                      rlat: -90. to +90. degrees
                      rlon:   0. to 360. degrees
        xlat2,xlon2 : lat, lon of a 2nd ref. point in degrees (float)
                      This point is considered to be on the rotated equator,
                      east of xlat1,xlon1 (it thus defines the rotation)
        setGridId   : Flag for creation of gid, ezscint grid id (True or False)
        params      : above parameters given as a dictionary (dict)
    Returns:
        {
            'lshape' : (lni,lnj) # dimensions of the local grid tile
            'lni'   : local grid tile dim along the x-axis (int)
            'lnj'   : local grid tile dim along the y-axis (int)
            'i0'    : local tile x-position of first point in the full grid (int)
                      (Fotran convention, first point start at index 1)
            'j0'    : local tile y-position of first point in the full grid (int)
                      (Fotran convention, first point start at index 1)
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : Full grid dim along the x-axis (int)
            'nj'    : Full grid dim along the y-axis (int)
            'grtyp' : grid type (Z) (str)
            'tag1'  : grid tag 1 (int)
            'tag2'  : grid tag 2 (int)
            'ig1'   : grid tag 1 (int), =tag1
            'ig2'   : grid tag 2 (int), =tag2
            'ig3'   : i0
            'ig4'   : j0
            'grref' : ref grid type (E) (str)
            'ig1ref' : ref grid parameters, encoded (int)
            'ig2ref' : ref grid parameters, encoded (int)
            'ig3ref' : ref grid parameters, encoded (int)
            'ig4ref' : ref grid parameters, encoded (int)
            'lat0'  : lat of SW grid corner in degrees (rotated coor.) (float)
            'lon0'  : lon of SW grid corner in degrees (rotated coor.) (float)
            'dlat'  : grid resolution/spacing along lat axe in degrees (float)
            'dlon'  : grid resolution/spacing along lon axe in degrees (float)
            'xlat1' : lat of grid center in degrees (float)
            'xlon1' : lon of grid center in degrees (float)
            'xlat2' : lat of a 2nd ref. point in degrees (float)
            'xlon2' : lon of a 2nd ref. point in degrees (float)
            'ax'    : points longitude, in rotated coor. (numpy,ndarray)
            'ay'    : points latitudes, in rotated coor. (numpy,ndarray)
            'id'    : ezscint grid-id if setGridId==True, -1 otherwise (int)
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    setGridId0 = setGridId
    if isinstance(ni,dict):
        lni = ni['lni']
        lnj = ni['lnj']
        i0 = ni['i0']
        j0 = ni['j0']
        try:
            setGridId0 = ni['setGridId']
        except:
            pass
        ni['setGridId'] = False
    params = defGrid_ZE(ni,nj,lat0,lon0,dlat,dlon,xlat1,xlon1,xlat2,xlon2,setGridId=False)
    params.update({
        'grtyp' : 'Z',  #TODO: actual '#' crashes gdef_fmem
        'lshape' : (lni,lnj),
        'lni' : lni,
        'lnj' : lnj,
        'i0'  : i0,
        'j0'  : j0,
        'ig1' : params['ig1ref'],
        'ig2' : params['ig2ref'],
        'ig3' : params['ig3ref'],
        'ig4' : params['ig4ref']
        })
    params['id'] = _ri.ezgdef_fmem(params) if setGridId0 else -1
    params.update({
        'grtyp' : '#',
        'ig1' : params['tag1'],
        'ig2' : params['tag2'],
        'ig3' : params['i0'],
        'ig4' : params['j0']
        })
    return params


def defGrid_G(ni,nj=None,glb=True,north=True,inverted=False,setGridId=True):
    """Provide grid parameters to define an FSTD Gaussian Grid

    gridParams = gridParams_G(ni,nj,lat0,lon0,dlat,dlon,setGridId)
    gridParams = gridParams_G(ni,nj,lat0,lon0,dlat,dlon)
    gridParams = gridParams_G(params,setGridId)
    gridParams = gridParams_G(params)

    Args:
        ni, nj     : grid dims (int)
        glb        : True for Global grid coverage,
                     False for Hemispheric
        north      : (used only if glb==False)
                     True for northern hemisphere,
                     False for Southern
        inverted   : False, South -> North (pt (1,1) at grid bottom)
                     True, North -> South (pt (1,1) at grid top)
        setGridId  : Flag for creation of gid, ezscint grid id (True or False)
        params     : above parameters given as a dictionary (dict)
    Returns:
        {
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : grid dim along the x-axis (int)
            'nj'    : grid dim along the y-axis (int)
            'grtyp' : grid type (str)
            'glb'   : True for Global grid coverage, False for Hemispheric
            'north' : (used only if glb==False) True for northern hemisphere, False for Southern
            'inverted' : False, South -> North (pt (1,1) at grid bottom)
                         True,  North -> South (pt (1,1) at grid top)
            'ig1'   : grid parameters, encoded (int)
            'ig2'   : grid parameters, encoded (int)
            'ig3'   : grid parameters, encoded (int)
            'ig4'   : grid parameters, encoded (int)
            'id'    : ezscint grid-id if setGridId==True, -1 otherwise (int)
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    params = {
        'ni'   : ni,
        'nj'   : nj,
        'glb'   : glb,
        'north' : north,
        'inverted' : inverted
        }
    if isinstance(ni,dict):
        params.update(ni)
        try:
            setGridId = ni['setGridId']
        except:
            pass
    for k in ('ni','nj'):
        v = params[k]
        if not isinstance(v,int):
            raise TypeError('defGrid_G: wrong input data type for %s, expecting int, Got (%s)' % (k,type(v)))
        if v <= 0:
            raise ValueError('defGrid_G: grid dims must be >= 0, got %s=%d' % (k,v))
    params['grtyp'] = 'G'
    params['ig1'] = 0
    if not params['glb']:
        params['ig1'] = 1 if params['north'] else 2
    params['ig2'] = 1 if params['inverted'] else 0
    params['ig3'] = 0
    params['ig4'] = 0
    params['id'] = _ri.ezqkdef(params) if setGridId else -1
    params['shape'] = (params['ni'],params['nj'])
    return params


def defGrid_PS(ni,nj=None,north=True,pi=None,pj=None,d60=None,dgrw=0.,setGridId=True):
    """Define a Polar stereographic grid for the northern or southern hemisphere

    gridParams = defGrid_PS(ni,nj,north,pi,pj,d60,dgrw,setGridId)
    gridParams = defGrid_PS(ni,nj,north,pi,pj,d60,dgrw)
    gridParams = defGrid_PS(params,setGridId)
    gridParams = defGrid_PS(params)

    Args:
        ni, nj    : grid dims (int)
        pi        : Horizontal position of the pole, (float
                    in grid points, from bottom left corner (1,1).
                    (Fotran convention, first point start at index 1)
        pj        : Vertical position of the pole, (float
                    in grid points, from bottom left corner (1,1).
                    (Fotran convention, first point start at index 1)
        d60       : grid length, in meters, at 60deg. of latitude. (float)
        dgrw      : angle (between 0 and 360, +ve counterclockwise)
                    between the Greenwich meridian and the horizontal
                    axis of the grid. (float)
        north     : True for northern hemisphere,
                    False for Southern
        setGridId : Flag for creation of gid, ezscint grid id (True or False)
        params    : above parameters given as a dictionary (dict)
    Returns:
        {
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : grid dim along the x-axis (int)
            'nj'    : grid dim along the y-axis (int)
            'grtyp' : grid type (str)
            'pi'    : Horizontal position of the pole, (float
                      in grid points, from bottom left corner (1,1).
                      (Fotran convention, first point start at index 1)
            'pj'    : Vertical position of the pole, (float
                      in grid points, from bottom left corner (1,1).
                      (Fotran convention, first point start at index 1)
            'd60'   : grid length, in meters, at 60deg. of latitude. (float)
            'dgrw'  : angle (between 0 and 360, +ve counterclockwise)
                      between the Greenwich meridian and the horizontal
                      axis of the grid. (float)
            'north' : True for northern hemisphere,
                      False for Southern
            'ig1'   : grid parameters, encoded (int)
            'ig2'   : grid parameters, encoded (int)
            'ig3'   : grid parameters, encoded (int)
            'ig4'   : grid parameters, encoded (int)
            'id'    : ezscint grid-id if setGridId==True, -1 otherwise (int)
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    params = {
        'ni'   : ni,
        'nj'   : nj,
        'north' : north,
        'pi'    : pi, 
        'pj'    : pj,
        'd60'   : d60,
        'dgrw'  : dgrw
        }
    if isinstance(ni,dict):
        params.update(ni)
        try:
            setGridId = ni['setGridId']
        except:
            pass
    for k in ('ni','nj'):
        v = params[k]
        if not isinstance(v,int):
            raise TypeError('defGrid_PS: wrong input data type for %s, expecting int, Got (%s)' % (k,type(v)))
        if v <= 0:
            raise ValueError('defGrid_PS: grid dims must be >= 0, got %s=%d' % (k,v))
    for k in ('pi','pj','d60','dgrw'):
        try:
            v = params[k]
        except:
            raise TypeError('defGrid_PS: provided incomplete grid description, missing: %s' % k)
        if isinstance(v,int): v = float(v)
        if not isinstance(v,float):
            raise TypeError('defGrid_PS: wrong input data type for %s, expecting float, Got (%s)' % (k,type(v)))
        params[k] = v
    params['grtyp'] = 'N' if params['north'] else 'S'
    ig1234 = _rb.cxgaig(params['grtyp'],params['pi'],params['pj'],
                        params['d60'],params['dgrw'])
    params['ig1'] = ig1234[0]
    params['ig2'] = ig1234[1]
    params['ig3'] = ig1234[2]
    params['ig4'] = ig1234[3]
    params['id'] = _ri.ezqkdef(params) if setGridId else -1
    params['shape'] = (params['ni'],params['nj'])
    return params


def defGrid_YY(nj,overlap=0.,xlat1=0.,xlon1=180.,xlat2=0.,xlon2=270.,setGridId=True):
    """Defines a YIN/YAN grid composed of 2 rotated LatLon (cylindrical equidistant) Grids

    gridParams = defGrid_YY(nj,overlap,xlat1,xlon1,xlat2,xlon2,setGridId)
    gridParams = defGrid_YY(nj,overlap,xlat1,xlon1,xlat2,xlon2)
    gridParams = defGrid_YY(params,setGridId)
    gridParams = defGrid_YY(params)

    Args:
        nj          : YIN grid dims (int)
                      ni = (nj-1)*3+1
        overlap     : number of overlapping degree between the 2 grids (float)
        xlat1,xlon1 : lat, lon of the grid center in degrees (float)
                      This defines, in rotated coor., (rlat,rlon) = (0.,180.)
                      on the rotated equator on the YIN grid
                      The grid is defined, in rotated coor on
                      rlat: -90. to +90. degrees
                      rlon:   0. to 360. degrees
        xlat2,xlon2 : lat, lon of a 2nd ref. point in degrees (float)
                      This point is considered to be on the rotated equator,
                      east of xlat1,xlon1 on the YIN grid
                      (it thus defines the rotation)
        setGridId   : Flag for creation of gid, ezscint grid id (True or False)
        params      : above parameters given as a dictionary (dict)
    Returns:
        {
            'shape' : (ni,nj) # dimensions of the grid
            'ni'    : grid dim along the x-axis (int)
            'nj'    : grid dim along the y-axis (int)
            'overlap': number of overlapping degrees between the 2 grids (float)
            'grtyp' : grid type (U) (str)

            'tag1'  : grid tag 1 (int)
            'tag2'  : grid tag 2 (int)
            'ig1'   : grid tag 1 (int), =tag1
            'ig2'   : grid tag 2 (int), =tag2
            'ig3'   : grid tag 3 (int)
            'ig4'   : grid tag 4, unused (set to 0) (int)

            'grref' : ref grid type (F) (str)
            'ig1ref' : ref grid parameters, encoded (int)
            'ig2ref' : ref grid parameters, encoded (int)
            'ig3ref' : ref grid parameters, encoded (int)
            'ig4ref' : ref grid parameters, encoded (int)
            'dlat'  : grid resolution/spacing along lat axe in degrees (float)
            'dlon'  : grid resolution/spacing along lon axe in degrees (float)
            'xlat1' : lat of grid center in degrees (float)
            'xlon1' : lon of grid center in degrees (float)
            'xlat2' : lat of a 2nd ref. point in degrees (float)
            'xlon2' : lon of a 2nd ref. point in degrees (float)
            'axy'   : positional record ('^>') (numpy,ndarray)
            'id'    : ezscint grid-id if setGridId==True, -1 otherwise (int)
            'nsubgrids' : number of subgrids =2 (int)
            'subgridid' : list of ezscint subgrid-id if setGridId==True, -1 otherwise (list of 2 int)
            'subgrid'   : params for each subgrid (list of 2 dict)
        }
    Raises:
        TypeError  on wrong input arg types
        ValueError on invalid input arg value
        RMNError   on any other error
    """
    params = {
        'nj'    : nj,
        'overlap' : overlap,
        'xlat1' : xlat1,
        'xlon1' : xlon1,
        'xlat2' : xlat2,
        'xlon2' : xlon2
        }
    if isinstance(nj,dict):
        params.update(nj)
        try:
            setGridId = ni['setGridId']
        except:
            pass
    for k in ('nj',):
        v = params[k]
        if not isinstance(v,int):
            raise TypeError('defGrid_YY: wrong input data type for %s, expecting int, Got (%s)' % (k,type(v)))
        if v <= 0:
            raise ValueError('defGrid_YY: grid dims must be >= 0, got %s=%d' % (k,v))
    for k in ('xlat1','xlon1','xlat2','xlon2','overlap'):
        v = params[k]
        if isinstance(v,int): v = float(v)
        if not isinstance(v,float):
            raise TypeError('defGrid_YY: wrong input data type for %s, expecting float, Got (%s)' % (k,type(v)))
        params[k] = v
    ni = (params['nj']-1)*3 + 1
    lon0 =  45. - 3.*params['overlap']
    lon1 = 315. + 3.*params['overlap']
    lat0 = -45. -    params['overlap']
    lat1 =  45. +    params['overlap']
    (dlat,dlon) = ((lat1-lat0)/float(nj-1), (lon1-lon0)/float(ni-1))
    version_uencode = 1
    family_uencode_S = 'F'
    params.update({
        'grtyp'     : 'U',
        'grref'     : family_uencode_S,
        'version'   : version_uencode,
        'ig1ref'    : version_uencode,
        'ig2ref'    : 0,
        'ig3ref'    : 0,
        'ig4ref'    : 0,
        'ni'        : ni,
        'dlat'      : dlat,
        'dlon'      : dlon,
        'lon0'      : lon0,
        'lat0'      : lat0,
        'nsubgrids' : 2,
        'subgridid' : [],
        'subgrid'   : []
        })
    (xlat1,xlon1,xlat2,xlon2) = (params['xlat1'],params['xlon1'],params['xlat2'],params['xlon2'])
    params['subgrid'].append(
        defGrid_ZE(params['ni'],params['nj'],lat0,lon0,dlat,dlon,xlat1,xlon1,xlat2,xlon2,setGridId)
        )
    (xlat1,xlon1,xlat2,xlon2) = yyg_yangrot_py(xlat1,xlon1,xlat2,xlon2)
    params['subgrid'].append(
        defGrid_ZE(params['ni'],params['nj'],lat0,lon0,dlat,dlon,xlat1,xlon1,xlat2,xlon2,setGridId)
        )
    params['subgridid'].append(params['subgrid'][0]['id'])
    params['subgridid'].append(params['subgrid'][1]['id'])
    params['id'] = _ri.ezgdef_supergrid(params['ni'], params['nj'], params['grtyp'], params['grref'], params['version'],params['subgridid'])
    params['axy'] = yyg_pos_rec(params['xlat1'],params['xlon1'],params['xlat2'],params['xlon2'],params['subgrid'][0]['ax'],params['subgrid'][0]['ay'])
    params['axyname'] = '^>'
    return params


#TODO: write in C (modelutils's C shared lib): llacar, cartall, yyg_yangrot, yyg_pos_rec
def yyg_yangrot_py(yinlat1, yinlon1, yinlat2, yinlon2):
    """Compute the rotation for the Yang grid using the rotation from Yin

    (yanlat1, yanlon1, yanlat2, yanlon2) = 
        yyg_yangrot_py(yinlat1, yinlon1, yinlat2, yinlon2)
        
    Args:
        yinlat1, yinlon1, yinlat2, yinlon2
    Returns:
        (yanlat1, yanlon1, yanlat2, yanlon2)
    Raises:
        TypeError  on wrong input arg types    
    """
    xyz1 = _ll.llacar_py(yinlon1, yinlat1)
    xyz2 = _ll.llacar_py(yinlon2, yinlat2)
    a = (xyz1[0]*xyz2[0]) + (xyz1[1]*xyz2[1]) + (xyz1[2]*xyz2[2])
    b = sqrt(((xyz1[1]*xyz2[2]) - (xyz2[1]*xyz1[2]))**2
             +  ((xyz2[0]*xyz1[2]) - (xyz1[0]*xyz2[2]))**2
             +  ((xyz1[0]*xyz2[1]) - (xyz2[0]*xyz1[1]))**2)
    c = sqrt( xyz1[0]**2 + xyz1[1]**2 + xyz1[2]**2 )
    d = sqrt( ( ( (a*xyz1[0]) - xyz2[0] ) / b )**2 + \
              ( ( (a*xyz1[1]) - xyz2[1] ) / b )**2 + \
              ( ( (a*xyz1[2]) - xyz2[2] ) / b )**2  )
    rot = _np.empty((3,3),dtype=_np.float32)
    rot[0,0] =  -xyz1[0]/c
    rot[0,1] =  -xyz1[1]/c
    rot[0,2] =  -xyz1[2]/c
    rot[1,0] = ( ((a*xyz1[0]) - xyz2[0]) / b)/d
    rot[1,1] = ( ((a*xyz1[1]) - xyz2[1]) / b)/d
    rot[1,2] = ( ((a*xyz1[2]) - xyz2[2]) / b)/d
    rot[2,0] = ( (xyz1[1]*xyz2[2]) - (xyz2[1]*xyz1[2]))/b
    rot[2,1] = ( (xyz2[0]*xyz1[2]) - (xyz1[0]*xyz2[2]))/b
    rot[2,2] = ( (xyz1[0]*xyz2[1]) - (xyz2[0]*xyz1[1]))/b
    #Get transpose of rotation
    invrot = rot.T
    #Find the centre of Yang grid through Yin by setting
    #And set the rotation for Yang grid with respect to Yin
    (xlat1,xlon1,xlat2,xlon2) = (0.,0.,90,0.)
    #Obtain the cartesian coordinates
    xyz1 = _ll.llacar_py(xlon1, xlat1)
    xyz2 = _ll.llacar_py(xlon2, xlat2)
    xyz3 = [0.,0.,0.]
    xyz4 = [0.,0.,0.]
    for i in xrange(3):
        xyz3[i] = 0.
        xyz4[i] = 0.
        for j in xrange(3):
            xyz3[i] = xyz3[i] + invrot[i,j]*xyz1[j]
            xyz4[i] = xyz4[i] + invrot[i,j]*xyz2[j]
    #Obtain the real geographic coordinates
    (xlon1,xlat1) = _ll.cartall_py(xyz3)
    (xlon2,xlat2) = _ll.cartall_py(xyz4)
    if (xlon1 >= 360.): xlon1 -= 360.
    if (xlon2 >= 360.): xlon2 -= 360.
    return (xlat1,xlon1,xlat2,xlon2)


def yyg_pos_rec(yinlat1, yinlon1, yinlat2, yinlon2,ax,ay):
    """Pack grid description value into the ^> record descriptor of the YY grid

    axy = yyg_pos_rec(yinlat1, yinlon1, yinlat2, yinlon2,ax,xy)

    Args:
        yinlat1,yinlon1 : lat, lon of the YIN grid center in degrees (float)
                      This defines, in rotated coor., (rlat,rlon) = (0.,180.)
                      on the rotated equator
                      The grid is defined, in rotated coor on
                      rlat: -90. to +90. degrees
                      rlon:   0. to 360. degrees
        yinlat2,yinlon2 : lat, lon of a 2nd YIN ref. point in degrees (float)
                      This point is considered to be on the rotated equator,
                      east of xlat1,xlon1 (it thus defines the rotation)
        ax : points longitude of the YIN grid, in rotated coor.(numpy.ndarray)
        ay : points latitudes of the YIN grid, in rotated coor.(numpy.ndarray)
    Returns:
        numpy.ndarray, positional record describing the yy-grid
    """
    vesion_uencode    = 1
    family_uencode_S = 'F'
    (yanlat1,yanlon1,yanlat2,yanlon2) = \
            yyg_yangrot_py(yinlat1, yinlon1, yinlat2, yinlon2)
    ni = ax.size
    nj = ay.size
    naxy = 5 + 2*(10+ni+nj)
    axy = _np.empty(naxy,dtype=_np.float32)
    axy[0 ] = ord(family_uencode_S)
    axy[1 ] = vesion_uencode
    axy[2 ] = 2 # 2 grids (Yin & Yang)
    axy[3 ] = 1 # the 2 grids have same resolution
    axy[4 ] = 1 # the 2 grids have same area extension on the sphere
    #YIN
    sindx = 5
    axy[sindx  ] = ni
    axy[sindx+1] = nj
    axy[sindx+2] = ax[0,0]
    axy[sindx+3] = ax[ni-1,0]
    axy[sindx+4] = ay[0,0]
    axy[sindx+5] = ay[0,nj-1]
    axy[sindx+6] = yinlat1
    axy[sindx+7] = yinlon1
    axy[sindx+8] = yinlat2
    axy[sindx+9] = yinlon2
    axy[sindx+10   :sindx+10+ni   ] = ax[0:ni,0]
    axy[sindx+10+ni:sindx+10+ni+nj] = ay[0   ,0:nj]
    #YAN
    sindx = sindx+10+ni+nj
    axy[sindx  ] = ni
    axy[sindx+1] = nj
    axy[sindx+2] = ax[0,0]
    axy[sindx+3] = ax[ni-1,0]
    axy[sindx+4] = ay[0,0]
    axy[sindx+5] = ay[0,nj-1]
    axy[sindx+6] = yanlat1
    axy[sindx+7] = yanlon1
    axy[sindx+8] = yanlat2
    axy[sindx+9] = yanlon2
    axy[sindx+10    :sindx+10+ni  ] = ax[0:ni,0]
    axy[sindx+10+ni:sindx+10+ni+nj] = ay[0   ,0:nj]
    return axy


# =========================================================================

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# -*- Mode: C; tab-width: 4; indent-tabs-mode: nil -*-
# vim: set expandtab ts=4 sw=4:
# kate: space-indent on; indent-mode cstyle; indent-width 4; mixedindent off;