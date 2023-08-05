# -*- coding:utf-8 -*-
""" LS PDO MAPPING """
# !/usr/bin/python
# Python:   3.6.5+
# Platform: Windows/Linux/Raspberry
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  LS PDO MAPPING( L7N Series ).
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
        self.axis_pdo = OrderedDict( cw = dict( value=0, offset=0, size=2, index=0x6040, alias='Control Word'    ),
                                     tp = dict( value=0, offset=2, size=4, index=0x607A, alias='Target Position' ) )

class rx_pdo_mapping_csv( ecmxf_pdo_mapping ):
    """ Index = 0x1601 """
    def __init__( self ) -> None:
        super( rx_pdo_mapping_csv, self ).__init__( )
        self.map_index= 0x1601
        self.axis_pdo = OrderedDict( cw = dict( value=0, offset=0, size=2, index=0x6040, alias='Control Word'    ),
                                     tp = dict( value=0, offset=2, size=4, index=0x60FF, alias='Target Velocity' ) )

class rx_pdo_mapping_cst( ecmxf_pdo_mapping ):
    """ Index = 0x1602 """
    def __init__( self ) -> None:
        super( rx_pdo_mapping_cst, self ).__init__( )
        self.map_index= 0x1602
        self.axis_pdo = OrderedDict( cw = dict( value=0, offset=0, size=2, index=0x6040, alias='Control Word'  ),
                                     tp = dict( value=0, offset=2, size=4, index=0x6071, alias='Target Torque' ) )


class tx_pdo_mapping_csp( ecmxf_pdo_mapping ):
    """ Index = 0x1A00 """
    def __init__( self ) -> None:
        super( tx_pdo_mapping_csp, self ).__init__( )
        self.map_index= 0x1A00
        self.axis_pdo = OrderedDict( sw = dict( value=0, offset=0, size=2, index=0x6041, ro=False, alias='Status Word'           ),
                                     pv = dict( value=0, offset=2, size=4, index=0x6064, ro=True,  alias='Position Actual Value' ) )

class tx_pdo_mapping_csv( ecmxf_pdo_mapping ):
    """ Index = 0x1A01 """
    def __init__( self ) -> None:
        super( tx_pdo_mapping_csv, self ).__init__( )
        self.map_index= 0x1A01
        self.axis_pdo = OrderedDict( sw = dict( value=0, offset=0, size=2, index=0x6041, ro=False, alias='Status Word'           ),
                                     pv = dict( value=0, offset=2, size=4, index=0x6064, ro=True,  alias='Position Actual Value' ) )

class tx_pdo_mapping_cst( ecmxf_pdo_mapping ):
    """ Index = 0x1A02 """
    def __init__( self ) -> None:
        super( tx_pdo_mapping_cst, self ).__init__( )
        self.map_index= 0x1A02
        self.axis_pdo = OrderedDict( sw = dict( value=0, offset=0, size=2, index=0x6041, ro=False, alias='Status Word'           ),
                                     pv = dict( value=0, offset=2, size=4, index=0x6064, ro=True,  alias='Position Actual Value' ) )

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
