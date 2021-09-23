set LDMB_PATH=d:\lmdb
mkdir %LDMB_PATH%
python prepare_data.py --out %LDMB_PATH% --n_worker 16 ./modern_paintings_resized/
rem python -m torch.distributed.launch --nproc_per_node=2 --master_port=9876 train.py --arch swagan %LDMB_PATH%
