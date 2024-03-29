#!/bin/bash

DATA_DIR=${1:-${DATA_DIR:-"/home/201702085/hyper/tasks/SpeechRecognition/klecspeech/data/KlecSpeech"}}
# 하단 경로 수정
MODEL_CONFIG=${2:-${MODEL_CONFIG:-"/../configs/jasper10x5dr_sp_offline_specaugment.yaml"}}
RESULT_DIR=${3:-${RESULT_DIR:-"../result/results_final_scratch"}}
CHECKPOINT=${4:-${CHECKPOINT:-""}}
CREATE_LOGFILE=${5:-${CREATE_LOGFILE:-"true"}}
CUDNN_BENCHMARK=${6:-${CUDNN_BENCHMARK:-"true"}}
# 하단 GPU 개수 설정란
NUM_GPUS=${7:-${NUM_GPUS:-4}}
AMP=${8:-${AMP:-"false"}}
EPOCHS=${9:-${EPOCHS:-100}}
SEED=${10:-${SEED:-6}}
BATCH_SIZE=${11:-${BATCH_SIZE:-128}}
LEARNING_RATE=${12:-${LEARNING_RATE:-"0.08"}}
GRADIENT_ACCUMULATION_STEPS=${13:-${GRADIENT_ACCUMULATION_STEPS:-16}}
EMA=${EMA:-0.0}
SAVE_FREQUENCY=${SAVE_FREQUENCY:-5}
TASK_PATH=${TASK_PATH:-"tasks.SpeechRecognition.klecspeech.local.manifest"}
#VOCAB=${VOCAB:-"../checkpoints/vocab"}
# 하단 경로 수정
VOCAB=${VOCAB:-"/../data/vocab"}

mkdir -p "$RESULT_DIR"

#export CUDA_VISIBLE_DEVICES=0
export OMP_NUM_THREADS=8

CMD="python -m torch.distributed.launch --nproc_per_node=$NUM_GPUS --master_port=40281"
CMD+=" ../../../../train.py"
CMD+=" --task_path=$TASK_PATH"
CMD+=" --batch_size=$BATCH_SIZE"
CMD+=" --num_epochs=$EPOCHS"
CMD+=" --output_dir=$RESULT_DIR"
CMD+=" --model_cfg=$PWD$MODEL_CONFIG"
CMD+=" --lr=$LEARNING_RATE"
CMD+=" --ema=$EMA"
CMD+=" --seed=$SEED"
CMD+=" --optimizer=novograd"
CMD+=" --dataset_dir=$DATA_DIR"
CMD+=" --val_manifest=$DATA_DIR/valid-wav.json"
# CMD+=" --train_manifest=$DATA_DIR/D01-wav.json"
# CMD+=",$DATA_DIR/D02-wav.json"
# CMD+=",$DATA_DIR/D03-wav.json"
# CMD+=",$DATA_DIR/D04-wav.json"
# CMD+=",$DATA_DIR/D05-wav.json"
# CMD+=",$DATA_DIR/D06-wav.json"
# CMD+=",$DATA_DIR/D07-wav.json"
# CMD+=",$DATA_DIR/D08-wav.json"
# CMD+=",$DATA_DIR/D09-wav.json"
# CMD+=",$DATA_DIR/D10-wav.json"
# CMD+=",$DATA_DIR/D11-wav.json"
# CMD+=",$DATA_DIR/D12-wav.json"
# CMD+=",$DATA_DIR/D13-wav.json"
# CMD+=",$DATA_DIR/D14-wav.json"
# CMD+=",$DATA_DIR/D15-wav.json"
# CMD+=",$DATA_DIR/D16-wav.json"
# CMD+=",$DATA_DIR/D17-wav.json"
# CMD+=",$DATA_DIR/D18-wav.json"
# CMD+=",$DATA_DIR/D19-wav.json"
# CMD+=",$DATA_DIR/D99-wav.json"
CMD+=" --train_manifest=$DATA_DIR/D09-wav.json"
CMD+=",$DATA_DIR/D15-wav.json"

CMD+=" --weight_decay=1e-3"
CMD+=" --save_freq=$SAVE_FREQUENCY"
CMD+=" --eval_freq=100"
CMD+=" --train_freq=1"
CMD+=" --lr_decay"
CMD+=" --gradient_accumulation_steps=$GRADIENT_ACCUMULATION_STEPS"
CMD+=" --num_gpus=$NUM_GPUS"
CMD+=" --vocab=$PWD$VOCAB"

[ "$AMP" == "true" ] && \
CMD+=" --amp"
[ "$CUDNN_BENCHMARK" = "true" ] && \
CMD+=" --cudnn"
[ -n "$CHECKPOINT" ] && \
CMD+=" --ckpt=$PWD${CHECKPOINT}"

if [ "$CREATE_LOGFILE" = "true" ] ; then
   export GBS=$(expr $BATCH_SIZE \* $NUM_GPUS)
   printf -v TAG "jasper_train_benchmark_amp-%s_gbs%d" "$AMP" $GBS
   DATESTAMP=`date +'%y%m%d%H%M%S'`
   LOGFILE=$RESULT_DIR/$TAG.$DATESTAMP.log
   printf "Logs written to %s\n" "$LOGFILE"
fi

set -x
if [ -z "$LOGFILE" ] ; then
   $CMD
else
   (
     $CMD
   ) |& tee $LOGFILE
fi
set +x
