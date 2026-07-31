#!/usr/bin/env python
# coding: utf-8

# # Enriching Dimensionality Reduction with Distortion Cues
# ---
# 
# This notebook reproduces the main analysis presented in the paper *Enriching Dimensionality Reduction with Distortion Cues*. The workflow computes a two-dimensional projection, constructs a Delaunay triangulation, estimates projection distortions through high-dimensional edge interpolation, and generates the data for visualizations used throughout the paper.

# ## 1. Import Dependencies
# 
# Import the required libraries together with the implementation of the proposed distortion cue framework.


import os
import numpy as np
from distortion_cues import ProjectionAnalysisVisualizer, visualizer, utility
from datasets.datasets import *

from distortion_cues import config as cfg


# ## 2. Dataset Configuration
# 
# Select the dataset and configure the parameters required for the projection analysis.
# 
# The framework supports both synthetic datasets, used for controlled experiments, and real-world datasets for practical evaluation.


# dataset = 'cube_same_size_same_dist' # "cube_diff_size_diff_dist", "cube_diff_size_same_dist", "har", "aedessex", "mnsit"

dataset = 'har'    # Choose dataset from above list that you need to analyse. Also, you can include your own dataset too.
method = 'tsne'   #tsne, Umap


np.random.seed(cfg.GLOBAL_SEED)

# Synthetic dataset 
num_dim = cfg.NUM_DIMENSION
n_pts_per_gauss = cfg.POINTS_PER_CUBE

runtime_repetition = cfg.RUNTIME_REPETITION

colors = cfg.CUSTOM_COLORS
figsize = cfg.FIGSIZE
data_point_size= cfg.SCATTER_POINT_SIZE
linewidths = cfg.LINE_WIDTH
dpi = cfg.DPI
bscatter_plot = cfg.SCATTER_PLOT
save_format = cfg.SAVE_FORMAT

cfg_dt = cfg.get_config(dataset, method)
perplexity = cfg_dt["perplexity"]
class_names = cfg_dt["class_names"]
colors = cfg_dt["colors"]
fontsize = cfg_dt["fontsize"]
border_thickness = cfg_dt["border_thickness"]
legend_dt_point_size = cfg_dt["legend_dt_point_size"]
legend_font_size = cfg_dt["legend_font_size"]

data_point_size = cfg_dt["data_point_size"]
linewidths = cfg_dt["linewidths"]
colormap = colors

cfg_dt_umap = cfg.get_config(dataset, "umap")
perplexity_umap = cfg_dt_umap["perplexity"]

data_point_size_umap = cfg_dt_umap["data_point_size"]
linewidths_umap = cfg_dt_umap["linewidths"]


# ## 3. Output Configuration
# 
# Configure the directory used to store the generated embeddings, intermediate results, distortion cues, and figures.


save_output = True



if save_output:
    output_folder = f"results"
    os.makedirs(output_folder, exist_ok=True)
    output_plot_folder = f"{output_folder}/Figure_5"
    os.makedirs(output_plot_folder, exist_ok=True)
else:
    output_folder = None


# ## 4. Load the Dataset
# 
# Load the selected high-dimensional dataset together with the associated labels required for visualization and quantitative evaluation.


# For synthetic data only
cube_sizes, cube_centers = utility.cubic_centers_sizes(dataset=dataset)


print("Loading the dataset ...")
D,c, dim, output_size, n_gauss = selected_dataset_dt(dataset, num_dim, n_pts_per_gauss, cube_sizes=cube_sizes, cube_centers=cube_centers, cluster_spacing = 1.0, spread_factor = 0.01)
class_label = c.astype(int)

class_label = class_label - class_label.min()
np.unique(class_label)


# np.save(f"{output_folder}/D_{dataset}.npy", D)
# np.save(f"{output_folder}/class_label_{dataset}.npy", class_label)


# ## 5. Initialize the Projection Analysis Framework
# 
# Initialize the proposed framework using the high-dimensional data and the selected dimensionality reduction technique.

# Lets initialize the framework using original data and employing *TSNE* as a projection method. However, you can use other projections also.


print("Initializing the projection analysis framework using tSNE...")
proj_viz = ProjectionAnalysisVisualizer(data = D, class_label= class_label, projection_method= method, perplexity=perplexity, output_path=output_folder)  # Supervised

print("Initializing the projection analysis framework using UMAP...")
proj_viz_umap = ProjectionAnalysisVisualizer(data = D, class_label= class_label, projection_method= "umap", perplexity=perplexity_umap, output_path=output_folder)  # Supervised

# ## 6. Compute the Low-Dimensional Projection
# 
# Generate the two-dimensional embedding that serves as the basis for the subsequent distortion analysis.

print("Visualizing the low-dimensional projection tsne...")
low_dm_emb = proj_viz.projection_emb_low_dim()
visualizer.plot_projection_custom_color(embedding=low_dm_emb, class_label = class_label, filename= f"{dataset}_true_label_{method}", color_list = colormap, figsize= figsize, data_point_size= data_point_size, linewidths=linewidths, legend_dt_point_size = legend_dt_point_size, legend_font_size = legend_font_size, class_names=class_names, output_path=output_plot_folder, dpi=dpi, save_format=save_format) 

print("Visualizing the low-dimensional projection UMAP...")
low_dm_emb_umap = proj_viz_umap.projection_emb_low_dim()
visualizer.plot_projection_custom_color(embedding=low_dm_emb_umap, class_label = class_label, filename= f"{dataset}_true_label_umap", color_list = colormap, figsize= figsize, data_point_size= data_point_size_umap, linewidths=linewidths_umap, legend_dt_point_size = legend_dt_point_size, legend_font_size = legend_font_size, class_names=class_names, output_path=output_plot_folder, dpi=dpi, save_format=save_format) 


# breakpoint()
# np.save(f"{output_folder}/low_dm_emb_{dataset}.npy", low_dm_emb)


# ## 7. High-Dimensional Distance Analysis
# 
# Compute inter- and intra-cluster distance statistics in the original high-dimensional space. These measurements provide a quantitative reference for evaluating relationships preserved in the low-dimensional projection.


print("Computing pairwise distance matrix in high-dimensional space...")
(distance_matrix_hd_true, mean_cluster_distance__hd_true), mean_time_pair_dist, std_time_pair_dist = utility.run_and_measure(
                                                    proj_viz.inter_intra_cluster_pairwise_distance,
                                                    D,
                                                    class_label,
                                                    repeats=runtime_repetition
                                                )

print(f"Pairwise Distance Matrix runtime: {mean_time_pair_dist:.4f} ± {std_time_pair_dist:.4f} sec")
visualizer.plot_pairwise_cluster_distance_v2_custom_color(distance_matrix=distance_matrix_hd_true, mean_cluster_distance =mean_cluster_distance__hd_true, label=class_label, filename=f"{dataset}_true_label_{method}", border_thickness= border_thickness, fontsize=fontsize, color_list=colormap, figsize= figsize, output_path=output_plot_folder, save_format=save_format)



# np.save(f"{output_folder}/distance_matrix_hd_true_{dataset}.npy", distance_matrix_hd_true)
# np.save(f"{output_folder}/mean_cluster_distance__hd_true_{dataset}.npy", mean_cluster_distance__hd_true)



# ## 8. Construct the Delaunay Triangulation
# 
# Construct a Delaunay triangulation over the projected embedding. The triangulation defines the neighborhood structure used for high-dimensional edge interpolation.


# tri_delaunay = proj_viz.delaunay_triangulation(embedding= low_dm_emb)


# Use the following code if you do not want to measure runtime otherwise uncomment above and use directly.

tri_delaunay, mean_time, std_time = utility.run_and_measure(
    proj_viz.delaunay_triangulation,
    embedding=low_dm_emb,
    repeats=runtime_repetition
)

print(f"Delaunay runtime: {mean_time:.6f} ± {std_time:.6f} sec")



# np.savez(f"{output_folder}/tri_delaunay_{dataset}.npz", simplices=tri_delaunay.simplices)



edges_delaunay,_ = utility.extract_delaunay_edges_2d(tri_delaunay)
# np.save(
#         f"{output_folder}/edges_delaunay_orig_{dataset}.npy",
#         edges_delaunay
#     )


# ### High-Dimensional Edge Interpolation
# 
# For each Delaunay edge, the corresponding relationship in the original high-dimensional space is estimated through interpolation. These estimates provide the basis for computing the distortion cues introduced in the paper.

# ## 9. Compute Distortion Cues
# 
# Estimate projection distortions by interpolating distances along Delaunay edges and comparing them with the corresponding relationships in the original high-dimensional space.
# 
# The resulting distortion values are used to enrich the projection with geometric cues that facilitate the interpretation of projection quality.

print("Computing distortion cues through high-dimensional edge interpolation (tSNE)...")
intensity_interp_cordinates, max_interp, min_interp  = proj_viz.delanay_hd_edge_lenghts_inter()
visualizer.plot_analysis_custom_color(
            low_dm_emb, 
            class_label,
             intensity_interp_cordinates, 

             show_all_edges=False,
             k_edges_per_cluster=3,
             edge_selection_mode="shortest",  #   longest, shortest
             
            bscatter_plot= bscatter_plot, 
            color_list = colormap,
            figsize=figsize, data_point_size= data_point_size, linewidths= linewidths, filename= f"delaunay_hd_edge_lengths_{dataset}_true_label_{method}",
            output_path=output_plot_folder, dpi=dpi, save_format=save_format

        )

print("Computing distortion cues through high-dimensional edge interpolation (UMAP)...")
intensity_interp_cordinates_umap, max_interp_umap, min_interp_umap  = proj_viz_umap.delanay_hd_edge_lenghts_inter()
visualizer.plot_analysis_custom_color(
            low_dm_emb_umap, 
            class_label,
             intensity_interp_cordinates_umap, 

             show_all_edges=False,
             k_edges_per_cluster=3,
             edge_selection_mode="shortest",  #   longest, shortest
             
            bscatter_plot= bscatter_plot, 
            color_list = colormap,
            figsize=figsize, data_point_size= data_point_size_umap, linewidths= linewidths_umap, filename= f"delaunay_hd_edge_lengths_{dataset}_true_label_umap",
             output_path=output_plot_folder, dpi=dpi, save_format=save_format

        )

