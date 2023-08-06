import os
import random
from torchelper.utils.dist_util import get_rank
from torchelper.models.model_builder import ModelBuilder
from tqdm import tqdm
import torch 
import time

import torch.distributed as dist
import torch.multiprocessing as mp
from torchelper.utils.config import merge_cfg
from torchelper.utils.cls_utils import get_cls, new_cls, auto_new_cls
from torchelper.data.base_dataset import get_data_loader
import torch.backends.cudnn as cudnn
import subprocess
from torch.utils.tensorboard import SummaryWriter
from torchelper.utils import logger
 

def check_close_port(port):
    result = subprocess.run(['lsof', '-i:'+str(port)], stdout=subprocess.PIPE)
    out = result.stdout.decode('utf-8')

    lines = out.split('\n')
    if len(lines)<=1:
        return
    print(out)
    lines = lines[1:]
    for line in lines:
        arr = [s for s in line.split(' ') if len(s)>0]
        if len(arr)<2:
            continue
        pid = int(arr[1])
        os.system('kill '+str(pid))
        print("kill", pid)

def check_close_gpu_ids(gpu_ids):
    if not isinstance(gpu_ids, list):
        gpu_ids = [gpu_ids]
    print('kill:', gpu_ids)
    result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)
    out = result.stdout.decode('utf-8')

    lines = out.split('\n')
    if len(lines)<=1:
        return

    start_flag = False
    for line in lines:
        if not start_flag:
            if line.startswith('|=') and not '+' in line:
                start_flag = True
        else:
            line = ' '.join(line.split())
            arr = line.split(' ')
            if len(arr)<8:
                continue
            gpu_id = int(arr[1])
            pid = int(arr[4])
            for gid in gpu_ids:
                if gpu_id == gid and arr[6].endswith('/python'):
                    os.system('kill '+str(pid))
                    print('kill', arr[6])
      

def get_port(def_port):
    result = subprocess.run(['lsof', '-i:'+str(def_port)], stdout=subprocess.PIPE)
    out = result.stdout.decode('utf-8')

    lines = out.split('\n')
    if len(lines)<=1:
        return def_port
    return get_port(def_port+1)


def validate(builder:ModelBuilder, epoch:int, val_dataset):
    '''执行验证集
    :param net: ModelBuilder子类实例
    :param epoch: int, 当前epoch
    :param val_dataset: 验证集
    :return: 返回描述
    :raises ValueError: 描述抛出异常场景
    '''
    if get_rank()==0:
        builder.set_eval()
        # net.before_validate(epoch)
        # time.sleep(10)
        
        val_data:dict = {}
        
        for data in tqdm(val_dataset):
            res = builder.validate(epoch, data)
            if res is None:
                continue
            for key, val in res.items():
                val_data[key] = val + val_data.get(key, 0)
        
        line = 'epoch: '+str(epoch)+', '
        avg_val_dict = {}
        if val_data is not None:
            val_arr = []
            for key, val in val_data.items():
                val_arr.append(key + ":" + str(val_data[key] * 1.0 / len(val_dataset)))
                avg_val_dict[key] = val_data[key] * 1.0 / len(val_dataset)
            line = line+', '.join(val_arr)
        # builder.on_val_end(avg_val_dict)
        builder.perform_cb('on_end_val', epoch=epoch, metric_dict=avg_val_dict)
        print(line)
    torch.distributed.barrier()

#更新tensorboard显示
def update_tensorboard(builder:ModelBuilder, tb_writer, epoch, step, step_per_epoch_per_gpu, gpu_count):
    if tb_writer is None:
        return
    audios = builder.get_audio_dict()
    images = builder.get_img_dict()
    scalars = builder.get_scalar_dict()
    metrics = builder.get_metric_dict()
    audios = audios if audios is not None else {}
    images = images if images is not None else {}
    scalars = scalars if scalars is not None else {}
    metrics = metrics if metrics is not None else {}
 
    step =  (epoch*step_per_epoch_per_gpu+step)*gpu_count
    # print(epoch, step_per_epoch_per_gpu, epoch*step_per_epoch_per_gpu)
    for k, v in audios.items():
        if v is None:
            logger.warn(k+" is None ... ")
            continue    
        tb_writer.add_audio(k, v, step, sample_rate=16000)
    for k, v in images.items():
        if v is None:
            logger.warn(k+" is None ... ")
            continue
        tb_writer.add_image(k, v, step)
    for k, v in scalars.items():
        if v is None:
            logger.warn(k+" is None ... ")
            continue
        tb_writer.add_scalar(k, v, step)
    for k, v in metrics.items():
        if v is None:
            logger.warn(k+" is None ... ")
            continue
        tb_writer.add_scalar(k, v, step)

def update_pbar(builder:ModelBuilder, pbar):
    if pbar is None:
        return
    scalars = builder.get_scalar_dict()
    if scalars is None:
        return
    msg = []
    for k, v in scalars.items():
        msg.append('%s:%.5f'%(k, v))
    pbar.set_description(', '.join(msg))

def train(gpu_id, cfg, is_dist):
   
    train_data_cfg = merge_cfg(cfg['dataset']['train'], cfg)
    val_data_cfg =  merge_cfg(cfg['dataset']['val'], cfg)
    train_dataset = auto_new_cls(train_data_cfg)
    val_dataset = auto_new_cls(val_data_cfg)
    gpu_count = len(cfg['ori_gpu_ids'])
 
    train_dataloader = get_data_loader(cfg['batch_per_gpu'], train_dataset, num_workers=0, dist=True)
    val_dataloader = get_data_loader(cfg['batch_per_gpu'], val_dataset, dist=False)

    builder:ModelBuilder = get_cls(cfg['model_builder'])(cfg, True, cfg['ckpt_dir'])
 
    builder.set_dataset(train_dataset)
    dataset_size = len(train_dataloader)
    
    tb_writer = None
    step_per_epoch_per_gpu = dataset_size 
    if gpu_id==0:
        tb_writer = SummaryWriter(cfg['ckpt_dir'])

    builder.perform_cb('on_begin_train', epoch=cfg['start_epoch'])
    for epoch in range(cfg['start_epoch'], cfg['total_epoch']):
        # validate(builder, epoch, val_dataloader)
        builder.set_train()
        if gpu_id==0:
            pbar = tqdm(train_dataloader)
            enum_data = enumerate(pbar)
        else:
            pbar = None
            enum_data =  enumerate(train_dataloader)
        builder.perform_cb('on_begin_epoch', epoch=epoch)
        for i, data in enum_data:
            builder.on_begin_forward(data, epoch, i)
            builder.perform_cb('on_begin_step', epoch=epoch, step=i)
            builder.forward_wrapper(epoch, i, data)
            builder.on_end_forward(  epoch, i)
            builder.on_begin_backward( epoch, i)
            # 计算loss
            builder.backward_wrapper()
            if is_dist:   # 多卡同步
                torch.distributed.barrier()
            builder.on_end_backward( epoch, i)
            builder.perform_cb('on_end_step', epoch=epoch, step=i)
            if gpu_id==0:
                update_pbar(builder, pbar)
                update_tensorboard(builder, tb_writer, epoch, i, step_per_epoch_per_gpu, gpu_count)
        builder.perform_cb('on_end_epoch', epoch=epoch)
        # builder.save_model(epoch, save_max_count, save_max_time)
        validate(builder, epoch, val_dataloader)
    builder.perform_cb('on_end_train')


def train_worker(gpu_id, nprocs, cfg, is_dist, port):
    '''独立进程运行
    '''
    os.environ['NCCL_BLOCKING_WAIT']="1"
    os.environ['NCCL_ASYNC_ERROR_HANDLING']='1'
    random.seed(0)
    torch.manual_seed(0)
    cudnn.deterministic = True
    # 提升速度，主要对input shape是固定时有效，如果是动态的，耗时反而慢
    torch.backends.cudnn.benchmark = True
    dist.init_process_group(backend='nccl',
                            init_method='tcp://127.0.0.1:'+str(port),
                            world_size=len(cfg['gpu_ids']),
                            rank=gpu_id)

    torch.cuda.set_device(gpu_id)
    # 按batch分割给各个GPU
    # cfg['batch_size'] = int(cfg['batch_size'] / nprocs)
    train(gpu_id, cfg, is_dist)

def train_main(cfg):
    check_close_gpu_ids(cfg['ori_gpu_ids'])
    # check_close_port(cfg['port'])
    gpu_nums = len(cfg['gpu_ids'])
    # if gpu_nums>1:
    port = get_port(cfg['port'])
    print('init port:', port)
    mp.spawn(train_worker, nprocs=gpu_nums, args=(gpu_nums, cfg, True, port))
    # else:
    #     train(cfg['gpu_ids'][0], cfg, False)
