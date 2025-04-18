DATA_ROOT=/home/xiezy/projects/VLN-Tutorial/MapGPT/datasets
OUTDIR=${DATA_ROOT}/exprs_map/4v/test/

flag="--root_dir ${DATA_ROOT}
      --img_root /home/xiezy/projects/VLN-Tutorial/MapGPT/datasets/RGB_Observations
      --split MapGPT_72_scenes_processed
      --end 10  # the number of cases to be tested
      --output_dir ${OUTDIR}
      --max_action_len 15
      --save_pred
      --stop_after 3
      --llm gpt-4-vision-preview
      --response_format str
      --max_tokens 1000
      "

python MapGPT/vln/main_gpt_debug.py $flag
