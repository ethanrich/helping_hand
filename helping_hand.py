# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:33:02 2020

@author: Ethan

This application takes EMG channels as inputs (eg two channels for two extensor muscles, two for flexors) and gives
STG stimulation (mA) as an output. The intensity (mA) of the stimulation is dependent on the level of activity in the
"healthy side". Contracting muscles harder will result in an increase in mA, which is capped at "max_amp".
"""

import time
import liesl
import reiz
from reiz.visual import Mural
from matplotlib import pyplot as plt
import numpy as np
from stg.api import STG4000

def check_channels(buffer):
    fig, axes = plt.subplots(2, 1, sharex=False)
    fig.canvas.manager.window.resize(1280, 1024)
    fig.tight_layout()

    # EMG channel inspection
    axes[0].cla()
    axes[0].plot(buffer.get_data()[:,opener_chans[0]])
    #            axes[1].cla()
    #            axes[1].plot(buffer.get_data()[:,opener_chans[1]])
    axes[0].set_title('Opener 1 EMG')
    #            axes[1].set_title('Opener 2 EMG')

    axes[1].cla()
    axes[1].plot(buffer.get_data()[:,closer_chans[0]])
    #            axes[3].cla()
    #            axes[3].plot(buffer.get_data()[:,closer_chans[1]])
    axes[1].set_title('Closer EMG')
    #            axes[3].set_title('Closer 2 EMG')

    fig.gca()
    plt.pause(0.01)


def calibrate_fes(canvas, stg):
        while True:
            try:
                omax_amp = int(input("Openers max amp: "))
                cmax_amp = int(input("Closers max amp: "))
                if 5 < omax_amp < 20:
                    if 5 < cmax_amp < 20:
                        break
            except ValueError:
                print("Bitte gib eine gültige Zahl ein")
                
        o_amps = [omax_amp, omax_amp*-1, 0]
        c_amps = [cmax_amp, cmax_amp*-1, 0]
        fes_ON = [0.2, 0.2, 50.1 - 0.2 * 2]
                
        buffer_in_s = 0.16  # how large is the buffer in the DLL?
        capacity_in_s = 2 * buffer_in_s  # how large is the buffer on the STG?
        
        # Start window and countdown
        canvas.start_run = False
        start_protocol = reiz.Cue(canvas, visualstim=Mural(text="Press F5 to start O test: " + str(o_amps)))
        while not canvas.start_run:
            start_protocol.show(duration=0.1)
        
        t0 = time.time()
        t1 = time.time()
        stg.set_signal(channel_index=0, amplitudes_in_mA=[0, 0, 0], durations_in_ms=fes_ON)
        stg.start_streaming(capacity_in_s=capacity_in_s, buffer_in_s=buffer_in_s)
    
        while t1-t0 < 5:
            stg.set_signal(channel_index=0, amplitudes_in_mA=o_amps, durations_in_ms=fes_ON)
            t1 = time.time()
    
        stg.stop_streaming()
        
        reiz.Cue(canvas, visualstim=Mural(text="Starting C test with: " + str(c_amps))).show(5)
        
        t0 = time.time()
        t1 = time.time()
        stg.set_signal(channel_index=1, amplitudes_in_mA=[0, 0, 0], durations_in_ms=fes_ON)
        stg.start_streaming(capacity_in_s=capacity_in_s, buffer_in_s=buffer_in_s)

        while t1-t0 < 5:
            stg.set_signal(channel_index=1, amplitudes_in_mA=c_amps, durations_in_ms=fes_ON)
            t1 = time.time()
        stg.stop_streaming()


def countdown(canvas, sec):
    for i in range(0, sec):
        cue = reiz.Cue(canvas, visualstim=Mural(text=str(sec - i)))
        cue.show(duration=1)

def calibrate_hh(buffer, canvas, o_stim_range, c_stim_range, opener_chans, closer_chans):
    
    reiz.Cue(canvas, visualstim=[
        reiz.visual.Mural(
            "EMG Calibration Procedure",
            position=[0, 0.25],
            font="arial",
            fontsize=1,),
        reiz.visual.Mural(
            "Follow the instructions", position=[0, -0.25], font="arial", fontsize=1)]).show(duration=3)
    reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Prepare to begin opening")]).show(duration=3)
    countdown(canvas, 3)

    openers_active = []
    closers_rest   = []
    for k in range(3):
        # show cue
        reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Open your hand")]).show(duration=3)
        # get data of last 1.5 seconds
        openers_data = buffer.get_data()[:,opener_chans]
        closers_data = buffer.get_data()[:,closer_chans]
        # for each channel, get the rms value
        openers_active = [openers_data[:,chan] - np.mean(openers_data[:,chan]) for chan in range(np.size(openers_data,1))]
        openers_active = [np.sqrt(np.mean((openers_active[chan] * 1000) ** 2))                 for chan in range(np.size(openers_data,1))]
        closers_rest   = [closers_data[:,chan] - np.mean(closers_data[:,chan]) for chan in range(np.size(closers_data,1))]
        closers_rest   = [np.sqrt(np.mean((closers_rest[chan] * 1000) ** 2))                   for chan in range(np.size(closers_data,1))]

        if k < 2:
            reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Prepare for next run")]).show(duration=2)
            countdown(canvas, 3)
        else:
            reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Done")]).show()

    reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Prepare to begin closing")]).show(duration=3)
    countdown(canvas, 3)
    openers_rest   = []
    closers_active = []
    for k in range(3):
        # show cue
        reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Close your hand")]).show(duration=3)
        # get data of last 1.5 seconds
        openers_data = abs(buffer.get_data()[:,opener_chans])
        closers_data = abs(buffer.get_data()[:,closer_chans])
        # for each channel, get the rms value
        openers_rest   = [openers_data[:,chan] - np.mean(openers_data[:,chan]) for chan in range(np.size(openers_data,1))]
        openers_rest   = [np.sqrt(np.mean((openers_rest[chan] * 1000) ** 2))   for chan in range(np.size(openers_data,1))]
        closers_active = [closers_data[:,chan] - np.mean(closers_data[:,chan]) for chan in range(np.size(closers_data,1))]
        closers_active = [np.sqrt(np.mean((closers_active[chan] * 1000) ** 2)) for chan in range(np.size(closers_data,1))]

        if k < 2:
            reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Prepare for next run")]).show(duration=2)
            countdown(canvas, 3)
        else:
            reiz.Cue(canvas, visualstim=[reiz.visual.Mural("Done")]).show()

    canvas.close()

    openers_snr = []
    closers_snr = []
    openers_snr = [(openers_active[chan] / openers_rest[chan]) ** 2 for chan in range(np.size(openers_data,1))]
    closers_snr = [(closers_active[chan] / closers_rest[chan]) ** 2 for chan in range(np.size(closers_data,1))]
    # take mean of channels for openers and closers
    openers     = np.mean(openers_snr)
    closers     = np.mean(closers_snr)
    # create a 50-element range of snr values to map to stim amplitudes
    o_snr_list  = np.arange(openers*0.01, openers-(openers*0.5), openers/101)
    c_snr_list  = np.arange(closers*0.01, closers-(closers*0.5), closers/101)

    return o_snr_list, c_snr_list, openers_rest, closers_rest



def helping_hand(stg, fes_ON, buffer, canvas, opener_chans, closer_chans, o_snr_list, c_snr_list, openers_rest, closers_rest):

    while True:
        openers_data = abs(buffer.get_data()[:,opener_chans])
        closers_data = abs(buffer.get_data()[:,closer_chans])

        o_temp = []
        o_rms  = []
        c_temp = []
        c_rms  = []
        o_current = []
        c_current = []

        # detrend, get current rms, get snr
        o_temp     = [openers_data[:,chan] - np.mean(openers_data[:,chan]) for chan in range(np.size(openers_data,1))]
        o_rms      = [np.sqrt(np.mean((o_temp[chan] * 1000) ** 2))         for chan in range(np.size(openers_data,1))]
        o_current  = [(o_rms[chan] / openers_rest[chan]) ** 2              for chan in range(np.size(openers_data,1))]
        o_current  = np.mean(o_current)

        c_temp     = [closers_data[:,chan] - np.mean(closers_data[:,chan]) for chan in range(np.size(closers_data,1))]
        c_rms      = [np.sqrt(np.mean((c_temp[chan] * 1000) ** 2))         for chan in range(np.size(closers_data,1))]
        c_current  = [(c_rms[chan] / closers_rest[chan]) ** 2              for chan in range(np.size(closers_data,1))]
        c_current  = np.mean(c_current)

        # convert to index of snr lists
        o_stim_idx = min(range(len(o_snr_list)), key=lambda i: abs(o_snr_list[i]-o_current))
        c_stim_idx = min(range(len(c_snr_list)), key=lambda i: abs(c_snr_list[i]-c_current))

        # ensure that only one muscle is stimulated at a time
        if o_stim_idx > c_stim_idx:
            c_stim_idx = 0
        else:
            o_stim_idx = 0

        # using the mapping made earlier, we use the indices to map to stim amplitude
        o_amps = [o_stim_range[o_stim_idx], o_stim_range[o_stim_idx]*-1, 0]
        c_amps = [c_stim_range[c_stim_idx], c_stim_range[c_stim_idx]*-1, 0]

        stg.set_signal(channel_index=0,
                                amplitudes_in_mA= o_amps,
                                durations_in_ms=fes_ON)
        stg.set_signal(channel_index=1,
                                amplitudes_in_mA= c_amps,
                                durations_in_ms=fes_ON)

        if c_amps[0] == 0:
            print('Openers: ' + str(o_amps[0]))
        elif o_amps[0] == 0:
            print('Closers: ' + str(c_amps[0]))
            
#%%

if __name__ == "__main__":
    
    sinfo  = liesl.get_streaminfos_matching(type="EEG")[0]
    buffer = liesl.RingBuffer(sinfo, duration_in_ms=500)
    buffer.start()
    buffer.await_running()
    time.sleep(0.01)
    canvas = reiz.Canvas()
    canvas.open()
    #---------------------------
    opener_chans = [63+7]
    closer_chans = [63+8, 63+9]
    #---------------------------
    
    pulse_width   = 0.2  # here the pulse width size can be changed
    fes_ON        = [pulse_width, pulse_width, 50.1 - pulse_width * 2]
    buffer_in_s   = 0.16  # how large is the buffer in the DLL?
    capacity_in_s = 2 * buffer_in_s  # how large is the buffer on the STG?
    stg           = STG4000()
    
    # check if the proper channels are connected
    check_channels(buffer)
    # find the stimulation threshold for the user
    calibrate_fes(canvas, stg)
    # stim range going from 0 to max_amp in steps of % of max amp
    omax_amp     = 10.2
    cmax_amp     = 10.2
    multiplier   = 1.0 # add a decimal number to this value to increase max amp
    o_stim_range = np.arange(1, omax_amp * multiplier, omax_amp * multiplier/40)
    c_stim_range = np.arange(1, cmax_amp * multiplier, cmax_amp * multiplier/40)
    
    # calibrate the resting state
    o_snr_list, c_snr_list, openers_rest, closers_rest = calibrate_hh(buffer, canvas, o_stim_range,
                                                                      c_stim_range, opener_chans, closer_chans)
    # initialize stg streaming
    stg.set_signal(channel_index=0,amplitudes_in_mA= [0,0,0],durations_in_ms=fes_ON)
    stg.set_signal(channel_index=1,amplitudes_in_mA= [0,0,0],durations_in_ms=fes_ON)
    stg.start_streaming(capacity_in_s=capacity_in_s, buffer_in_s=buffer_in_s)
    
    # start helping hand 
    while True:
        helping_hand(stg, fes_ON, buffer, canvas, opener_chans, closer_chans,
                     o_snr_list, c_snr_list, openers_rest, closers_rest)

    stg.stop_streaming()






