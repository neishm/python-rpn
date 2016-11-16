#!/usr/bin/env python
# . s.ssmuse.dot /ssm/net/hpcs/201402/02/base /ssm/net/hpcs/201402/02/intel13sp1u2 /ssm/net/rpn/libs/15.2
"""
Unit tests for librmn.base

See: https://wiki.cmc.ec.gc.ca/wiki/Exemples_d%27utilisation_des_programmes_BURP
"""

import os
import sys
import rpnpy.librmn.all as rmn
import unittest
import ctypes as _ct
import numpy as _np

if sys.version_info > (3, ):
    long = int

#--- primitives -----------------------------------------------------

class RpnPyLibrmnBurp(unittest.TestCase):

    burptestfile = 'bcmk_burp/2007021900.brp'
    #(path, itype, iunit)
    knownValues = (
        (burptestfile, rmn.WKOFFIT_TYPE_LIST['BURP'], 999), 
        )

    def getFN(self, name):
        ATM_MODEL_DFILES = os.getenv('ATM_MODEL_DFILES')
        return os.path.join(ATM_MODEL_DFILES.strip(), name)
        

    def testWkoffitKnownValues(self):
        """wkoffit should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            funit = rmn.wkoffit(self.getFN(mypath))
            self.assertEqual(funit, itype, mypath+':'+repr(funit)+' != '+repr(itype))

    def testfnomfclosKnownValues(self):
        """fnom fclos should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            funit = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            rmn.fclos(funit)
            self.assertEqual(funit, iunit, mypath+':'+repr(funit)+' != '+repr(iunit))

    def testmrfnbrKnownValues(self):
        """mrfnbr mrfmxl mrfbfl should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            funit   = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            nbrp    = rmn.mrfnbr(funit)
            maxlen  = rmn.mrfmxl(funit)
            maxlen2 = rmn.mrfbfl(funit)
            ## https://wiki.cmc.ec.gc.ca/wiki/Probl%C3%A8me_avec_les_fonctions_de_manipulation_de_fichiers_BURP_dans_RMNLIB
            maxlen = max(64, maxlen)+10
            rmn.fclos(funit)
            self.assertEqual(nbrp, 47544)
            self.assertEqual(maxlen,  6208+10)
            self.assertEqual(maxlen2, 6208+10)

    def testmrfopnclsKnownValues(self):
        """mrfopn mrfcls should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            rmn.mrfopt(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
            funit  = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            nbrp   = rmn.mrfopn(funit, rmn.FST_RO)
            rmn.mrfcls(funit)
            rmn.fclos(funit)
            self.assertEqual(nbrp, 47544)

    def testmrflocKnownValues(self):
        """mrfloc should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            rmn.mrfopt(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
            funit = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            nbrp  = rmn.mrfopn(funit, rmn.FST_RO)
            handle = 0
            handle = rmn.mrfloc(funit, handle)
            self.assertNotEqual(handle, 0)
            (stnid, idtyp, lat, lon, date, temps, sup) = \
                ('*********', -1, -1, -1, -1, -1, None)
            handle = 0
            nbrp2 = 0
            for irep in xrange(nbrp):
                handle = rmn.mrfloc(funit, handle, stnid, idtyp, lat, lon, date, temps, sup)
                ## sys.stderr.write(repr(handle)+'\n')
                self.assertNotEqual(handle, 0)
                nbrp2 += 1
            handle = 0
            sup = []
            for irep in xrange(nbrp):
                handle = rmn.mrfloc(funit, handle, stnid, idtyp, lat, lon, date, temps, sup)
                self.assertNotEqual(handle, 0)
            rmn.mrfcls(funit)
            rmn.fclos(funit)
            self.assertEqual(nbrp2, nbrp)

    def testmrfgetKnownValues(self):
        """mrfget should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            rmn.mrfopt(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
            funit  = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            nbrp   = rmn.mrfopn(funit, rmn.FST_RO)
            maxlen = max(64, rmn.mrfmxl(funit))+10

            buf = None
            handle = 0
            handle = rmn.mrfloc(funit, handle)
            buf = rmn.mrfget(handle, buf, funit)
            self.assertEqual(buf.size, 12416)
            #TODO: self.assertEqual(buf, ???)
            ## sys.stderr.write(repr(handle)+"("+repr(maxlen)+') rmn.mrfget None size='+repr(buf.size)+'\n')

            buf = maxlen
            handle = 0
            handle = rmn.mrfloc(funit, handle)
            buf = rmn.mrfget(handle, buf, funit)
            self.assertEqual(buf.size, 12436)
            #TODO: self.assertEqual(buf, ???)
            ## sys.stderr.write(repr(handle)+"("+repr(maxlen)+') rmn.mrfget maxlen size='+repr(buf.size)+'\n')

            buf = _np.empty((maxlen, ), dtype=_np.int32)
            buf[0] = maxlen
            handle = 0
            handle = rmn.mrfloc(funit, handle)
            buf = rmn.mrfget(handle, buf, funit)
            self.assertEqual(buf.size, 6218)
            #TODO: self.assertEqual(buf, ???)
            ## sys.stderr.write(repr(handle)+"("+repr(maxlen)+') rmn.mrfget empty size='+repr(buf.size)+'\n')

            handle = 0
            for irep in xrange(nbrp):
                handle = rmn.mrfloc(funit, handle)
                buf = rmn.mrfget(handle, buf, funit)
                ## print handle, buf.shape, buf[0:10]
                self.assertEqual(buf.size, 6218)
            
            rmn.mrfcls(funit)
            rmn.fclos(funit)

    def testmrbhdrKnownValues(self):
        """mrbhdr should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            rmn.mrfopt(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
            funit  = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            nbrp   = rmn.mrfopn(funit, rmn.FST_RO)
            maxlen = max(64, rmn.mrfmxl(funit))+10

            buf = None
            handle = 0
            handle = rmn.mrfloc(funit, handle)
            buf    = rmn.mrfget(handle, buf, funit)
            params = rmn.mrbhdr(buf)
            params0 = {'flgs': 72706, 'xaux': None, 'nxaux': 0, 'elev': 457,
                       'nblk': 12, 'dy': 0, 'lati ': 15420, 'long': 27663,
                       'nsup': 0, 'temps': 0, 'idtyp': 138, 'oars': 518,
                       'dx': 0, 'stnid': '71915    ', 'date': 20070219,
                       'drnd': 0, 'sup': None, 'runn': 8}
            for k in params.keys():
                self.assertEqual(params0[k], params[k],
                                 'For {0}, expected {1}, got {2}'
                                 .format(k, params0[k], params[k]))
            rmn.mrfcls(funit)
            rmn.fclos(funit)

    def testmrbprmKnownValues(self):
        """mrbprm should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            rmn.mrfopt(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
            funit  = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            nbrp   = rmn.mrfopn(funit, rmn.FST_RO)
            maxlen = max(64, rmn.mrfmxl(funit))+10

            buf = None
            handle = 0
            handle = rmn.mrfloc(funit, handle)
            buf    = rmn.mrfget(handle, buf, funit)
            params = rmn.mrbhdr(buf)
            for iblk in xrange(params['nblk']):
                blkparams = rmn.mrbprm(buf, iblk+1)
            blkparams0 = {'nele': 10, 'nbit': 20, 'datyp': 2, 'nval': 17,
                          'bdesc': 0, 'btyp': 9326, 'bfam': 10, 'nt': 1,
                          'bit0': 288}
            for k in blkparams.keys():
                self.assertEqual(blkparams0[k], blkparams[k],
                                 'For {0}, expected {1}, got {2}'
                                 .format(k, blkparams0[k], blkparams[k]))
            rmn.mrfcls(funit)
            rmn.fclos(funit)

    def testmrbxtrKnownValues(self):
        """mrbprm should give known result with known input"""
        for mypath, itype, iunit in self.knownValues:
            rmn.mrfopt(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
            funit  = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
            nbrp   = rmn.mrfopn(funit, rmn.FST_RO)
            maxlen = max(64, rmn.mrfmxl(funit))+10

            buf = None
            handle = 0
            handle = rmn.mrfloc(funit, handle)
            buf    = rmn.mrfget(handle, buf, funit)
            params = rmn.mrbhdr(buf)
            ## blkdata = {
            ##     'lstele' : None,
            ##     'tblval' : None
            ##     }
            for iblk in xrange(params['nblk']):
                blkparams = rmn.mrbprm(buf, iblk+1)
                ## blkdata   = rmn.mrbxtr(buf, iblk+1, blkdata['lstele'], blkdata['tblval'])
                blkdata   = rmn.mrbxtr(buf, iblk+1)
                for k in blkparams.keys():
                    self.assertEqual(blkparams[k], blkdata[k],
                                     'For {0}, expected {1}, got {2}'
                                     .format(k, blkparams[k], blkdata[k]))
            lstele0 = _np.array([1796, 2817, 2818, 3073, 3264, 2754, 2049, 2819, 2820, 3538], dtype=_np.int32)
            tblval0 = _np.array([10000, -1, -1, -1, -1, 405, -1, -1, -1, 1029000], dtype=_np.int32)
            self.assertFalse(_np.any(lstele0 - blkdata['lstele'] != 0))
            self.assertEqual((blkparams['nele'], blkparams['nval'], blkparams['nt']), blkdata['tblval'].shape)
            self.assertFalse(_np.any(tblval0 - blkdata['tblval'][0:blkdata['nele'],0,0] != 0))
            
            rmn.mrfcls(funit)
            rmn.fclos(funit)


    ## def testmrbxtrdclKnownValues(self):
    ##     """fnomfclos should give known result with known input"""
    ##     for mypath, itype, iunit in self.knownValues:
    ##         ier    = rmn.c_mrfopc(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
    ##         funit  = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
    ##         nbrp   = rmn.c_mrfopn(funit, rmn.FST_RO)
    ##         maxlen = max(64, rmn.c_mrfmxl(funit))+10

    ##         (stnid, idtyp, lat, lon, date, temps, nsup, nxaux) = \
    ##             ('*********', -1, -1, -1, -1, -1, 0, 0)
    ##         sup  = _np.empty((1, ), dtype=_np.int32)
    ##         xaux = _np.empty((1, ), dtype=_np.int32)
    ##         buf  = _np.empty((maxlen, ), dtype=_np.int32)
    ##         buf[0] = maxlen
    ##         handle = 0
            
    ##         itime = _ct.c_int(0)
    ##         iflgs = _ct.c_int(0)
    ##         stnids = ''
    ##         idburp = _ct.c_int(0)
    ##         ilat  = _ct.c_int(0)
    ##         ilon  = _ct.c_int(0)
    ##         idx   = _ct.c_int(0)
    ##         idy   = _ct.c_int(0)
    ##         ialt  = _ct.c_int(0)
    ##         idelay = _ct.c_int(0)
    ##         idate = _ct.c_int(0)
    ##         irs   = _ct.c_int(0)
    ##         irunn = _ct.c_int(0)
    ##         nblk  = _ct.c_int(0)

    ##         nele  = _ct.c_int(0)
    ##         nval  = _ct.c_int(0)
    ##         nt    = _ct.c_int(0)
    ##         bfam  = _ct.c_int(0)
    ##         bdesc = _ct.c_int(0)
    ##         btyp  = _ct.c_int(0)
    ##         nbit  = _ct.c_int(0)
    ##         bit0  = _ct.c_int(0)
    ##         datyp = _ct.c_int(0)

    ##         for irep in xrange(nbrp):
    ##             handle = rmn.c_mrfloc(funit, handle, stnid, idtyp, lat, lon, date, temps, sup, nsup)
    ##             ier = rmn.c_mrfget(handle, buf)
    ##             ier = rmn.c_mrbhdr(buf, 
    ##                     itime, iflgs, stnids, idburp, 
    ##                     ilat, ilon, idx, idy, ialt, 
    ##                     idelay, idate, irs, irunn, nblk, 
    ##                     sup, nsup, xaux, nxaux)
    ##             ## print irep, handle, itime, iflgs, stnids, idburp, ilat, ilon, idx, idy, ialt, idelay, idate, irs, irunn, nblk

    ##             for iblk in xrange(nblk.value):
    ##                 ier = rmn.c_mrbprm(buf, iblk, 
    ##                              nele, nval, nt, bfam, bdesc, btyp, nbit, bit0, datyp)
    ##                 lstele = _np.empty((nele.value, ), dtype=_np.int32)
    ##                 ## tblval = _np.empty((nele.value, nval.value, nt.value), dtype=_np.int32)
    ##                 nmax = nele.value*nval.value*nt.value#*2
    ##                 tblval = _np.empty((nmax, ), dtype=_np.int32)
    ##                 ier = rmn.c_mrbxtr(buf, iblk, lstele, tblval)
    ##                 #print irep, iblk, ier, nele.value, nval.value, nt.value, lstele, tblval
    ##                 codes = _np.empty((nele.value, ), dtype=_np.int32)
    ##                 ier = rmn.c_mrbdcl(lstele, codes, nele)
    ##                 #print irep, iblk, ier, codes
    ##                 #self.assertEqual(ier, 0)
                
    ##         ier    = rmn.c_mrfcls(funit)
    ##         ier    = rmn.fclos(funit)


    ## def testmrbxtrcvtKnownValues(self):
    ##     """fnomfclos should give known result with known input"""
    ##     for mypath, itype, iunit in self.knownValues:
    ##         ier    = rmn.c_mrfopc(rmn.FSTOP_MSGLVL, rmn.FSTOPS_MSG_FATAL)
    ##         funit  = rmn.fnom(self.getFN(mypath), rmn.FST_RO)
    ##         nbrp   = rmn.c_mrfopn(funit, rmn.FST_RO)
    ##         maxlen = max(64, rmn.c_mrfmxl(funit))+10

    ##         (stnid, idtyp, lat, lon, date, temps, nsup, nxaux) = \
    ##             ('*********', -1, -1, -1, -1, -1, 0, 0)
    ##         sup  = _np.empty((1, ), dtype=_np.int32)
    ##         xaux = _np.empty((1, ), dtype=_np.int32)
    ##         buf  = _np.empty((maxlen, ), dtype=_np.int32)
    ##         buf[0] = maxlen
    ##         handle = 0
            
    ##         itime = _ct.c_int(0)
    ##         iflgs = _ct.c_int(0)
    ##         stnids = ''
    ##         idburp = _ct.c_int(0)
    ##         ilat  = _ct.c_int(0)
    ##         ilon  = _ct.c_int(0)
    ##         idx   = _ct.c_int(0)
    ##         idy   = _ct.c_int(0)
    ##         ialt  = _ct.c_int(0)
    ##         idelay = _ct.c_int(0)
    ##         idate = _ct.c_int(0)
    ##         irs   = _ct.c_int(0)
    ##         irunn = _ct.c_int(0)
    ##         nblk  = _ct.c_int(0)

    ##         nele  = _ct.c_int(0)
    ##         nval  = _ct.c_int(0)
    ##         nt    = _ct.c_int(0)
    ##         bfam  = _ct.c_int(0)
    ##         bdesc = _ct.c_int(0)
    ##         btyp  = _ct.c_int(0)
    ##         nbit  = _ct.c_int(0)
    ##         bit0  = _ct.c_int(0)
    ##         datyp = _ct.c_int(0)

    ##         MRBCVT_DECODE = 0
    ##         MRBCVT_ENCODE = 1

    ##         for irep in xrange(nbrp):
    ##             handle = rmn.c_mrfloc(funit, handle, stnid, idtyp, lat, lon, date, temps, sup, nsup)
    ##             ier = rmn.c_mrfget(handle, buf)
    ##             ier = rmn.c_mrbhdr(buf, 
    ##                     itime, iflgs, stnids, idburp, 
    ##                     ilat, ilon, idx, idy, ialt, 
    ##                     idelay, idate, irs, irunn, nblk, 
    ##                     sup, nsup, xaux, nxaux)
    ##             ## print irep, handle, itime, iflgs, stnids, idburp, ilat, ilon, idx, idy, ialt, idelay, idate, irs, irunn, nblk

    ##             for iblk in xrange(nblk.value):
    ##                 ier = rmn.c_mrbprm(buf, iblk, 
    ##                              nele, nval, nt, bfam, bdesc, btyp, nbit, bit0, datyp)
    ##                 lstele = _np.empty((nele.value, ), dtype=_np.int32)
    ##                 tblval = _np.empty((nele.value, nval.value, nt.value), dtype=_np.int32)
    ##                 pval   = _np.empty((nele.value, nval.value, nt.value), dtype=_np.float32)
    ##                 ## nmax = nele.value*nval.value*nt.value#*2
    ##                 ## tblval = _np.empty((nmax, ), dtype=_np.int32)
    ##                 ier = rmn.c_mrbxtr(buf, iblk, lstele, tblval)
    ##                 codes = _np.empty((nele.value, ), dtype=_np.int32)
    ##                 ier = rmn.c_mrbdcl(lstele, codes, nele)
    ##                 ## print irep, iblk, ier, codes
    ##                 #self.assertEqual(ier, 0)

    ##                 if datyp.value in (2, 4):
    ##                     pval[:, :, :] = tblval[:, :, :]
    ##                     ier = rmn.c_mrbcvt(lstele, tblval, pval, nele, nval, nt, MRBCVT_DECODE)
    ##                 elif datyp.value == 6:
    ##                     pval[:, :, :] = tblval[:, :, :] #??transfer???
    ##                     ## pval(j)=transfer(tblval(j), z4val)
    ##                 else:
    ##                     pass #raise
    ##                 #print irep, iblk, ier, datyp.value, pval
    ##         ier    = rmn.c_mrfcls(funit)
    ##         ier    = rmn.fclos(funit)

if __name__ == "__main__":
    unittest.main()

# -*- Mode: C; tab-width: 4; indent-tabs-mode: nil -*-
# vim: set expandtab ts=4 sw=4:
# kate: space-indent on; indent-mode cstyle; indent-width 4; mixedindent off;
