Run with:

source geant/bin/geant.sh
source root/bin/thisroot.sh

python2 deco_rand_muon_simulation.py

The files generated are charge deposited on pixels, run Single_plot.py to convert them into luminance on image
Note that background files extracted from real events should be put into appropriate folder or set to 0

The folder htcwildfire contains all parameters for the HTC wildfire model. In the file source_measurement_replace.conf
"MCTrack", "MCParticle" has been commented out, and they represent the MC true value of particles produced 
in this simulation (remove the '#' to make them work)
