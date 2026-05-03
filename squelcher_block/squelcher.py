# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Squelcher block
# Author: krakenrf
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore







class squelcher(gr.hier_block2, Qt.QWidget):
    def __init__(self, decimation=128, samp_rate=1200000):
        gr.hier_block2.__init__(
            self, "Squelcher block",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        Qt.QWidget.__init__(self)
        self.top_layout = Qt.QVBoxLayout()
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)
        self.setLayout(self.top_layout)

        ##################################################
        # Parameters
        ##################################################
        self.decimation = decimation
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.delay_time_s = delay_time_s = 2
        self.alpha_iir = alpha_iir = 0.01

        ##################################################
        # Blocks
        ##################################################
        self._delay_time_s_range = Range(0, 5, 0.5, 2, 200)
        self._delay_time_s_win = RangeWidget(self._delay_time_s_range, self.set_delay_time_s, "'delay_time_s'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_time_s_win)
        self._alpha_iir_range = Range(0, 1, 0.01, 0.01, 200)
        self._alpha_iir_win = RangeWidget(self._alpha_iir_range, self.set_alpha_iir, "'alpha_iir'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._alpha_iir_win)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(alpha_iir, 1)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.99, 1, 0)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(3)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, int((delay_time_s)*(samp_rate/decimation)))
        self.blocks_complex_to_mag_1 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self, 0), (self.blocks_complex_to_mag_1, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))


    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.blocks_delay_0.set_dly(int((self.delay_time_s)*(self.samp_rate/self.decimation)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_delay_0.set_dly(int((self.delay_time_s)*(self.samp_rate/self.decimation)))

    def get_delay_time_s(self):
        return self.delay_time_s

    def set_delay_time_s(self, delay_time_s):
        self.delay_time_s = delay_time_s
        self.blocks_delay_0.set_dly(int((self.delay_time_s)*(self.samp_rate/self.decimation)))

    def get_alpha_iir(self):
        return self.alpha_iir

    def set_alpha_iir(self, alpha_iir):
        self.alpha_iir = alpha_iir
        self.single_pole_iir_filter_xx_0.set_taps(self.alpha_iir)

