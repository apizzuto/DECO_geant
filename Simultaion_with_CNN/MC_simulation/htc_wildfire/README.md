# DECO Simulation with particle beams

This directory is for simulating the detector described in the DECO measurement on the depletion thickness in cell phone camera image sensors.

A Monolithic pixel is used, with a depletion thickness of 26.3um and extra non-instrumented silicon is added behind the chip to aid in the production of worm like signatures in the detector.
No misalignment is added but the absolute position and orientation of the detector is specified.

The setup of the simulation chain includes Generic Digitization, instantiation of a particle beam, as well as detector geometry relative to the incident beam. There is a python script which can be used to submit batches of beams to cover large phase spaces with ease.
