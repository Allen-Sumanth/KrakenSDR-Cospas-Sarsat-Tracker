#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
import logging as log

def get_state_directory() -> str:
    oldpath = os.path.expanduser("~/.grc_gnuradio")
    try:
        from gnuradio.gr import paths
        newpath = paths.persistent()
        if os.path.exists(newpath):
            return newpath
        if os.path.exists(oldpath):
            log.warning(f"Found persistent state path '{newpath}', but file does not exist. " +
                     f"Old default persistent state path '{oldpath}' exists; using that. " +
                     "Please consider moving state to new location.")
            return oldpath
        # Default to the correct path if both are configured.
        # neither old, nor new path exist: create new path, return that
        os.makedirs(newpath, exist_ok=True)
        return newpath
    except (ImportError, NameError):
        log.warning("Could not retrieve GNU Radio persistent state directory from GNU Radio. " +
                 "Trying defaults.")
        xdgstate = os.getenv("XDG_STATE_HOME", os.path.expanduser("~/.local/state"))
        xdgcand = os.path.join(xdgstate, "gnuradio")
        if os.path.exists(xdgcand):
            return xdgcand
        if os.path.exists(oldpath):
            log.warning(f"Using legacy state path '{oldpath}'. Please consider moving state " +
                     f"files to '{xdgcand}'.")
            return oldpath
        # neither old, nor new path exist: create new path, return that
        os.makedirs(xdgcand, exist_ok=True)
        return xdgcand

sys.path.append(os.environ.get('GRC_HIER_PATH', get_state_directory()))

from PyQt5 import QtCore
from cospas_sarsat_doa import cospas_sarsat_doa  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import krakensdr
from squelcher import squelcher  # grc-generated hier_block
import kraken_music_doa_epy_block_0 as epy_block_0  # embedded python block
import sip
import threading



class kraken_music_doa(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "kraken_music_doa")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.theta_deg = theta_deg = 45
        self.samp_rate = samp_rate = 2400000
        self.freq = freq = 406.025
        self.delay_time_s_0 = delay_time_s_0 = 2
        self.decimation = decimation = 128
        self.cpi_size = cpi_size = 2**20
        self.alpha_iir_0 = alpha_iir_0 = 0.01
        self.Nv = Nv = 0.2

        ##################################################
        # Blocks
        ##################################################

        self._theta_deg_range = qtgui.Range(0, 360, 1, 45, 200)
        self._theta_deg_win = qtgui.RangeWidget(self._theta_deg_range, self.set_theta_deg, "Angle of Incidence (degrees)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._theta_deg_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Nv_range = qtgui.Range(0, 1, 0.01, 0.2, 200)
        self._Nv_win = qtgui.RangeWidget(self._Nv_range, self.set_Nv, "Noise voltage", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Nv_win)
        self.squelcher_0 = squelcher(
            alpha_iir=0.01,
            decimation=decimation,
            delay_time_s=2,
            samp_rate=samp_rate,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            360, #size
            1000, #samp_rate
            'DOA Graph', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (samp_rate//decimation), #bw
            'CH_0 Decimated FFT', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.1)
        self.qtgui_freq_sink_x_0.set_y_axis((-60), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.krakensdr_doa_music_0 = krakensdr.doa_music((cpi_size//decimation), freq, 0.22, 5, 'UCA')
        self.fir_filter_xxx_0_0_2 = filter.fir_filter_ccc(decimation, firdes.low_pass(1.0, samp_rate, (samp_rate/decimation)/2, 1000))
        self.fir_filter_xxx_0_0_2.declare_sample_delay(0)
        self.fir_filter_xxx_0_0_1 = filter.fir_filter_ccc(decimation, firdes.low_pass(1.0, samp_rate, (samp_rate/decimation)/2, 1000))
        self.fir_filter_xxx_0_0_1.declare_sample_delay(0)
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_ccc(decimation, firdes.low_pass(1.0, samp_rate, (samp_rate/decimation)/2, 1000))
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccc(decimation, firdes.low_pass(1.0, samp_rate, (samp_rate/decimation)/2, 1000))
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(decimation, firdes.low_pass(1.0, samp_rate, (samp_rate/decimation)/2, 1000))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.epy_block_0 = epy_block_0.blk(cpi_size=cpi_size//decimation)
        self._delay_time_s_0_range = qtgui.Range(0, 5, 0.5, 2, 200)
        self._delay_time_s_0_win = qtgui.RangeWidget(self._delay_time_s_0_range, self.set_delay_time_s_0, "'delay_time_s_0'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_time_s_0_win)
        self.cospas_sarsat_doa_0 = cospas_sarsat_doa(
            samp_rate=samp_rate,
            theta_deg=theta_deg,
        )
        self.channels_channel_model_0_0_0_1 = channels.channel_model(
            noise_voltage=Nv,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=False)
        self.channels_channel_model_0_0_0_0 = channels.channel_model(
            noise_voltage=Nv,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=False)
        self.channels_channel_model_0_0_0 = channels.channel_model(
            noise_voltage=Nv,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=False)
        self.channels_channel_model_0_0 = channels.channel_model(
            noise_voltage=Nv,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=False)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=Nv,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_to_stream_0_2_0 = blocks.vector_to_stream(gr.sizeof_float*1, 360)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_0_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_multiply_xx_0_3 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self._alpha_iir_0_range = qtgui.Range(0, 1, 0.01, 0.01, 200)
        self._alpha_iir_0_win = qtgui.RangeWidget(self._alpha_iir_0_range, self.set_alpha_iir_0, "'alpha_iir_0'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._alpha_iir_0_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_2, 0), (self.blocks_stream_to_vector_0_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_3, 0), (self.blocks_stream_to_vector_0_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.krakensdr_doa_music_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.krakensdr_doa_music_0, 1))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.krakensdr_doa_music_0, 2))
        self.connect((self.blocks_stream_to_vector_0_0_0_0, 0), (self.epy_block_0, 1))
        self.connect((self.blocks_stream_to_vector_0_0_1, 0), (self.krakensdr_doa_music_0, 3))
        self.connect((self.blocks_stream_to_vector_0_0_2, 0), (self.krakensdr_doa_music_0, 4))
        self.connect((self.blocks_throttle2_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0_2_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.channels_channel_model_0_0_0, 0), (self.fir_filter_xxx_0_0_1, 0))
        self.connect((self.channels_channel_model_0_0_0_0, 0), (self.fir_filter_xxx_0_0_2, 0))
        self.connect((self.channels_channel_model_0_0_0_1, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.cospas_sarsat_doa_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.cospas_sarsat_doa_0, 1), (self.channels_channel_model_0_0, 0))
        self.connect((self.cospas_sarsat_doa_0, 2), (self.channels_channel_model_0_0_0, 0))
        self.connect((self.cospas_sarsat_doa_0, 4), (self.channels_channel_model_0_0_0_0, 0))
        self.connect((self.cospas_sarsat_doa_0, 3), (self.channels_channel_model_0_0_0_1, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_vector_to_stream_0_2_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.squelcher_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.fir_filter_xxx_0_0_1, 0), (self.blocks_multiply_xx_0_2, 1))
        self.connect((self.fir_filter_xxx_0_0_2, 0), (self.blocks_multiply_xx_0_3, 1))
        self.connect((self.krakensdr_doa_music_0, 0), (self.epy_block_0, 0))
        self.connect((self.squelcher_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.squelcher_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.squelcher_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.squelcher_0, 0), (self.blocks_multiply_xx_0_2, 0))
        self.connect((self.squelcher_0, 0), (self.blocks_multiply_xx_0_3, 0))
        self.connect((self.squelcher_0, 0), (self.blocks_stream_to_vector_0_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "kraken_music_doa")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_theta_deg(self):
        return self.theta_deg

    def set_theta_deg(self, theta_deg):
        self.theta_deg = theta_deg
        self.cospas_sarsat_doa_0.set_theta_deg(self.theta_deg)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.cospas_sarsat_doa_0.set_samp_rate(self.samp_rate)
        self.fir_filter_xxx_0.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0_0.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0_1.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0_2.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, (self.samp_rate//self.decimation))
        self.squelcher_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_delay_time_s_0(self):
        return self.delay_time_s_0

    def set_delay_time_s_0(self, delay_time_s_0):
        self.delay_time_s_0 = delay_time_s_0

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.fir_filter_xxx_0.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0_0.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0_1.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.fir_filter_xxx_0_0_2.set_taps(firdes.low_pass(1.0, self.samp_rate, (self.samp_rate/self.decimation)/2, 1000))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, (self.samp_rate//self.decimation))
        self.squelcher_0.set_decimation(self.decimation)

    def get_cpi_size(self):
        return self.cpi_size

    def set_cpi_size(self, cpi_size):
        self.cpi_size = cpi_size

    def get_alpha_iir_0(self):
        return self.alpha_iir_0

    def set_alpha_iir_0(self, alpha_iir_0):
        self.alpha_iir_0 = alpha_iir_0

    def get_Nv(self):
        return self.Nv

    def set_Nv(self, Nv):
        self.Nv = Nv
        self.channels_channel_model_0.set_noise_voltage(self.Nv)
        self.channels_channel_model_0_0.set_noise_voltage(self.Nv)
        self.channels_channel_model_0_0_0.set_noise_voltage(self.Nv)
        self.channels_channel_model_0_0_0_0.set_noise_voltage(self.Nv)
        self.channels_channel_model_0_0_0_1.set_noise_voltage(self.Nv)




def main(top_block_cls=kraken_music_doa, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
