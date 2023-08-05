# -*- coding:utf-8 -*-
""" hexinSigmoid """
# !/usr/bin/python
# Python:   3.6.5+
# Platform: Windows/Linux/MacOS
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  hexinSigmoid.
# Package:  pip install numpy
#           pip install matplotlib scipy
# History:  2020-09-27 Ver:1.0 [Heyn] Initialization
#           2021-05-24 Ver:1.1 [Heyn] Optimized code
#           2021-06-02 Ver:1.1 [Heyn] New add plot_acc, plot and rename values to position
#           2021-07-02 Ver:1.2 [Heyn] Bug fixed.

import logging
import numpy as np

class hexinSigmoid( object ):
    """
        TEST = hexinSigmoid( dsitclock=5 )
        TEST.position( cpos=0, tpos=1000, ms=500, flexible=6 )
        print( len( TEST ) )

        TEST.plot_pos( cpos=0, tpos=1000, ms=500, flexible=6 )
        TEST.plot_acc( cpos=0, tpos=1000, ms=500, flexible=6 )
        TEST.plot_all( cpos=0, tpos=1000, ms=500, flexible=6 )
    """
    def __init__( self, dsitclock:int=5 ) -> None:
        super( hexinSigmoid, self ).__init__()
        self.__tpos, self.__data, self.dsitclock = 0, [], dsitclock

    def __curve( self, x, inflection:float, flexible:float=6, ymin:float=0, ymax:float=1 ):
        """
            inflection : It's yman value
        """
        inflection = ( 1 if inflection == 0 else inflection )
        ax = flexible / inflection
        bx = flexible
        return ( ymin + (ymax-ymin) / ( 1 + np.exp( -ax*x + bx ) ) )


    def position( self, cpos=0, tpos=0, ms:int=500, flexible:float=6, inflection:float=500 ) -> list:
        """
            cpos : current position.
            tpos : target  position.
        """
        if ( cpos == tpos ) or ( ms <= 0 ):
            self.__data = [ int(tpos) ]
            self.__size = 1
            return self.__data

        self.__data = self.__curve( x          = np.arange( 0, ms, self.dsitclock ),
                                    inflection = inflection,
                                    flexible   = flexible,
                                    ymin       = cpos,
                                    ymax       = tpos )

        logging.debug('MAX POSITION/ms  {}'.format( max( list( map( int, self.__data[1:] - self.__data[0:-1] ) ) ) // self.dsitclock ) )
        
        self.__data = list( map( int, self.__data ) )
        self.__size = len( self.__data )
        self.__tpos = tpos

        logging.debug('*'*30)
        logging.debug('CURRENT POSITION {}'.format( cpos ) )
        logging.debug('TARGET  POSITION {}'.format( tpos )  )
        logging.debug('DATA SIZE        {}'.format( self.__size ) )
        logging.debug('STARTUP VALUE    {}'.format( self.__data[0]  ) )
        logging.debug('FINAL POSITION   {}'.format( self.__data[-1] ) )
        logging.debug('FINAL DEVIATION  {}'.format( tpos - self.__data[-1] ) )
        logging.debug('*'*30)
        return self.__data

    def position_tail( self ) -> int:
        """ Get Actual Position. """
        return self.__data[-1]

    def plot_pos( self, cpos=0, tpos=0, ms:int=500, flexible:float=6, inflection:float=4/5 ) -> None:
        import matplotlib.pyplot as plt
        self.position( cpos=cpos, tpos=tpos, ms=ms, flexible=flexible, inflection=inflection )
        plt.plot( np.arange( 0, len(self.__data) ), self.__data )
        plt.show()

    def __acc( self, cpos=0, tpos=0, ms:int=500, flexible:float=6, inflection:float=500 ):
        from scipy.misc import derivative

        return derivative( func = self.__curve,
                           x0   = np.arange( 0, ms, self.dsitclock ),
                           dx   = 1e-6,
                           n    = 1,
                           args = ( inflection,
                                    flexible,
                                    cpos,
                                    tpos ) )
    
    @staticmethod
    def __acc_axis_xy( acc:np.ndarray ) -> tuple:
        try:
            acc_y = min(acc) if max( acc ) <= 0 else max( acc )
            acc_x = np.where( acc == acc_y )[0][0]
        except BaseException:
            return 0, 0
        return acc_x, acc_y

    def plot_acc( self, cpos=0, tpos=0, ms:int=500, flexible:float=6, inflection:float=500) -> None:
        """ Get acceleration dv/dt """
        import matplotlib.pyplot as plt
        acc = self.__acc( cpos=cpos, tpos=tpos, ms=ms, flexible=flexible, inflection=inflection )
        plt.plot( np.arange( 0, len(acc) ), acc )
        x, y = self.__acc_axis_xy( acc )
        plt.text( x, y, 'Max ACC = {:.2f} scale/ms'.format( y ) )
        plt.show()

    def plot_all( self, cpos=0, tpos=0, ms:int=500, flexible:float=6, inflection:float=500, max_pos_ms:int=int(6450/60*2**17/1000) ) -> None:
        import matplotlib.pyplot as plt
        pos = self.position( cpos=cpos, tpos=tpos, ms=ms, flexible=flexible, inflection=inflection )
        acc = self.__acc(    cpos=cpos, tpos=tpos, ms=ms, flexible=flexible, inflection=inflection )
        
        # plt.style.use( 'dark_background' )
        fig, ax1 = plt.subplots()
        ax1.set_xlabel( 'time (ms)' )
        ax1.set_ylabel( 'pos', color='tab:blue' )
        ax1.plot( np.arange( 0, len(pos) ), pos, 'b-', color='tab:blue' )
        ax1.tick_params( axis='y', labelcolor='tab:blue' )
        ax1.text( len(pos)//2, self.position_tail()//2, 'offset = {}'.format( tpos-self.position_tail() ), color='tab:blue' )

        ax2 = ax1.twinx()

        ax2.set_ylabel( 'acc', color='tab:red' )
        ax2_axis_x_arange = np.arange( 0, len(acc) )

        ax2.plot( ax2_axis_x_arange, acc, 'r-', color='tab:red' )

        x, y = self.__acc_axis_xy( acc )
        ax2.text( x, y, 'max = {:.2f} pos/ms'.format( y ), color='tab:red' )
        ax2.tick_params( axis='y', labelcolor='tab:red' )

        ax2_axis_y_arange_line = np.array([max_pos_ms*self.dsitclock]*len(acc))
        ax2.plot( ax2_axis_x_arange, ax2_axis_y_arange_line, 'c:', color='black' )
        ax2.text( 0, max_pos_ms*self.dsitclock, 'max = {:.2f} pos'.format( max_pos_ms*self.dsitclock ), color='black' )
        
        ax2.fill_between( ax2_axis_x_arange,
                          acc,
                          ax2_axis_y_arange_line,
                          where=acc>=ax2_axis_y_arange_line,
                          facecolor='red',
                          interpolate=True)

        fig.tight_layout()
        plt.show()

    def __str__( self ) -> str:
        return 'DATA SIZE       = {}\nSTARTUP VALUE   = {}\nFINAL POSITION  = {}\nFINAL DEVIATION = {}\n'.format( self.__size,
                                                                                                                  self.__data[0],
                                                                                                                  self.__data[-1],
                                                                                                                  self.__tpos - self.__data[-1] )

    def __len__( self ) -> int:
        return self.__size

# End
