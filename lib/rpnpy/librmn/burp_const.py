#!/usr/bin/env python
# -*- coding: utf-8 -*-
# . s.ssmuse.dot /ssm/net/hpcs/201402/02/base \
#                /ssm/net/hpcs/201402/02/intel13sp1u2 /ssm/net/rpn/libs/15.2
# Author: Stephane Chamberland <stephane.chamberland@canada.ca>
# Copyright: LGPL 2.1

"""
Module librmn_burp_const defines a set of helper constants to make code
using the librmn burp module more readable.
"""
import numpy as _np

#=== BURP Constants ===

## See:
## * ls -lL $AFSISIO/datafiles/constants/ | grep -i burp
## ** $AFSISIO/datafiles/constants/tableburp_[ef].val 
##    table_b_bufr_[ef]_opsvalid_v23
## ** $AFSISIO/datafiles/constants/tableburp [fr]
##    $AFSISIO/datafiles/constants/table_b_bufr_e [en]
## * ls -lL $AFSISIO/datafiles/constants/ | grep -i bufr
##
## * 3 types of files:
## ** table_b_bufr_master, table_b_bufr_[ef], table_b_bufr_[ef]_opsvalid_v23
## ** table_d_bufr_[ef]
## ** tabloc_bufr_[ef]
##
## Also:
## * ade*bufr*
## * libecbufr_tables/*

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
BURP_FLAGS_IDX_NAME = { #TODO: review
    0  : 'assembled stations',
    ## 0  : '',#observations au-dessus de la terre (masque terre/mer)
    1  : 'surface wind used',
    2  : 'message unreliable (p/t)',
    ## 2  : '', #data sur la correction de radiation (stations aerologiques)
    3  : 'incorrect coordinates',
    ## 3  : '', #correction de la position des bateaux, provenant du CQ des bateaux.
    4  : 'message corrected',
    ## 4  : '',#en reserve
    5  : 'message amended',
    ## 5  : '',# station hors du domaine d'interet
    6  : 'station rejected by AO',
    7  : 'station on black list',
    8  : 'station to evaluate',
    9  : 'superobservation',
    ## 9  : '',#decodeur rapporte position de station douteuse ?incorrect coordinates?
    10 : 'data observed',
    11 : 'data derived',
    12 : 'residues',
    ## 12 : '', #data vues by AO
    13 : 'verifications',
    ## 13 : '', #'residues'
    14 : 'TEMP part RADAT',
    15 : 'TEMP part A',
    16 : 'TEMP part B',
    17 : 'TEMP part C',
    18 : 'TEMP part D',
    19 : 'reserved1', #'data analysed'
    20 : 'reserved2', #'data forecast'
    21 : 'reserved3', #'verifications'
    22 : 'reserved4',
    23 : 'reserved5'
}
BURP_FLAGS_IDX = dict([(v, k) for k, v in BURP_FLAGS_IDX_NAME.items()])


BURP_IDTYP_DESC = { 
    '12' : 'SYNOP, NON AUTOMATIQUE',
    '13' : 'SHIP, NON AUTOMATIQUE',
    '14' : 'SYNOP MOBIL',
    '15' : 'METAR',
    '16' : 'SPECI',
    '18' : 'DRIFTER',
    '20' : 'RADOB',
    '22' : 'RADREP',
    '32' : 'PILOT',
    '33' : 'PILOT SHIP',
    '34' : 'PILOT MOBIL',
    '35' : 'TEMP',
    '36' : 'TEMP SHIP',
    '37' : 'TEMP DROP',
    '38' : 'TEMP MOBIL',
    '39' : 'ROCOB',
    '40' : 'ROCOB SHIP',
    '41' : 'CODAR',
    '42' : 'AMDAR (AIRCRAFT METEOROLOGICAL DATA REPORT)',
    '44' : 'ICEAN',
    '45' : 'IAC',
    '46' : 'IAC FLEET',
    '47' : 'GRID',
    '49' : 'GRAF',
    '50' : 'WINTEM',
    '51' : 'TAF',
    '53' : 'ARFOR',
    '54' : 'ROFOR',
    '57' : 'RADOF',
    '61' : 'MAFOR',
    '62' : 'TRACKOB',
    '63' : 'BATHY7',
    '64' : 'TESAC',
    '65' : 'WAVEOB',
    '67' : 'HYDRA',
    '68' : 'HYFOR',
    '71' : 'CLIMAT',
    '72' : 'CLIMAT SHIP',
    '73' : 'NACLI/CLINP/SPCLI/CLISA/INCLI',
    '75' : 'CLIMAT TEMP',
    '76' : 'CLIMAT TEMP SHIP',
    '81' : 'SFAZI',
    '82' : 'SFLOC',
    '83' : 'SFAZU',
    '85' : 'SAREP',
    '86' : 'SATEM',
    '87' : 'SARAD',
    '88' : 'SATOB',
    '92' : 'GRIB',
    '94' : 'BUFR',
    '127' : "DONNEES DE SURFACE DE QUALITE DE L’AIR",
    '128' : 'AIREP',
    '129' : 'PIREP',
    '130' : 'PROFILEUR DE VENT',
    '131' : 'SUPEROBS DE SYNOP',
    '132' : 'SUPEROBS DE AIREP',
    '133' : 'SA + SYNOP',
    '134' : "PAOBS (PSEUDO-DONNEES D'AUSTRALIE)",
    '135' : 'TEMP + PILOT',
    '136' : 'TEMP + SYNOP',
    '137' : 'PILOT + SYNOP',
    '138' : 'TEMP + PILOT + SYNOP',
    '139' : 'TEMP SHIP + PILOT SHIP',
    '140' : 'TEMP SHIP + SHIP',
    '141' : 'PILOT SHIP + SHIP',
    '142' : 'TEMPS SHIP + PILOT SHIP + SHIP',
    '143' : 'SAWR, STATION NON AUTOMATIQUE (REGULIER OU REGULIER SPECIAL)',
    '144' : 'SAWR, STATION AUTOMATIQUE (REGULIER OU REGULIER SPECIAL)',
    '145' : 'SYNOP ("PATROL SHIPS")',
    '146' : 'ASYNOP, STATION AUTOMATIQUE',
    '147' : 'ASHIP, STATION AUTOMATIQUE, (BOUEES FIXES, PLATES-FORMES.)',
    '148' : 'SAWR, STATION NON AUTOMATIQUE (SPECIAL)',
    '149' : 'SAWR, STATION AUTOMATIQUE (SPECIAL)',
    '150' : 'PSEUDO-DONNEES DU CMC, SURFACE, MODE ANALYSE',
    '151' : 'PSEUDO-DONNEES DU CMC, ALTITUDE, MODE ANALYSE',
    '152' : 'PSEUDO-DONNEES DU CMC, SURFACE, MODE REPARATION',
    '153' : 'PSEUDO-DONNEES DU CMC, ALTITUDE, MODE REPARATION',
    '154' : 'PREVISIONS DE VENTS DE TYPE FD',
    '155' : 'PREVISIONS DE VENTS DE TYPE FD AMENDEES',
    '156' : 'PREVISIONS STATISTIQUES DES ELEMENTS DU TEMPS',
    '157' : 'ACARS (AIRCRAFT METEOROLOGICAL DATA REPORT)',
    '158' : 'HUMSAT',
    '159' : 'TEMP MOBIL + PILOT MOBIL',
    '160' : 'TEMP MOBIL + SYNOP MOBIL',
    '161' : 'PILOT MOBIL + SYNOP MOBIL',
    '162' : 'TEMP MOBIL + PILOT MOBIL + SYNOP MOBIL',
    '163' : 'RADAR',
    '164' : 'RADIANCES TOVS AMSUA',
    '165' : 'PROFILS VERTICAUX ANALYSES OU PREVUS',
    '166' : 'MOS EVOLUTIF (PROJET PENSE)',
    '167' : 'DONNEES SATELLITAIRES PROVENANTDE SCATTEROMÈTRES (ERS, ADEOS, ETC.)',
    '168' : 'DONNEES SATELLITAIRES DE TYPE SSMI',
    '169' : 'RADIO-OCCULTATIONS',
    '170' : 'OZONE',
    '171' : 'METEOSAT',
    '172' : 'STANDARD HYDROMETEOROLOGICAL EXCHANGE FORMAT (S.H.E.F.)',
    '173' : 'VERIFICATIONS DES MODÈLES DU CMC',
    '174' : 'DONNEES SATELLITAIRES PROVENANTDE RADARS À OUVERTURE SYNTHETIQUE (ERS, ETC.)',
    '175' : 'DONNEES SATELLITAIRES PROVENANT D’ALTIMÈTRES RADAR (ERS, ETC.)',
    '176' : 'STATIONS D’UN RESEAU COOPERATIF (INTERDIT DE REDISTRIBUER LES DONNEES)',
    '177' : 'ADS AUTOMATED DEPENDANCE SURVEILLANCE (AIREP AUTOMATIQUE)',
    '178' : 'DONNEES PROVENANTDE ICEC POUR LES LACS',
    '179' : 'DONNEES PROVENANTDE ICEC POUR LES OCEANS',
    '180' : 'RADIANCES GOES',
    '181' : 'RADIANCES ATOVS AMSUB',
    '182' : 'RADIANCES MHS',
    '183' : 'DONNEES AIRS',
    '184' : 'RADIANCES (GENERIQUE)',
    '188' : 'DONNEES SATELLITAIRES DE VENT AMELIOREES (FORMAT BUFR)',
    '189' : 'DONNEES DE SURFACE GPS'
}

BURP_IDTYP_IDX = dict([(v, int(k)) for k, v in BURP_IDTYP_DESC.items()])

#==== Data types ====

#<source lang=python>
## String lenght
BURP_STNID_STRLEN = 9
BURP_OPTC_STRLEN = 9

## BURP valid code for data types
BURP_DATYP_LIST = { #TODO: review
    'binary'  : 0,  # 0 = string of bits (bit string)  
    'uint'    : 2,  # 2 = unsigned integers  
    'char'    : 3,  # 3 = characters (NBIT must be equal to 8)  
    'int'     : 4,  # 4 = signed integers  
    'upchar'  : 5,  # 5 = uppercase characters (the lowercase characters
                    #     will be converted to uppercase during the read)
                    #     (NBIT must be equal to 8)  
    'float'   : 6,  # 6 = real*4 (ie: 32bits)  #TODO: review
                    # ?? nombres complexes, partie réelle, simple précision (R4)
    'double'  : 7,  # 7 = real*8 (ie: 64bits)  #TODO: review
                    # ?? nombres complexes, partie réelle, double précision (R8)
    'complex' : 8,  # 8 = complex*4 (ie: 2 times 32bits)  #TODO: review
                    # ?? nombres complexes, partie imaginaire, simple précision (I4)
    'dcomplex': 9   # 9 = complex*8 (ie: 2 times 64bits)  #TODO: review
                    # ?? nombres complexes, partie imaginaire, simple précision (I8)
}
BURP_DATYP_NAMES = dict([(v, k) for k, v in BURP_DATYP_LIST.items()])

## Numpy versus BURP data type equivalence
BURP_DATYP2NUMPY_LIST = { #TODO: review
    0: _np.uint32,    # binary, transparent
    2: _np.uint32,    # unsigned integer
    3: _np.uint8,     # character string
    4: _np.int32,     # signed integer
    5: _np.uint8,     # character string (uppercase)
    6: _np.float32,   # floating point      #TODO: review
    7: _np.float64,   # double precision    #TODO: review
    8: _np.complex64, # complex IEEE        #TODO: review
    9: _np.complex128 # double complex IEEE #TODO: review
}
## Note: Type 3 and 5 are processed like strings of bits thus,
##       the user should do the data compression himself.
#</source>

#==== mrfopt (options) ====

#<source lang=python>
BURPOP_MISSING = 'MISSING'
BURPOP_MSGLVL  = 'MSGLVL'

BURPOP_MSG_TRIVIAL = 'TRIVIAL  '
BURPOP_MSG_INFO    = 'INFORMATIF'
BURPOP_MSG_WARNING = 'WARNING  '
BURPOP_MSG_ERROR   = 'ERROR    '
BURPOP_MSG_FATAL   = 'ERRFATAL '
BURPOP_MSG_SYSTEM  = 'SYSTEM   '
#</source>