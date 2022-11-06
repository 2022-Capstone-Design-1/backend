#!/bin/bash

WAV_DIR=$1
DATA_DIR=${2:-${DATA_DIR:-"/pybackend/hyper/tasks/SpeechRecognition/klecspeech/data"}}
MODEL_CONFIG=${3:-${MODEL_CONFIG:-"/pybackend/hyper/tasks/SpeechRecognition/klecspeech/configs/jasper10x5dr_sp_offline_specaugment.yaml"}}
RESULT_DIR=${4:-${RESULT_DIR:-"pybackend/hyper/tasks/SpeechRecognition/klecspeech/result/inference"}}
CHECKPOINT=${5:-${CHECKPOINT:-"pybackend/hyper/tasks/SpeechRecognition/klecspeech/result/results_final_scratch/Jasper_epoch100_checkpoint.pt"}}
CREATE_LOGFILE=${6:-${CREATE_LOGFILE:-"true"}}
CUDNN_BENCHMARK=${7:-${CUDNN_BENCHMARK:-"true"}}
AMP=${8:-${AMP:-"false"}}
NUM_STEPS=${9:-${NUM_STEPS:-"-1"}}
SEED=${10:-${SEED:-42}}
BATCH_SIZE=${11:-${BATCH_SIZE:-1}}
CPU=${12:-${CPU:-"false"}}
EMA=${13:-${EMA:-"false"}}
TASK_PATH=${14:-${TASK_PATH:-"tasks.SpeechRecognition.klecspeech.local.manifest"}}
VOCAB=${15:-${VOCAB:-"vocab"}}

mkdir -p "$RESULT_DIR"

CMD="python pybackend/hyper/inference.py"
CMD+=" --task_path=$TASK_PATH"
CMD+=" --batch_size $BATCH_SIZE"
CMD+=" --dataset_dir $PWD$DATA_DIR"

# CMD+=" --wav $PWD$DATA_DIR/000000.wav"
# CMD+=" --wav ../../../../test.wav"
CMD+=" --wav $WAV_DIR"

CMD+=" --model_cfg $PWD$MODEL_CONFIG"
CMD+=" --vocab=$VOCAB"
CMD+=" --seed $SEED "
[ "$NUM_STEPS" -gt 0 ] && \
CMD+=" --steps $NUM_STEPS"
[ "$CUDNN_BENCHMARK" = "true" ] && \
CMD+=" --cudnn"
[ "$AMP" == "true" ] && \
CMD+=" --amp"
[ "$CPU" == "true" ] && \
CMD+=" --cpu"
[ "$EMA" == "true" ] && \
CMD+=" --ema"
[ -n "$CHECKPOINT" ] && \
CMD+=" --ckpt=${CHECKPOINT}"

if [ "$CREATE_LOGFILE" = "true" ] ; then
   export GBS=$(expr $BATCH_SIZE)
   printf -v TAG "jasper_inference_benchmark_amp-%s_gbs%d" "$AMP" $GBS
   DATESTAMP=`date +'%y%m%d%H%M%S'`
   LOGFILE="${RESULT_DIR}/${TAG}.${DATESTAMP}.log"
   printf "Logs written to %s\n" "$LOGFILE"
fi

set -x
if [ -z "$LOGFILE" ] ; then
   $CMD
else
   (
     $CMD
   ) |& tee "$LOGFILE"
fi
set +x
[ -n "$PREDICTION_FILE" ] && echo "PREDICTION_FILE: ${PREDICTION_FILE}"
[ -n "$LOGITS_FILE" ] && echo "LOGITS_FILE: ${LOGITS_FILE}"
