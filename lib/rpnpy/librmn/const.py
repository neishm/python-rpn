#!/usr/bin/env python
# -*- coding: utf-8 -*-
# . s.ssmuse.dot /ssm/net/hpcs/201402/02/base \
#                /ssm/net/hpcs/201402/02/intel13sp1u2 /ssm/net/rpn/libs/15.2
# Author: Stephane Chamberland <stephane.chamberland@canada.ca>
# Copyright: LGPL 2.1

"""
Module librmn_const defines a set of helper constants to make code
using the librmn module more readable.
"""
import numpy  as _np

#=== primitives ===
#<source lang=python>
## Python dict with wkoffit file type codes
WKOFFIT_TYPE_LIST = { #TODO:
    'INEXISTANT' : -3,
    'VIDE' : -2,
    'INCONNU' : -1,
    'STANDARD RANDOM 89' : 1,
    'STANDARD SEQUENTIEL 89' : 2,
    'STANDARD SEQUENTIEL FORTRAN 89' : 3,
    'CCRN' : 4,
    'CCRN-RPN' : 5,
    'BURP' : 6,
    'GRIB' : 7,
    'BUFR' : 8,
    'BLOK' : 9,
    'FORTRAN' : 10,
    'COMPRESS' : 11,
    'GIF89' : 12,
    'GIF87' : 13,
    'IRIS' : 14,
    'JPG' : 15,
    'KMW' : 16,
    'PBM' : 17,
    'PCL' : 18,
    'PCX' : 19,
    'PDSVICAR' : 20,
    'PM' : 21,
    'PPM' : 22,
    'PS' : 23,
    'KMW_' : 24,
    'RRBX' : 25,
    'SUNRAS' : 26,
    'TIFF' : 27,
    'UTAHRLE' : 28,
    'XBM' : 29,
    'XWD' : 30,
    'ASCII' : 31,
    'BMP' : 32,
    'STANDARD RANDOM 98' : 33,
    'STANDARD SEQUENTIEL 98' : 34,
    'NETCDF' : 35
    }

WKOFFIT_TYPE_LIST_INV = dict([(v, k) for k, v in WKOFFIT_TYPE_LIST.items()])
#</source>
#=== base ===

#<source lang=python>
NEWDATE_PRINT2TRUE  = 2
NEWDATE_TRUE2PRINT  = -2
NEWDATE_PRINT2STAMP = 3
NEWDATE_STAMP2PRINT = -3

NEWDATE_OPT_360DAYS   = 'year=360_day'
NEWDATE_OPT_365DAYS   = 'year=365_day'
NEWDATE_OPT_GREGORIAN = 'year=gregorian'
#</source>

#=== fstd98/fstd98 ===

#==== fstopt (options) ====

#<source lang=python>
FSTOP_GET = 1
FSTOP_SET = 0

FSTOP_MSGLVL    = "MSGLVL"
FSTOP_TOLRNC    = "TOLRNC"
FSTOP_PRINTOPT  = "PRINTOPT"
FSTOP_TURBOCOMP = "TURBOCOMP"

FSTOPI_MSG_DEBUG   = 0
FSTOPI_MSG_INFO    = 2
FSTOPI_MSG_WARNING = 4
FSTOPI_MSG_ERROR   = 6
FSTOPI_MSG_FATAL   = 8
FSTOPI_MSG_SYSTEM  = 10
FSTOPI_MSG_CATAST  = 10

FSTOPI_TOL_NONE    = 0
FSTOPI_TOL_DEBUG   = 2
FSTOPI_TOL_INFO    = 4
FSTOPI_TOL_WARNING = 6
FSTOPI_TOL_ERROR   = 8
FSTOPI_TOL_FATAL   = 10

FSTOPS_MSG_DEBUG   = "DEBUG"
FSTOPS_MSG_INFO    = "INFORM"
FSTOPS_MSG_WARNING = "WARNIN"
FSTOPS_MSG_ERROR   = "ERRORS"
FSTOPS_MSG_FATAL   = "FATALE"
FSTOPS_MSG_SYSTEM  = "SYSTEM"
FSTOPS_MSG_CATAST  = "CATAST"

FSTOPS_TURBO_FAST  = "FAST"
FSTOPS_TURBO_BEST  = "BEST"
#</source>

#==== File mode ====

#<source lang=python>
FST_RW           = "RND+R/W"
FST_RW_OLD       = "RND+R/W+OLD"
FST_RO           = "RND+R/O"
FILE_MODE_RO     = FST_RO
FILE_MODE_RW_OLD = FST_RW_OLD
FILE_MODE_RW     = FST_RW
#</source>

#==== Metadata ====

#<source lang=python>
## Wildcards for search and replace
FST_FIND_ANY_INT = -1
FST_FIND_ANY_STR = ' '

## String lenght
FST_GRTYP_LEN  = 1
FST_TYPVAR_LEN = 2
FST_NOMVAR_LEN = 4
FST_ETIKET_LEN = 12

## Default Metadata to be used as a record metadata "skeleton"
FST_RDE_META_DEFAULT = {
    'dateo' : 0,
    'deet'  : 0,
    'npas'  : 0,
    'ni'    : 1,
    'nj'    : 1,
    'nk'    : 1,
    'nbits' : 16,
    'datyp' : 133,
    'ip1'   : 0,
    'ip2'   : 0,
    'ip3'   : 0,
    'typvar': 'P',
    'nomvar': ' ',
    'etiket': ' ',
    'grtyp' : 'G',
    'ig1'   : 0,
    'ig2'   : 0,
    'ig3'   : 0,
    'ig4'   : 0,
    'swa'   : 0,
    'lng'   : 0,
    'dltf'  : 0,
    'ubc'   : 0,
    'xtra1' : 0,
    'xtra2' : 0,
    'xtra3' : 0
}
#</source>

#==== Data types ====

#<source lang=python>
##     0: binary, transparent
##     1: floating point
##     2: unsigned integer
##     3: character (R4A in an integer)
##     4: signed integer
##     5: IEEE floating point
##     6: floating point (16 bit, made for compressor)
##     7: character string
##     8: complex IEEE
##   130: compressed short integer  (128+2)
##   133: compressed IEEE           (128+5)
##   134: compressed floating point (128+6)
## +128 : second stage packer active
## +64  : missing value convention used

## FSTD valid code for data types
FST_DATYP_LIST = {
    'binary' : 0,
    'float' : 1,
    'uint' : 2,
    'char_r4a' : 3,
    'int' : 4,
    'float_IEEE' : 5,
    'float16' : 6,
    'char' : 7,
    'complex' : 8,
    'float_compressed' : 129,
    'uint_compressed' : 130,
    'char_r4a_compressed' : 131,
    'int_compressed' : 132,
    'float_IEEE_compressed' : 133,
    'float16_compressed' : 134,
    'char_compressed' : 135,
    'complex_compressed' : 136,
    }

## Numpy versus FSTD data type equivalence
FST_DATYP2NUMPY_LIST = { #TODO: review
    0: _np.uint32,   # binary, transparent
    1: _np.float32,  # floating point
    2: _np.uint32,   # unsigned integer
    3: _np.uint32,   # character (R4A in an integer)
    4: _np.int32,    # signed integer
    5: _np.float32,  # IEEE floating point
    6: _np.float32,  # floating point (16 bit, made for compressor)
    7: _np.uint8,    # character string
    8: _np.complex64 # complex IEEE
}

FST_DATYP2NUMPY_LIST64 = { #TODO: review
    0: _np.uint64,  # binary, transparent
    1: _np.float64, # floating point
    2: _np.uint64,  # unsigned integer
    3: _np.uint64,  # character (R4A in an integer)
    4: _np.int64,   # signed integer
    5: _np.float64, # IEEE floating point
    6: _np.float64, # floating point (16 bit, made for compressor)
    #7: _np.uint8,  # character string
    8: _np.complex128  # complex IEEE
}
#</source>

#=== Convip / Convert IP ===

#<source lang=python>
## KIND = 0, hauteur (m) par rapport au niveau de la mer (-20, 000 -> 100, 000)
## KIND = 1, sigma   (0.0 -> 1.0)
## KIND = 2, p est en pression (mb)  (0 -> 1100)
## KIND = 3, code arbitraire  (-4.8e8 -> 1.0e10)
## KIND = 4, hauteur (M) par rapport au niveau du sol    (-20, 000 -> 100, 000)
## KIND = 5, coordonnee hybride        (0.0 -> 1.0)
## KIND = 6, coordonnee theta (1 -> 200, 000)
## KIND =10, temps en heure    (0.0 -> 200, 000.0)
## KIND =15, reserve (entiers)
## KIND =17, indice x de la matrice de conversion (1.0 -> 1.0e10)
##           (partage avec kind=1 a cause du range exclusif
## KIND =21, p est en metres-pression
##           (partage avec kind=5 a cause du range exclusif)
##           (0 -> 1, 000, 000) fact=1e4

KIND_ABOVE_SEA = 0
KIND_SIGMA     = 1
KIND_PRESSURE  = 2
KIND_ARBITRARY = 3
KIND_ABOVE_GND = 4
KIND_HYBRID    = 5
KIND_THETA     = 6
KIND_HOURS     = 10
KIND_SAMPLES   = 15
KIND_MTX_IND   = 17
KIND_M_PRES    = 21

LEVEL_KIND_MSL = KIND_ABOVE_SEA
LEVEL_KIND_SIG = KIND_SIGMA
LEVEL_KIND_PMB = KIND_PRESSURE
LEVEL_KIND_ANY = KIND_ARBITRARY
LEVEL_KIND_MGL = KIND_ABOVE_GND
LEVEL_KIND_HYB = KIND_HYBRID
LEVEL_KIND_TH  = KIND_THETA
LEVEL_KIND_MPR = KIND_M_PRES
TIME_KIND_HR   = KIND_HOURS

CONVIP_IP2P_31BITS = 0

CONVIP_IP2P        = -1 #CONVIP_IP2P_DEFAULT  = -1
CONVIP_DECODE      = CONVIP_IP2P

CONVIP_P2IP        = 1 #CONVIP_STYLE_DEFAULT = 1
CONVIP_P2IP_NEW    = 2 #CONVIP_STYLE_NEW = 2
CONVIP_P2IP_OLD    = 3 #CONVIP_STYLE_OLD  = 3
CONVIP_ENCODE      = CONVIP_P2IP_NEW
CONVIP_ENCODE_OLD  = CONVIP_P2IP_OLD
#</source>

#=== Interp (ezscint) ===

#<source lang=python>
EZ_YES = 'YES'
EZ_NO = 'NO'

EZ_OPT_INTERP_DEGREE = 'INTERP_DEGREE'
EZ_INTERP_NEAREST = 'NEAREST'
EZ_INTERP_LINEAR = 'LINEAR'
EZ_INTERP_CUBIC = 'CUBIC'

EZ_OPT_EXTRAP_DEGREE = 'EXTRAP_DEGREE'
EZ_EXTRAP_NONE = 'DO_NOTHING'
EZ_EXTRAP_MAX = 'MAXIMUM'
EZ_EXTRAP_MIN = 'MINIMUM'
EZ_EXTRAP_VALUE = 'VALUE'
EZ_EXTRAP_ABORT = 'ABORT'

EZ_OPT_EXTRAP_VALUE = 'EXTRAP_VALUE'

EZ_OPT_POLAR_CORRECTION = 'POLAR_CORRECTION'
## YES or NO

EZ_OPT_VERBOSE = 'VERBOSE'
## YES or NO

EZ_OPT_MISSING_INTERP_ALG = 'MISSING_INTERP_ALG'
## TBD

EZ_OPT_MISSING_GRIDPT_DISTANCE = 'MISSING_GRIDPT_DISTANCE'
# float value

EZ_OPT_MISSING_DISTANCE_THRESHOLD = 'MISSING_DISTANCE_THRESHOLD'
# float value

EZ_OPT_MISSING_MISSING_POINTS_TOLERANCE = 'MISSING_MISSING_POINTS_TOLERANCE'
#int value

EZ_OPT_WEIGHT_NUMBER = 'WEIGHT_NUMBER'
#int value

EZ_OPT_CLOUD_INTERP_ALG = 'CLOUD_INTERP_ALG'
EZ_CLOUD_INTERP_DISTANCE = 'DISTANCE'
EZ_CLOUD_INTERP_LINEAR = 'LINEAR'

EZ_OPT_USE_1SUBGRID = 'USE_1SUBGRID'
## YES or NO
#</source>

#=== BURP  ===

#<source lang=python>
MRBCVT_DECODE = 0
MRBCVT_ENCODE = 1
#</source>

#==== File mode ====

#<source lang=python>
BURP_MODE_READ   = 'READ'
BURP_MODE_CREATE = 'CREATE'
BURP_MODE_APPEND = 'APPEND'
#</source>

#==== Report Header Flags ====

#<source lang=python>
BURP_FLAGS_IDX_NAME = {
    0  : 'assembled stations',
    1  : 'surface wind used',
    2  : 'message unreliable (p/t)',
    3  : 'incorrect coordinates',
    4  : 'message corrected',
    5  : 'message amended',
    6  : 'station rejected by AO',
    7  : 'station on black list',
    8  : 'station to evaluate',
    9  : 'superobservation',
    10 : 'data observed',
    11 : 'data derived',
    12 : 'residues',
    13 : 'verifications',
    14 : 'TEMP, part RADAT',
    15 : 'TEMP, part A',
    16 : 'TEMP, part B',
    17 : 'TEMP, part C',
    18 : 'TEMP, part D',
    19 : 'reserved1',
    20 : 'reserved2',
    21 : 'reserved3',
    22 : 'reserved4',
    23 : 'reserved5'
}
## Doc 2005:
## Bit Signification
## ?? 0 1= observations au-dessus de la terre (masque terre/mer)
## 1 1= vent de surface utilisé (stations terrestres)
## ?? 2 1= enregistrement contient des données sur la correction de radiation (stations aérologiques)
## ?? 3 1= enregistrement contient correction de la position des bateaux, provenant du CQ des bateaux.
## ?? * 4 en réserve
## ?? 5 1= station hors du domaine d'intérêt
## 6 1= station avec élément rejeté par le contrôle de qualité de AO (analyse objective)
## 7 1= station avec élément(s) sur liste noire
## 8 1= station à évaluer mais non utilisée par AO
## ?? 9 1= décodeur rapporte position de station douteuse
## 10 1= enregistrement contient des données observées
## 11 1= enregistrement contient des données dérivées d'entrée
## ?? 12 1= enregistrement contient des données vues par l'AO
## ?? 13 1= enregistrement contient des résidus
## 14 1= partie RADAT de TEMP ou présence de Ts de SATOB
## 15 1= partie A de TEMP, PILOT, SATEM ou SATOB
## 16 1= partie B de TEMP, PILOT, SATEM
## 17 1= partie C de TEMP, PILOT ou SATEM
## 18 1= partie D de TEMP, PILOT ou SATEM
## ?? 19 1= enregistrement contient des données analysées5
## ?? 20 1= enregistrement contient des données prévues
## ?? 21 1= enregistrement contient des données de vérification
BURP_FLAGS_IDX = dict([(v, k) for k, v in BURP_FLAGS_IDX_NAME.items()])

#==== Data types ====

#<source lang=python>
## String lenght
BURP_STNID_STRLEN = 9

## BURP valid code for data types
BURP_DATYP_LIST = {
    'binary'  : 0,  # 0 = string of bits (bit string)  
    'uint'    : 2,  # 2 = unsigned integers  
    'char'    : 3,  # 3 = characters (NBIT must be equal to 8)  
    'int'     : 4,  # 4 = signed integers  
    'upchar'  : 5,  # 5 = uppercase characters (the lowercase characters
                    #     will be converted to uppercase during the read)
                    #     (NBIT must be equal to 8)  
    'float'   : 6,  # 6 = real*4 (ie: 32bits)  
    'double'  : 7,  # 7 = real*8 (ie: 64bits)  
    'complex' : 8,  # 8 = complex*4 (ie: 2 times 32bits)  
    'dcomplex': 9   # 9 = complex*8 (ie: 2 times 64bits)  
}
BURP_DATYP_NAMES = dict([(v, k) for k, v in BURP_DATYP_LIST.items()])

## Numpy versus BURP data type equivalence
BURP_DATYP2NUMPY_LIST = { #TODO: review
    0: _np.uint32,    # binary, transparent
    2: _np.uint32,    # unsigned integer
    3: _np.uint8,     # character string
    4: _np.int32,     # signed integer
    5: _np.uint8,     # character string (uppercase)
    6: _np.float32,   # floating point
    7: _np.float64,   # double precision 
    8: _np.complex64, # complex IEEE
    9: _np.complex128 # double complex IEEE
}
## Note: Type 3 and 5 are processed like strings of bits thus,
##       the user should do the data compression himself.

## Doc 2005:
## 0 chaîne de bits
## 2 entiers sans signe
## 3 caractères, NBIT doit être égal à 8
## 4 entiers avec signe
## 5 tous les caractères en majuscules, NBIT doit être égal à 8.
## 6 nombres complexes, partie réelle, simple précision (R4)
## 7 nombres complexes, partie réelle, double précision (R8)
## 8 nombres complexes, partie imaginaire, simple précision (I4)
## 9 nombres complexes, partie imaginaire, simple précision (I8)
#</source>

#==== mrfopt (options) ====

#<source lang=python>
BURPOP_MISSING = 'MISSING'
BURPOP_MSGLVL  = 'MSGLVL'

BURPOP_MSG_TRIVIAL = 'TRIVIAL'
BURPOP_MSG_INFO    = 'INFORMATIF'
BURPOP_MSG_WARNING = 'WARNING'
BURPOP_MSG_ERROR   = 'ERROR'
BURPOP_MSG_FATAL   = 'FATAL'
BURPOP_MSG_SYSTEM  = 'SYSTEM'
#</source>
