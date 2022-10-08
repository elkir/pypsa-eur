# SPDX-FileCopyrightText: : 2017-2020 The PyPSA-Eur Authors
#
# SPDX-License-Identifier: MIT

"""
Export input and output timeseries dataframes for the solve_network procedure

.. code:: yaml

    extract_ml:
        keep_na_columns:


Inputs
------

- ``results/networks/elec_s{simpl}_{clusters}_ec_l{ll}_{opts}.nc``: Solved PyPSA network including optimisation results

Outputs
-------

- ``results/ml/{year}/{chunk}/elec_s{simpl}_{clusters}_ec_l{ll}_{opts}_inputs.P``: Dataframe consisting of all the timeseries inputs to the solve_network rule
- ``results/ml/{year}/{chunk}/elec_s{simpl}_{clusters}_ec_l{ll}_{opts}_outputs.P``: Dataframe consisting of all the timeseries outputs to the solve_network rule
- ``results/ml/{year}/{chunk}/elec_s{simpl}_{clusters}_ec_l{ll}_{opts}_outputs_p.P``: Dataframe consisting of only the timeseries for power at each node of the network


Description
-----------

"""

import logging
from _helpers import configure_logging

import pandas as pd
import numpy as np
import pypsa


logger = logging.getLogger(__name__)

def n_extract_values(n, index):
    '''
    Extracts timeseries specified in index (list of (atribute,column,Nvars) pairs)
    Adds a prefix to column names as "attr:col: <name>"
    ''' 
    return pd.concat([getattr(n,c)[d].add_prefix(f"{c[:-2]}:{d}: ") for c,d,_ in index],axis=1)



def get_outputs_df(n,keep_na_columns=False):
    # ### Outputs
    iOutputs = [
    ('buses_t', 'p'),
    ('buses_t', 'v_ang'),
    ('buses_t', 'marginal_price'),
    ('generators_t', 'p'),
    ('storage_units_t', 'p'),
    ('storage_units_t', 'state_of_charge'),
    ('storage_units_t', 'spill'),
    ('lines_t', 'p0'),
    ('lines_t', 'p1'),
    ('lines_t', 'mu_lower'),
    ('lines_t', 'mu_upper'),
    ('links_t', 'p0'),
    ('links_t', 'p1'),
    ('links_t', 'mu_lower'),
    ('links_t', 'mu_upper'),
    ]
    # output index
    index_outputs=[(c,d,getattr(n,c)[d].shape[1]) for c,d in iOutputs]
    df_outputs = n_extract_values(n,index_outputs)
    if not keep_na_columns:
        df_outputs= df_outputs.dropna(how='any',axis=1)
    return df_outputs

# ### Inputs
def get_inputs_df(n):
    iInputsT = [
    ('loads_t', 'p_set'),
    ('generators_t', 'p_max_pu'),
    ('storage_units_t', 'inflow')]
    index_inputs=[(c,d,getattr(n,c)[d].shape[1]) for c,d in iInputsT]

    df_inputs = n_extract_values(n,index_inputs)
    return df_inputs
    







if __name__ == "__main__":
    if 'snakemake' not in globals():
        from _helpers import mock_snakemake
        snakemake = mock_snakemake('extract_ml_data', network='elec', simpl='',
                                  clusters='5', ll='copt', opts='Co2L-BAU-CCL-24H',
                                  year="2013",chunk="6M")
    configure_logging(snakemake)
  
    n = pypsa.Network(snakemake.input[0])
    
    df_inputs = get_inputs_df(n)
    df_outputs = get_outputs_df(n,keep_na_columns=snakemake.config["export_ml"]["keep_na_columns"])
    
    
    df_inputs.to_pickle(snakemake.output.inputs)
    df_outputs.to_pickle(snakemake.output.outputs)
    df_outputs.loc[:,df_outputs.columns.str.startswith("buses:p:")
            ].to_pickle(snakemake.output.outputs_p)
    
    
   
