import os

TESTS_HOME = os.path.abspath(os.path.dirname(__file__))

TESTDATA_PATH = os.path.join(TESTS_HOME, 'testdata')

TESTDATA = {
    'cordex_tasmax.nc': os.path.join(TESTDATA_PATH, 'CORDEX', 'EUR-44', 'mon', 'tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc'),
    }

