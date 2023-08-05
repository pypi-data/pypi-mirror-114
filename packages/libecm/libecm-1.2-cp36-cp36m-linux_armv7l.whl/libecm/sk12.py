# -*- coding:utf-8 -*-
""" Library for NEXTW ECM(SK\XF) Module. """
# !/usr/bin/python
# Python:   3.6.5+
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Library for NEXTW ECM(SK\XF) Module.
# History:  2020-08-18 Wheel Ver:0.1 [Heyn] Initialize
#           2020-09-07 Wheel Ver:0.2 [Heyn] New add read and write SDO

import logging
from .ecm_sk12 import *

from libecm import ecm_sk12 as ethercat

class sdo( object ):
    """
    Write SDO -> sdo( 1, 0x2106, alias='Speed P Gain 1', size=2 ).value = 50
    Read  SDO -> sdo( 1, 0x2106, alias='Speed P Gain 1', size=2 ).value
    """

    def __init__( self, slave=1, index=0, subindex=0, size=1, alias='' ) -> None:
        self.alias = alias
        self.slave, self.index, self.subindex, self.size = slave, index, subindex, size

    @property
    def value( self ):
        result = ethercat.read_sdo( slave=self.slave, index=self.index, subindex=self.subindex )
        logging.debug( '{} ( 0x{:08X} ) = {} (READ)'.format( self.alias, result['object'], result['values'] ) )
        return result['values']

    @value.setter
    def value( self, value ):
        param = ( ( self.index << 16 | self.subindex ) & 0xFFFFFFFF )
        logging.debug( '{} ( 0x{:08X} ) = {}, SIZE={} (WRITE)'.format( self.alias, param, value, self.size ) )
        ethercat.write_sdo( slave=self.slave, param=param, size=self.size, value=value  )
