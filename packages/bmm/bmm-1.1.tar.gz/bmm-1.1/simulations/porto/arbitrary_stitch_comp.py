import os
import json

import numpy as np
import osmnx as ox
import pandas as pd

import bmm

seed = 0
np.random.seed(seed)

timestamps = 15
ffbsi_n_samps = int(1e2)
max_rejections = 30
initial_truncation = None
max_speed = 35
proposal_dict = {'proposal': 'optimal',
                 'num_inter_cut_off': 10,
                 'resample_fails': False,
                 'd_max_fail_multiplier': 2.}

porto_sim_dir = os.getcwd()
graph_path = porto_sim_dir + '/portotaxi_graph_portugal-140101.osm._simple.graphml'
graph = ox.load_graphml(graph_path)

test_route_data_path = porto_sim_dir + '/test_route.csv'

# Load long-lat polylines
polyline_ll = np.array(json.loads(pd.read_csv(test_route_data_path)['POLYLINE'][0]))
# Convert to utm
polyline = bmm.long_lat_to_utm(polyline_ll, graph)

save_dir = porto_sim_dir

# Create save_dir if not found
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Setup map-matching model
mm_model = bmm.ExponentialMapMatchingModel()
mm_model.max_speed = max_speed

# Run FFBSi
ffbsi_route = bmm.offline_map_match(graph,
                                    polyline,
                                    ffbsi_n_samps,
                                    timestamps=timestamps,
                                    mm_model=mm_model,
                                    max_rejections=max_rejections,
                                    initial_d_truncate=initial_truncation,
                                    store_filter_particles=True,
                                    **proposal_dict)

# xlim = (532414.3280397488, 532602.8407174668)
# ylim = (4557148.458743169, 4557402.671739089)

xlim = (532424.3969578809, 532544.9005208821)
ylim = (4557289.839800358, 4557377.009260867)

arb_particle = [np.array([[0.00000000e+00, 4.74800221e+08, 4.74793814e+08, 0.00000000e+00, 3.15674384e-01,
                           5.32443286e+05, 4.55736072e+06, 0.00000000e+00]]),
                np.array([[0.00000000e+00, 4.74800221e+08, 4.74800358e+08, 0.00000000e+00,
                           3.49999862e-01, 5.32453899e+05, 4.55735725e+06, 0.00000000e+00],
                          [1.50000000e+01, 4.74800221e+08, 4.74800358e+08, 0.00000000e+00,
                           8.51428512e-01, 5.32453232e+05, 4.55733735e+06, 2.00000000e+01]]),
                np.array([[1.50000000e+01, 4.74793814e+08, 4.74800358e+08, 0.00000000e+00,
                           2.85530189e-01, 5.32439124e+05, 4.55732713e+06, 3.61953104e+01],
                          [0.00000000e+00, 4.74793814e+08, 4.74800358e+08, 0.00000000e+00,
                           1.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.30000000e+01],
                          [3.00000000e+01, 4.74800358e+08, 4.74797434e+08, 0.00000000e+00,
                           9.73597981e-01, 5.32522127e+05, 4.55730204e+06, 8.67517835e+01]]),
                np.array([[3.00000000e+01, 4.74797434e+08, 4.74794846e+08, 0.00000000e+00,
                           7.24127929e-01, 5.32527382e+05, 4.55730108e+06, 8.61087731e+01],
                          [0.00000000e+00, 4.74797434e+08, 4.74794846e+08, 0.00000000e+00,
                           1.00000000e+00, 0.00000000e+00, 0.00000000e+00, 7.00000000e+00],
                          [0.00000000e+00, 4.74794846e+08, 4.74802727e+08, 0.00000000e+00,
                           1.00000000e+00, 0.00000000e+00, 0.00000000e+00, 3.91031048e+01],
                          [4.50000000e+01, 4.74802727e+08, 3.49907807e+08, 0.00000000e+00,
                           5.10758925e-01, 5.32574224e+05, 4.55717472e+06, 1.39407136e+02]]),
                np.array([[4.50000000e+01, 4.74802727e+08, 3.49907807e+08, 0.00000000e+00,
                           4.70781693e-01, 5.32572990e+05, 4.55717745e+06, 1.34407136e+02],
                          [6.00000000e+01, 4.74802727e+08, 3.49907807e+08, 0.00000000e+00,
                           9.00151785e-01, 5.32618847e+05, 4.55710855e+06, 8.30000000e+01]])
                ]

stitched_particle = ffbsi_route.particles[0]
fig, ax = bmm.plot(graph, [stitched_particle], polyline, label_start_end=False)
ax.annotate('Start', arb_particle[0][0, 5:7] + 10, zorder=12)
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)
fig.savefig(save_dir + '/stitched_particle', dpi=300)

fig, ax = bmm.plot(graph, arb_particle, polyline, particles_alpha=1., label_start_end=False)
ax.annotate('Start', arb_particle[0][0, 5:7] + 10, zorder=12)
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)
fig.savefig(save_dir + '/arb_stitched_particle', dpi=300)
