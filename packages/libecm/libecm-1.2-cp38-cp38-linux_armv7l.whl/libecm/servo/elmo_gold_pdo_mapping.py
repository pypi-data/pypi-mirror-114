# -*- coding:utf-8 -*-
""" ELMO GOLD PDO MAPPING """
# !/usr/bin/python
# Python:   3.6.5+
# Platform: Windows/Linux/Raspberry
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  ELMO GOLD PDO MAPPING.
# Package:  pip install libecm
# History:  2021-05-17 Ver:1.0 [Heyn] Initialization
#           2021-05-31 Ver:1.1 [Heyn] New tx_pdo_mapping_xxx -> axis_pdo ro(read only) keywords

from collections  import OrderedDict
from libecm.ecmxf import ecmxf_pdo_mapping
from libecm.ecmxf import MODE_CSP, MODE_CSV, MODE_CST

class rx_pdo_mapping_csp( ecmxf_pdo_mapping ):
    """ Index = 0x1600 """
    def __init__( self ) -> None:
        super( rx_pdo_mapping_csp, self ).__init__( )
        self.map_index= 0x1600
        self.axis_pdo = OrderedDict( tp = dict( value=0, offset=0, size=4, index=0x607A, alias='Target Position' ),
                                     do = dict( value=0, offset=4, size=4, index=0x60FE, alias='Digital Outputs' ),
                                     cw = dict( value=0, offset=8, size=2, index=0x6040, alias='Control Word'    ) )

class rx_pdo_mapping_csv( ecmxf_pdo_mapping ):
    """ Index = 0x1601 """
    def __init__( self ) -> None:
        super( rx_pdo_mapping_csv, self ).__init__( )
        self.map_index= 0x1601
        self.axis_pdo = OrderedDict( tp = dict( value=0, offset=0, size=4, index=0x60FF, alias='Target Velocity' ),
                                     cw = dict( value=0, offset=4, size=2, index=0x6040, alias='Control Word'    ) )

class rx_pdo_mapping_cst( ecmxf_pdo_mapping ):
    """ Index = 0x1602 """
    def __init__( self ) -> None:
        super( rx_pdo_mapping_cst, self ).__init__( )
        self.map_index= 0x1602
        self.axis_pdo = OrderedDict( tp = dict( value=0, offset=0, size=2, index=0x6071, alias='Target Torque' ),
                                     cw = dict( value=0, offset=2, size=2, index=0x6040, alias='Control Word'  ) )


class tx_pdo_mapping_csp( ecmxf_pdo_mapping ):
    """ Index = 0x1A00 """
    def __init__( self ) -> None:
        super( tx_pdo_mapping_csp, self ).__init__( )
        self.map_index= 0x1A00
        self.axis_pdo = OrderedDict( pv = dict( value=0, offset=0, size=4, index=0x6064, ro=True,  alias='Position Actual Value' ),
                                     di = dict( value=0, offset=4, size=4, index=0x60FD, ro=False, alias='Digital Inputs'        ),
                                     sw = dict( value=0, offset=8, size=2, index=0x6041, ro=False, alias='Status Word'           ) )

class tx_pdo_mapping_csv( ecmxf_pdo_mapping ):
    """ Index = 0x1A01 """
    def __init__( self ) -> None:
        super( tx_pdo_mapping_csv, self ).__init__( )
        self.map_index= 0x1A01
        self.axis_pdo = OrderedDict( pv = dict( value=0, offset=0,  size=4, index=0x6064, ro=False, alias='Position Actual Value' ),
                                     vd = dict( value=0, offset=4,  size=4, index=0x606B, ro=True,  alias='Velocity Demand Value' ),
                                     tv = dict( value=0, offset=8,  size=2, index=0x6074, ro=True,  alias='Torque  Demand Value'  ),
                                     sw = dict( value=0, offset=10, size=2, index=0x6041, ro=False, alias='Status Word'           ) )

class tx_pdo_mapping_cst( ecmxf_pdo_mapping ):
    """ Index = 0x1A02 """
    def __init__( self ) -> None:
        super( tx_pdo_mapping_cst, self ).__init__( )
        self.map_index= 0x1A02
        self.axis_pdo = OrderedDict( pv = dict( value=0, offset=0, size=4, index=0x6064, ro=False, alias='Position Actual Value'     ),
                                     tv = dict( value=0, offset=4, size=2, index=0x6077, ro=True,  alias='Torque Actual Value'       ),
                                     sw = dict( value=0, offset=6, size=2, index=0x6041, ro=False, alias='Status Word'               ),
                                     md = dict( value=0, offset=8, size=1, index=0x6061, ro=False, alias='Mode Of Operation Display' ),
                                     xx = dict( value=0, offset=9, size=1, index=0x0000, ro=False, alias=''                          ) )


ETHCAT_RX_PDO_MAPPING = { MODE_CSP : rx_pdo_mapping_csp,
                          MODE_CSV : rx_pdo_mapping_csv,
                          MODE_CST : rx_pdo_mapping_cst
                        }

ETHCAT_TX_PDO_MAPPING = { MODE_CSP : tx_pdo_mapping_csp,
                          MODE_CSV : tx_pdo_mapping_csv,
                          MODE_CST : tx_pdo_mapping_cst
                        }

def get_rx_pdo_mapping( modes:list=[] ) -> list:
    return [ ETHCAT_RX_PDO_MAPPING[mode]() for mode in modes ]

def get_tx_pdo_mapping( modes:list=[] ) -> list:
    return [ ETHCAT_TX_PDO_MAPPING[mode]() for mode in modes ]
