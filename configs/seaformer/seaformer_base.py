# model settings
norm_cfg = dict(type='SyncBN', requires_grad=True)

model_cfgs = dict(
        cfg1=[
            # k,  t,  c, s
            [3, 1, 16, 1],  
            [3, 4, 32, 2], 
            [3, 3, 32, 1]],  
        cfg2=[
            [5, 3, 64, 2],  
            [5, 3, 64, 1]],  
        cfg3=[
            [3, 3, 128, 2],  
            [3, 3, 128, 1]],
        cfg4=[
            [5, 4, 192, 2]],  
        cfg5=[
            [3, 6, 256, 2]], 
        channels=[16, 32, 64, 128, 192, 256],
        depths=[4, 4],
        key_dims=[16,24],
        emb_dims=[192, 256],
        num_heads=8,
        drop_path_rate=0.1,
)

model = dict(
    type='EncoderDecoder',
    backbone=dict(
        type='SeaFormer',
        cfgs=[model_cfgs['cfg1'], model_cfgs['cfg2'], model_cfgs['cfg3'], model_cfgs['cfg4'], model_cfgs['cfg5']],
        channels=model_cfgs['channels'],
        key_dims=model_cfgs['key_dims'],
        emb_dims=model_cfgs['emb_dims'],
        depths=model_cfgs['depths'],
        num_heads=model_cfgs['num_heads'],
        drop_path_rate=model_cfgs['drop_path_rate'],
        norm_cfg=norm_cfg,
        init_cfg=dict(type='Pretrained', checkpoint='ckpts/SeaFormer_B_cls_76.4.pth')
    ),
    decode_head=dict(
        type='LightHead',
        in_channels=[64, 192, 256],
        in_index=[0, 1, 2],
        channels=160,
        dropout_ratio=0.1,
        embed_dims=[128, 160],
        num_classes=150,
        is_dw=True,
        norm_cfg=norm_cfg,
        align_corners=False,
        loss_decode=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0)),
    # model training and testing settings
    train_cfg=dict(),
    test_cfg=dict(mode='whole'))