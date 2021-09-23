mkdir lmdb
python prepare_data.py --out lmdb --n_worker 16 /Users/Enrico/Downloads/stylegan2-pytorch-master/modern_paintings_resized/
rem python -m torch.distributed.launch --nproc_per_node=2 --master_port=9876 train.py --arch swagan /Users/Enrico/Downloads/stylegan2-pytorch-master/lmdb/amedeo-modigliani
