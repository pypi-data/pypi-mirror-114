# -*- coding: utf-8 -*-

from .image_functions import (
    # simpler_crop,
    crop_np,
    crop_pil,
    crop,
    subtle_sharpie_enhance,
    harsh_sharpie_enhance,
    salting,
    simple_rotation_augmentation,
    blur_out_edges,
    reasonable_rotation_augmentation,
    show_major_lines_on_image,
    find_big_lines,
    separate_image_averager,
    augment_and_move,
    dimensions_to_df,
    dimensions_to_histo,
    proportions_ht_wt_to_histo,
    crop_them_all,
    find_very_hazy,
    find_by_sample_upper,
    find_sample_upper_greater_than_lower,
    find_outliers_by_total_mean,
    find_outliers_by_mean_to_df,
    create_matrix,
    find_tiny_image_differences,
    tesseract_specific,
    find_suspect_text,
    find_suspect_text_by_length,
    histogram_difference_for_inverts,
    histogram_difference_for_inverts_todf,
    find_duplicated_images,
    find_duplicated_images_todf,
    show_images_in_df,
    dataframe_up_my_pics,
    simple_spinning_template,
    make_contour_image,
    avg_image_maker,
    set_image_variability,
    avg_image_maker_by_label,
    zero_to_twofivefive_simplest_norming,
    rescale_range_from_histogram_low_end,
    make_histo_scaled_folder,

    Rotator,

)

# from .pipeline import (

#     DirectorySource,
#     PipelineError,
#     Step,

# )
