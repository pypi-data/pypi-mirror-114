"""
Module that contains common values found in the MCS Joint Release 5 header file
src/exec/me.h and other functions useful for working with the MCS metadata.  
The header file values are:
 * ME_SSMIF_FORMAT_VERSION - SSMIF format version code
 * ME_MAX_NSTD - Maximum number of stands that can be described
 * ME_MAX_NFEE - Maximum number of FEEs that can be described
 * ME_MAX_FEEID_LENGTH - Number of characters in FEE ID name
 * ME_MAX_RACK - Maximum number of racks?
 * ME_MAX_PORT - Maximum number of ports?
 * ME_MAX_NRPD - Maxmimum number of RPD cables
 * ME_MAX_RPDID_LENGTH - Number of characters in the RPD ID name
 * ME_MAX_NSEP - Maximum number of SEP cable connections
 * ME_MAX_SEPID_LENGTH - Number of characters in the SEP ID name
 * ME_MAX_SEPCABL_LENGTH - Number of characters in the SEP cable ID name
 * ME_MAX_NARB - Maximum number of ARX boards
 * ME_MAX_NARBCH - Number of ARX channels per board
 * ME_MAX_ARBID_LENGTH - Number of characters in the ARX ID name
 * ME_MAX_NROACH - Maximum number of ROACH boards
 * ME_MAX_NROACHCH - Number of channels per ROACH board
 * ME_MAX_ROACHID_LENGTH - Number of characters in the ROACH board ID name
 * ME_MAX_NSERVER - Maximum number of servers
 * ME_MAX_SERVERID_LENGTH - Number of characters in the server ID name
 * ME_MAX_NDR - Maximum number of data recorders
 * ME_MAX_DRID_LENGTH - Number of characters in the DR ID name
 * ME_MAX_NPWRPORT - Maximum number of power ports
 * ME_MAX_SSNAME_LENGTH - Number of characters in the power port ID names, for 
                          codes used for PWR_NAME
 * LWA_MAX_NSTD - Maximum number of stands for the LWA
 * MIB_REC_TYPE_BRANCH - eType for MIB branch entries
 * MIB_REC_TYPE_VALUE - etype for MIB value entries
 * MIB_INDEX_FIELD_LENGTH - Number of characters in a MIB index field
 * MIB_LABEL_FIELD_LENGTH - Number of characters in a MIB label field
 * MIB_VAL_FIELD_LENGTH - Number of characters in a MIB value field
 * SSMIF_STRUCT - String representing the C structure of the binary SSMIF

The other functions:
 * Parse the binary packed metadata, 
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import

import re
import ctypes
from datetime import datetime

from lsl.common import adp as adpCommon
from lsl.common.mcs import mjdmpm_to_datetime, datetime_to_mjdmpm, status_to_string, \
                           summary_to_string, sid_to_string, cid_to_string, mode_to_string, \
                           flat_to_multi, apply_pointing_correction, MIB_REC_TYPE_BRANCH, \
                           MIB_REC_TYPE_VALUE, MIB_INDEX_FIELD_LENGTH, MIB_LABEL_FIELD_LENGTH, \
                           MIB_VAL_FIELD_LENGTH, MIB, MIBEntry


from lsl.misc import telemetry
telemetry.track_module()


__version__ = '0.4'
__all__ = ['ME_SSMIF_FORMAT_VERSION', 'ME_MAX_NSTD', 'ME_MAX_NFEE', 'ME_MAX_FEEID_LENGTH', 'ME_MAX_RACK', 'ME_MAX_PORT', 
           'ME_MAX_NRPD', 'ME_MAX_RPDID_LENGTH', 'ME_MAX_NSEP', 'ME_MAX_SEPID_LENGTH', 'ME_MAX_SEPCABL_LENGTH', 
           'ME_MAX_NARB', 'ME_MAX_NARBCH', 'ME_MAX_ARBID_LENGTH', 'ME_MAX_NROACH', 'ME_MAX_NROACHCH', 'ME_MAX_ROACHID_LENGTH', 
           'ME_MAX_NSERVER', 'ME_MAX_SERVERID_LENGTH', 'ME_MAX_NDR', 'ME_MAX_DRID_LENGTH', 'ME_MAX_NPWRPORT', 
           'ME_MAX_SSNAME_LENGTH', 'LWA_MAX_NSTD', 'MIB_REC_TYPE_BRANCH', 'MIB_REC_TYPE_VALUE', 'MIB_INDEX_FIELD_LENGTH', 
           'MIB_LABEL_FIELD_LENGTH', 'MIB_VAL_FIELD_LENGTH', 
           'SSMIF_STRUCT', 'STATION_SETTINGS_STRUCT', 'SUBSYSTEM_STATUS_STRUCT', 'SUBSUBSYSTEM_STATUS_STRUCT', 
           'SSF_STRUCT', 'OSF_STRUCT', 'OSFS_STRUCT', 'BEAM_STRUCT', 'OSF2_STRUCT', 
           'delay_to_mcsd', 'mcsd_to_delay', 'gain_to_mcsg', 'mcsg_to_gain',
           'mjdmpm_to_datetime', 'datetime_to_mjdmpm', 'status_to_string', 'summary_to_string', 'sid_to_string', 'cid_to_string', 
           'mode_to_string', 'parse_c_struct', 'flat_to_multi', 'apply_pointing_correction', 'MIB', 'MIBEntry']


ME_SSMIF_FORMAT_VERSION = 9	# SSMIF format version code
ME_MAX_NSTD = 256			# Maximum number of stands that can be described
ME_MAX_NFEE = 256			# Maximum number of FEEs that can be described
ME_MAX_FEEID_LENGTH = 10		# Number of characters in FEE ID name
ME_MAX_RACK = 6			# Maximum number of racks?
ME_MAX_PORT = 50			# Maximum number of ports?
ME_MAX_NRPD = 512			# Maxmimum number of RPD cables
ME_MAX_RPDID_LENGTH = 25		# Number of characters in the RPD ID name
ME_MAX_NSEP = 512			# Maximum number of SEP cable connections
ME_MAX_SEPID_LENGTH = 25		# Number of characters in the SEP ID name
ME_MAX_SEPCABL_LENGTH = 25	# Number of characters in the SEP cable ID name
ME_MAX_NARB = 32			# Maximum number of ARX boards
ME_MAX_NARBCH = 16			# Number of ARX channels per board
ME_MAX_ARBID_LENGTH = 10		# Number of characters in the ARX ID name
ME_MAX_NROACH = 16			# Maximum number of ROACH boards
ME_MAX_NROACHCH = 32		# Number of channels per ROACH board
ME_MAX_ROACHID_LENGTH = 10	# Number of characters in the ROACH board ID name
ME_MAX_NSERVER = 7			# Maximum number of server
ME_MAX_SERVERID_LENGTH = 10	# Number of characters in the server ID name
ME_MAX_NDR = 4				# Maximum number of data recorders
ME_MAX_DRID_LENGTH = 10		# Number of characters in the DR ID name
ME_MAX_NPWRPORT = 50		# Maximum number of power ports
ME_MAX_SSNAME_LENGTH = 3		# Number of characters in the power port ID names, for codes used for PWR_NAME
LWA_MAX_NSTD = 256			# Maximum number of stands for the LWA
TPSS_FORMAT_VERSION = 6		# MCS0030 format version code


SSMIF_STRUCT = """
    int    iFormatVersion;           /* FORMAT_VERSION */
    char   sStationID[3];            /* STATION_ID */
    double fGeoN;                    /* GEO_N */
    double fGeoE;                    /* GEO_E */
    double fGeoEl;                   /* GEO_EL */
    int    nStd;                     /* N_STD */
    double fStdLx[ME_MAX_NSTD];      /* STD_LX[] */
    double fStdLy[ME_MAX_NSTD];      /* STD_LY[] */
    double fStdLz[ME_MAX_NSTD];      /* STD_LZ[] */
    int    iAntStd[2*ME_MAX_NSTD];   /* ANT_STD[] */
    int    iAntOrie[2*ME_MAX_NSTD];  /* ANT_ORIE[] */
    int    iAntStat[2*ME_MAX_NSTD];  /* ANT_STAT[] */
    float  fAntTheta[2*ME_MAX_NSTD]; /* ANT_THETA[] */
    float  fAntPhi[2*ME_MAX_NSTD];   /* ANT_PHI[] */
    int    eAntDesi[2*ME_MAX_NSTD];  /* ANT_DESI[] */
    int    nFEE;                     /* N_FEE */
    char   sFEEID[ME_MAX_NFEE][ME_MAX_FEEID_LENGTH+1]; /* FEE_ID[] */
    int    iFEEStat[ME_MAX_NFEE];    /* FEE_STAT[] */
    int    eFEEDesi[ME_MAX_NFEE];    /* FEE_DESI[] */
    float  fFEEGai1[ME_MAX_NFEE];    /* FEE_GAI1[] */
    float  fFEEGai2[ME_MAX_NFEE];    /* FEE_GAI2[] */
    int    iFEEAnt1[ME_MAX_NFEE];    /* FEE_ANT1[] */
    int    iFEEAnt2[ME_MAX_NFEE];    /* FEE_ANT2[] */
    int    iFEERack[ME_MAX_NFEE];    /* FEE_RACK[] */
    int    iFEEPort[ME_MAX_NFEE];    /* FEE_PORT[] */
    int    nRPD;                     /* N_RPD */
    char   sRPDID[ME_MAX_NRPD][ME_MAX_RPDID_LENGTH+1]; /* RPD_ID[] */
    int    iRPDStat[ME_MAX_NRPD];    /* RPD_STAT[] */
    int    eRPDDesi[ME_MAX_NRPD];    /* RPD_DESI[] */
    float  fRPDLeng[ME_MAX_NRPD];    /* RPD_LENG[] */
    float  fRPDVF[ME_MAX_NRPD];      /* RPD_VF[] */
    float  fRPDDD[ME_MAX_NRPD];      /* RPD_DD[] */
    float  fRPDA0[ME_MAX_NRPD];      /* RPD_A0[] */
    float  fRPDA1[ME_MAX_NRPD];      /* RPD_A1[] */
    float  fRPDFref[ME_MAX_NRPD];    /* RPD_FREF[] */
    float  fRPDStr[ME_MAX_NRPD];     /* RPD_STR[] */
    int    iRPDAnt[ME_MAX_NRPD];     /* RPD_ANT[] */
    int    nSEP;                     /* N_SEP */
    char   sSEPID[ME_MAX_NSEP][ME_MAX_SEPID_LENGTH+1]; /* SEP_ID[] */
    int    iSEPStat[ME_MAX_NSEP];    /* SEP_STAT[] */
    char   sSEPCabl[ME_MAX_NSEP][ME_MAX_SEPCABL_LENGTH+1]; /* SEP_Cabl[] */
    float  fSEPLeng[ME_MAX_NSEP];    /* SEP_LENG[] */
    int    eSEPDesi[ME_MAX_NSEP];    /* SEP_DESI[] */
    float  fSEPGain[ME_MAX_NSEP];    /* SEP_GAIN[] */
    int    iSEPAnt[ME_MAX_NSEP];     /* SEP_ANT[] */
    int    nARB;                     /* N_ARB */
    int    nARBCH;                   /* N_ARBCH */
    char   sARBID[ME_MAX_NARB][ME_MAX_ARBID_LENGTH+1]; /* ARB_ID[] */
    int    iARBSlot[ME_MAX_NARB];    /* ARB_SLOT[] */
    int    eARBDesi[ME_MAX_NARB];    /* ARB_DESI[] */
    int    iARBRack[ME_MAX_NARB];    /* ARB_RACK[] */
    int    iARBPort[ME_MAX_NARB];    /* ARB_PORT[] */
    int    eARBStat[ME_MAX_NARB][ME_MAX_NARBCH];       /* ARB_STAT[][] */
    float  fARBGain[ME_MAX_NARB][ME_MAX_NARBCH];        /* ARB_GAIN[][] */
    int    iARBAnt[ME_MAX_NARB][ME_MAX_NARBCH];        /* ARB_ANT[][] */
    char   sARBIN[ME_MAX_NARB][ME_MAX_NARBCH][ME_MAX_ARBID_LENGTH+1]; /* ARB_IN[][] */
    char   sARBOUT[ME_MAX_NARB][ME_MAX_NARBCH][ME_MAX_ARBID_LENGTH+1]; /* ARB_OUT[][] */
    int    nRoach;                     /* N_ROACH */
    int    nRoachCh;                   /* N_ROACHCH */
    char   sRoachID[ME_MAX_NROACH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_ID[] */
    char   sRoachSlot[ME_MAX_NROACH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_SLOT[] */
    int    eRoachDesi[ME_MAX_NROACH]; /* ROACH_DESI[] */
    int    eRoachStat[ME_MAX_NROACH][ME_MAX_NROACHCH];       /* ROACH_STAT[][] */
    char   sRoachINR[ME_MAX_NROACH][ME_MAX_NROACHCH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_INR[][] */
    char   sRoachINC[ME_MAX_NROACH][ME_MAX_NROACHCH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_INC[][] */
    int    iRoachAnt[ME_MAX_NROACH][ME_MAX_NROACHCH];        /* ROACH_ANT[][] */
    int    nServer;                     /* N_SERVER */
    char   sServerID[ME_MAX_NSERVER][ME_MAX_SERVERID_LENGTH+1]; /* SERVER_ID[] */
    char   sServerSlot[ME_MAX_NSERVER][ME_MAX_SERVERID_LENGTH+1]; /* SERVER_SLOT[] */
    int    eServerStat[ME_MAX_NSERVER];       /* SERVER_STAT[] */
    int    eServerDesi[ME_MAX_NSERVER];       /* SERVER_DESI[] */
    int    nDR;                     /* N_DR */
    int    eDRStat[ME_MAX_NDR];       /* DR_STAT[] */
    char   sDRID[ME_MAX_NDR][ME_MAX_DRID_LENGTH+1]; /* DR_ID[] */
    char   sDRPC[ME_MAX_NDR][ME_MAX_DRID_LENGTH+1]; /* DR_PC[] */
    int    iDRDP[ME_MAX_NDR];       /* DR_DP[] */
    int    nPwrRack;                /* N_PWR_RACK */
    int    nPwrPort[ME_MAX_RACK];   /* N_PWR_PORT[] */
    int    ePwrSS[ME_MAX_RACK][ME_MAX_NPWRPORT]; /* PWR_SS[][], converted to a LWA_SID_ value */
    char   sPwrName[ME_MAX_RACK][ME_MAX_NPWRPORT][ME_MAX_SSNAME_LENGTH+1]; /* PWR_NAME[][] */
    int    eCRA;                /* MCS_CRA */
    float  fPCAxisTh; /* PC_AXIS_TH */
    float  fPCAxisPh; /* PC_AXIS_PH */
    float  fPCRot;    /* PC_ROT */
"""


STATION_SETTINGS_STRUCT = """
    signed short int mrp_asp; // SESSION_MRP_ASP // MRP_ASP
    signed short int mrp_dp;  // SESSION_MRP_DP_ // MRP_DP_
    signed short int mrp_dr1; // SESSION_MRP_DR1 // MRP_DR1
    signed short int mrp_dr2; // SESSION_MRP_DR2 // MRP_DR2
    signed short int mrp_dr3; // SESSION_MRP_DR3 // MRP_DR3
    signed short int mrp_dr4; // SESSION_MRP_DR4 // MRP_DR4
    signed short int mrp_dr5; // SESSION_MRP_DR5 // MRP_DR5
    signed short int mrp_shl; // SESSION_MRP_SHL // MRP_SHL
    signed short int mrp_mcs; // SESSION_MRP_MCS // MRP_MCS
    signed short int mup_asp; // SESSION_MUP_ASP // MUP_ASP
    signed short int mup_dp;  // SESSION_MUP_DP_ // MUP_DP_
    signed short int mup_dr1; // SESSION_MUP_DR1 // MUP_DR1
    signed short int mup_dr2; // SESSION_MUP_DR2 // MUP_DR2
    signed short int mup_dr3; // SESSION_MUP_DR3 // MUP_DR3
    signed short int mup_dr4; // SESSION_MUP_DR4 // MUP_DR4
    signed short int mup_dr5; // SESSION_MUP_DR5 // MUP_DR5
    signed short int mup_shl; // SESSION_MUP_SHL // MUP_SHL
    signed short int mup_mcs; // SESSION_MUP_MCS // MUP_MCS
    signed short int fee[LWA_MAX_NSTD];     // OBS_FEE[LWA_MAX_NSTD][2]  // FEE[LWA_MAX_NSTD]
    signed short int asp_flt[LWA_MAX_NSTD]; // OBS_ASP_FLT[LWA_MAX_NSTD] // ASP_FLT[LWA_MAX_NSTD]
    signed short int asp_at1[LWA_MAX_NSTD]; // OBS_ASP_AT1[LWA_MAX_NSTD] // ASP_AT1[LWA_MAX_NSTD]
    signed short int asp_at2[LWA_MAX_NSTD]; // OBS_ASP_AT2[LWA_MAX_NSTD] // ASP_AT2[LWA_MAX_NSTD]
    signed short int asp_ats[LWA_MAX_NSTD]; // OBS_ASP_ATS[LWA_MAX_NSTD] // ASP_ATS[LWA_MAX_NSTD]
    signed short int tbf_gain; // OBS_TBF_GAIN // TBF_GAIN
    signed short int tbn_gain; // OBS_TBN_GAIN // TBN_GAIN
    signed short int drx_gain; // OBS_DRX_GAIN // DRX_GAIN
"""


SUBSYSTEM_STATUS_STRUCT = """
    int summary;
    char info[256];
    long tv[2];
"""


SUBSUBSYSTEM_STATUS_STRUCT = """
    int    eFEEStat[ME_MAX_NFEE];                      /* FEE_STAT[] */
    int    eRPDStat[ME_MAX_NRPD];                      /* RPD_STAT[] */
    int    eSEPStat[ME_MAX_NSEP];                      /* SEP_STAT[] */
    int    eARBStat[ME_MAX_NARB][ME_MAX_NARBCH];       /* ARB_STAT[][] */
    int    eRoachStat[ME_MAX_NROACH][ME_MAX_NROACHCH]; /* ROACH_STAT[][] */
    int    eServerStat[ME_MAX_NSERVER];                /* SERVER_STAT[] */
    int    eDRStat[ME_MAX_NDR];                        /* DR_STAT[] */
"""


SSF_STRUCT = """
    unsigned short int FORMAT_VERSION;
    char PROJECT_ID[9];
    unsigned int SESSION_ID;
    unsigned short int SESSION_CRA;
    signed short int SESSION_DRX_BEAM;
    char SESSION_SPC[32];
    unsigned long int SESSION_START_MJD;
    unsigned long int SESSION_START_MPM;
    unsigned long int SESSION_DUR;
    unsigned int SESSION_NOBS;
    signed short int SESSION_MRP_ASP;
    signed short int SESSION_MRP_DP_;
    signed short int SESSION_MRP_DR1;
    signed short int SESSION_MRP_DR2;
    signed short int SESSION_MRP_DR3;
    signed short int SESSION_MRP_DR4;
    signed short int SESSION_MRP_DR5;
    signed short int SESSION_MRP_SHL;
    signed short int SESSION_MRP_MCS;
    signed short int SESSION_MUP_ASP;
    signed short int SESSION_MUP_DP_;
    signed short int SESSION_MUP_DR1;
    signed short int SESSION_MUP_DR2;
    signed short int SESSION_MUP_DR3;
    signed short int SESSION_MUP_DR4;
    signed short int SESSION_MUP_DR5;
    signed short int SESSION_MUP_SHL;
    signed short int SESSION_MUP_MCS;
    signed char SESSION_LOG_SCH;
    signed char SESSION_LOG_EXE;
    signed char SESSION_INC_SMIB;
    signed char SESSION_INC_DES;
"""


OSF_STRUCT = """
    unsigned short int FORMAT_VERSION;
    char               PROJECT_ID[9];
    unsigned int       SESSION_ID;
    signed short int   SESSION_DRX_BEAM;
    char               SESSION_SPC[32];
    unsigned int       OBS_ID; 
    unsigned long int  OBS_START_MJD;
    unsigned long int  OBS_START_MPM;
    unsigned long int  OBS_DUR;
    unsigned short int OBS_MODE;
    char               OBS_BDM[32];  /* added 140310 */
    float              OBS_RA;
    float              OBS_DEC;
    unsigned short int OBS_B;
    unsigned int       OBS_FREQ1;
    unsigned int       OBS_FREQ2;
    unsigned short int OBS_BW;
    unsigned int       OBS_STP_N;
    unsigned short int OBS_STP_RADEC;
"""


OSFS_STRUCT = """
    float              OBS_STP_C1;
    float              OBS_STP_C2;
    unsigned int       OBS_STP_T;
    unsigned int       OBS_STP_FREQ1;
    unsigned int       OBS_STP_FREQ2;
    unsigned short int OBS_STP_B;
"""


BEAM_STRUCT = """
    unsigned short int OBS_BEAM_DELAY[2*LWA_MAX_NSTD];
    signed short int   OBS_BEAM_GAIN[LWA_MAX_NSTD][2][2];
"""


OSF2_STRUCT = """
    signed short int   OBS_FEE[LWA_MAX_NSTD][2];
    signed short int   OBS_ASP_FLT[LWA_MAX_NSTD];
    signed short int   OBS_ASP_AT1[LWA_MAX_NSTD];
    signed short int   OBS_ASP_AT2[LWA_MAX_NSTD];
    signed short int   OBS_ASP_ATS[LWA_MAX_NSTD];
    unsigned int       OBS_TBF_SAMPLES;
    signed short int   OBS_TBF_GAIN;
    signed short int   OBS_TBN_GAIN;
    signed short int   OBS_DRX_GAIN;
    unsigned int       alignment;
"""


_cDecRE = re.compile(r'(?P<type>[a-z][a-z \t]+)[ \t]+(?P<name>[a-zA-Z_0-9]+)(\[(?P<d1>[\*\+A-Z_\d]+)\])?(\[(?P<d2>[\*\+A-Z_\d]+)\])?(\[(?P<d3>[\*\+A-Z_\d]+)\])?(\[(?P<d4>[\*\+A-Z_\d]+)\])?;')


def parse_c_struct(cStruct, char_mode='str', endianness='native', overrides=None):
    """
    Function to take a C structure declaration and build a ctypes.Structure out 
    of it with the appropriate alignment, character interpretation*, and endianness
    (little, big, network, or native).
    
    .. note::  ctypes converts character arrays to Python strings until the first null is
    incountered.  This behavior causes problems for multi-dimension arrays of null
    filled strings.  By setting char_mode to 'int', all char types are retuned as 
    bytes which can be converted to strings via chr().
    """
    
    # Process the macro overrides dictionary
    if overrides is None:
        overrides = {}
        
    # Figure out how to deal with character arrays
    if char_mode not in ('str', 'int'):
        raise RuntimeError("Unknown character mode: '%s'" % char_mode)
    if char_mode == 'str':
        baseCharType = ctypes.c_char
    else:
        baseCharType = ctypes.c_byte
    
    # Hold the basic fields and dimensions
    fields = []
    dims2 = {}
    
    # Split into lines and go!
    cStruct = cStruct.split('\n')
    for line in cStruct:
        ## Skip structure declaration, blank lines, comments, and lines too short to hold a 
        ## declaration
        line = line.strip().rstrip()
        if '{' in line or '}' in line:
            continue
        if line[:2] == '//':
            continue
        if len(line) < 5:
            continue
            
        ## RegEx the line to find the type, name, and dimensions (if needed) for
        ## the next structure variable
        mtch = _cDecRE.search(line)
        if mtch is None:
            raise RuntimeError("Unparseable line: '%s'" % line)
        
        dec = mtch.group('type')
        dec = dec.rstrip()
        name = mtch.group('name')
        
        try:
            d1 = mtch.group('d1')
            if d1 is not None:
                try:
                    d1 = overrides[d1]
                except KeyError:
                    d1 = eval(d1)
            d2 = mtch.group('d2')
            if d2 is not None:
                try:
                    d2 = overrides[d2]
                except KeyError:
                    d2 = eval(d2)
            d3 = mtch.group('d3')
            if d3 is not None:
                try:
                    d3 = overrides[d3]
                except KeyError:
                    d3 = eval(d3)
            d4 = mtch.group('d4')
            if d4 is not None:
                try:
                    d4 = overrides[d4]
                except KeyError:
                    d4 = eval(d4)
        except NameError:
            raise RuntimeError("Unknown value in array index: '%s'" % line)
        
        ## Basic data types
        if dec in ('signed int', 'int'):
            typ = ctypes.c_int
        elif dec == 'unsigned int':
            typ = ctypes.c_uint
        elif dec in ('signed short int', 'signed short', 'short int', 'short'):
            typ = ctypes.c_short
        elif dec in ('unsigned short int', 'unsigned short'):
            typ = ctypes.c_ushort
        elif dec in ('signed long int', 'signed long', 'long int', 'long'):
            typ = ctypes.c_long
        elif dec in ('unsigned long int', 'unsigned long'):
            typ = ctypes.c_ulong
        elif dec in ('signed long long', 'long long'):
            typ = ctypes.c_longlong
        elif dec == 'unsigned long long':
            typ = ctypes.c_uint64
        elif dec == 'float':
            typ = ctypes.c_float
        elif dec == 'double':
            typ = ctypes.c_double
        elif dec == 'char':
            typ = baseCharType
        elif dec == 'signed char':
            typ = ctypes.c_byte
        elif dec == 'unsigned char':
            typ = ctypes.c_ubyte
        else:
            raise RuntimeError("Unparseable line: '%s' -> type: %s, name: %s, dims: %s, %s, %s %s" % (line, dec, name, d1, d2, d3, d4))
        
        ## Array identification and construction
        dims2[name] = []
        if d1 is not None:
            count = d1
            dims2[name].append(d1)
            
            if d2 is not None:
                count *= d2
                dims2[name].append(d2)
            if d3 is not None:
                count *= d3
                dims2[name].append(d3)
            if d4 is not None:
                count *= d4
                dims2[name].append(d4)
                
            typ *= count
        
        ## Append
        fields.append( (name, typ) )
    
    # ctypes creation - endianess
    endianness = endianness.lower()
    if endianness not in ('little', 'big', 'network', 'native'):
        raise RuntimeError("Unknown endianness: '%s'" % endianness)
    
    if endianness == 'little':
        endianness = ctypes.LittleEndianStructure
    elif endianness == 'big':
        endianness = ctypes.BigEndianStructure
    elif endianness == 'network':
        endianness = ctypes.BigEndianStructure
    else:
        endianness = ctypes.Structure
    
    # ctypes creation - actual
    class MyStruct(endianness):
        """
        ctypes.Structure of the correct endianness for the provided
        C structure.  
        
        In addition to the standard attributes defined for a ctypes.Structure 
        instance there are a few additional attributes related to the parsed C
        structure.  They are:
         * origC - String containing the original C structure
         * dims  - Dictionary of the dimensionallity of the data, if needed, 
                   keyed by variable name
        """
        
        origC = '\n'.join(cStruct)
        
        _fields_ = fields
        _pack_ = 8	# Pack it like we are 64-bit
        dims = dims2
        
        def __str__(self):
            """
            Print out the structure in a nice easy-to-read formation that
            captures the various structure elements, their data types, and 
            their values.
            """
            
            out = ''
            for f,d in self._fields_:
                out += '%s (%s): %s\n' % (f, d, eval("self.%s" % f))
            return out
            
        def sizeof(self):
            """
            Return the size, in bytes, of the structure.
            """
            
            return ctypes.sizeof(self)
            
        def returnDict(self):
            """
            Return the structure as a simple Python dictionary keyed off the
            structure elements.
            """
            
            output = {}
            for f,d in self._fields_:
                output[f] = eval("self.%s" % f)
            return output
    
    # Create and return
    return MyStruct()


def _two_bytes_swap(value):
    return ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)


def delay_to_mcsd(delay):
    """
    Given a delay in ns, convert it to a course and fine portion and into 
    the form expected by MCS in a custom beamforming SDF (little endian 
    16.12 unsigned integer).

    .. versionadded:: 0.6.3
    """
    
    return _two_bytes_swap( adpCommon.delay_to_dpd(delay) )


def mcsd_to_delay(delay):
    """
    Given delay value from an OBS_BEAM_DELAY field in a custom beamforming 
    SDF, return the delay in ns.

    .. versionadded:: 0.6.3
    """
    
    return adpCommon.dpd_to_delay( _two_bytes_swap(delay) )


def gain_to_mcsg(gain):
    """
    Given a gain (between 0 and 1), convert it to a gain in the form 
    expected by MCS in a custom beamforming SDF (little endian 16.1 
    signed integer).

    .. versionadded::0.6.3
    """
    
    return _two_bytes_swap( adpCommon.gain_to_dpg(gain) )


def mcsg_to_gain(gain):
    """
    Given a gain value from an OBS_BEAM_GAIN field in a custom beamforming
    SDF, return the decimal equivalent.

    .. versionadded:: 0.6.3
    """
    
    return adpCommon.dpg_to_gain( _two_bytes_swap(gain) )
