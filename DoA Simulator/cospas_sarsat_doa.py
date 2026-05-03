# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Cospas-Sarsat DoA Simulator (5-Channel KrakenSDR Sim)
# Author: GNU Radio DoA Simulator
# Description: Cospas-Sarsat DoA Simulator
# GNU Radio version: 3.10.1.1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore







class cospas_sarsat_doa(gr.hier_block2, Qt.QWidget):
    def __init__(self):
        gr.hier_block2.__init__(
            self, "Cospas-Sarsat DoA Simulator (5-Channel KrakenSDR Sim)",
                gr.io_signature(0, 0, 0),
                gr.io_signature.makev(5, 5, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
        )

        Qt.QWidget.__init__(self)
        self.top_layout = Qt.QVBoxLayout()
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)
        self.setLayout(self.top_layout)

        ##################################################
        # Variables
        ##################################################
        self.theta_deg = theta_deg = 45
        self.samp_rate = samp_rate = 48000
        self.bit_rate = bit_rate = 400
        self.antenna_spacing = antenna_spacing = 0.5
        self.sps = sps = int(samp_rate / bit_rate)
        self.phase4 = phase4 = __import__('cmath').exp(1j * 2 * __import__('math').pi * antenna_spacing * 4 * __import__('math').sin(__import__('math').radians(theta_deg)))
        self.phase3 = phase3 = __import__('cmath').exp(1j * 2 * __import__('math').pi * antenna_spacing * 3 * __import__('math').sin(__import__('math').radians(theta_deg)))
        self.phase2 = phase2 = __import__('cmath').exp(1j * 2 * __import__('math').pi * antenna_spacing * 2 * __import__('math').sin(__import__('math').radians(theta_deg)))
        self.phase1 = phase1 = __import__('cmath').exp(1j * 2 * __import__('math').pi * antenna_spacing * 1 * __import__('math').sin(__import__('math').radians(theta_deg)))
        self.phase0 = phase0 = complex(1, 0)
        self.noise_amp = noise_amp = 0.05
        self.carrier_freq = carrier_freq = 1000
        self.beacon_bits = beacon_bits = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,1,1,1,1, 0,1,0,0,0,0,0,1, 0,0,1,0,1,1,0,0,1,0,1,0, 0,1,0,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1,0,1, 1,0,1,0,1,0,1,0,1,0, 1,0,1,0,1,0,1,0,1,0, 1,0,1,0,1,0,1,0,1,0]

        ##################################################
        # Blocks
        ##################################################
        self.vector_source_0 = blocks.vector_source_b(beacon_bits, True, 1, [])
        self._theta_deg_range = Range(-180, 180, 1, 45, 200)
        self._theta_deg_win = RangeWidget(self._theta_deg_range, self.set_theta_deg, "Angle of Incidence (degrees)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._theta_deg_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_chunks_to_symbols_0 = digital.chunks_to_symbols_bf([1,-1], 1)
        self.blocks_vector_source_x_0 = blocks.vector_source_c([complex(1,0)] * int(samp_rate * 0.5) + [complex(0,0)] * int(samp_rate * 5.0), True, 1, [])
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, sps)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_ch4 = blocks.multiply_const_cc(phase4)
        self.blocks_multiply_ch3 = blocks.multiply_const_cc(phase3)
        self.blocks_multiply_ch2 = blocks.multiply_const_cc(phase2)
        self.blocks_multiply_ch1 = blocks.multiply_const_cc(phase1)
        self.blocks_multiply_ch0 = blocks.multiply_const_cc(phase0)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_noise = blocks.add_vcc(1)
        self.analog_sig_source_carrier = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, carrier_freq, 1.0, 0, 0)
        self.analog_noise_source = analog.noise_source_c(analog.GR_GAUSSIAN, noise_amp, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source, 0), (self.blocks_add_noise, 1))
        self.connect((self.analog_sig_source_carrier, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_noise, 0), (self.blocks_multiply_ch0, 0))
        self.connect((self.blocks_add_noise, 0), (self.blocks_multiply_ch1, 0))
        self.connect((self.blocks_add_noise, 0), (self.blocks_multiply_ch2, 0))
        self.connect((self.blocks_add_noise, 0), (self.blocks_multiply_ch3, 0))
        self.connect((self.blocks_add_noise, 0), (self.blocks_multiply_ch4, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_ch0, 0), (self, 3))
        self.connect((self.blocks_multiply_ch1, 0), (self, 0))
        self.connect((self.blocks_multiply_ch2, 0), (self, 1))
        self.connect((self.blocks_multiply_ch3, 0), (self, 2))
        self.connect((self.blocks_multiply_ch4, 0), (self, 4))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_noise, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_xx_0, 2))
        self.connect((self.digital_chunks_to_symbols_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.vector_source_0, 0), (self.digital_chunks_to_symbols_0, 0))


    def get_theta_deg(self):
        return self.theta_deg

    def set_theta_deg(self, theta_deg):
        self.theta_deg = theta_deg
        self.set_phase1(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 1 * __import__('math').sin(__import__('math').radians(self.theta_deg))))
        self.set_phase2(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 2 * __import__('math').sin(__import__('math').radians(self.theta_deg))))
        self.set_phase3(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 3 * __import__('math').sin(__import__('math').radians(self.theta_deg))))
        self.set_phase4(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 4 * __import__('math').sin(__import__('math').radians(self.theta_deg))))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(int(self.samp_rate / self.bit_rate))
        self.analog_sig_source_carrier.set_sampling_freq(self.samp_rate)
        self.blocks_vector_source_x_0.set_data([complex(1,0)] * int(self.samp_rate * 0.5) + [complex(0,0)] * int(self.samp_rate * 5.0), [])

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.set_sps(int(self.samp_rate / self.bit_rate))

    def get_antenna_spacing(self):
        return self.antenna_spacing

    def set_antenna_spacing(self, antenna_spacing):
        self.antenna_spacing = antenna_spacing
        self.set_phase1(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 1 * __import__('math').sin(__import__('math').radians(self.theta_deg))))
        self.set_phase2(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 2 * __import__('math').sin(__import__('math').radians(self.theta_deg))))
        self.set_phase3(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 3 * __import__('math').sin(__import__('math').radians(self.theta_deg))))
        self.set_phase4(__import__('cmath').exp(1j * 2 * __import__('math').pi * self.antenna_spacing * 4 * __import__('math').sin(__import__('math').radians(self.theta_deg))))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_repeat_0.set_interpolation(self.sps)

    def get_phase4(self):
        return self.phase4

    def set_phase4(self, phase4):
        self.phase4 = phase4
        self.blocks_multiply_ch4.set_k(self.phase4)

    def get_phase3(self):
        return self.phase3

    def set_phase3(self, phase3):
        self.phase3 = phase3
        self.blocks_multiply_ch3.set_k(self.phase3)

    def get_phase2(self):
        return self.phase2

    def set_phase2(self, phase2):
        self.phase2 = phase2
        self.blocks_multiply_ch2.set_k(self.phase2)

    def get_phase1(self):
        return self.phase1

    def set_phase1(self, phase1):
        self.phase1 = phase1
        self.blocks_multiply_ch1.set_k(self.phase1)

    def get_phase0(self):
        return self.phase0

    def set_phase0(self, phase0):
        self.phase0 = phase0
        self.blocks_multiply_ch0.set_k(self.phase0)

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.analog_noise_source.set_amplitude(self.noise_amp)

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.analog_sig_source_carrier.set_frequency(self.carrier_freq)

    def get_beacon_bits(self):
        return self.beacon_bits

    def set_beacon_bits(self, beacon_bits):
        self.beacon_bits = beacon_bits
        self.vector_source_0.set_data(self.beacon_bits, [])

