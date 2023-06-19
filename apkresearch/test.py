# -*- coding: utf-8 -*-
import pandas as pd

# �t�@�C����ǂݍ���
df = pd.read_csv('output_result.csv')

# Permission��𒊏o���A���ꂼ��̒l�̏o���񐔂��J�E���g
permission_counts = df.loc[:, 'Permission':].apply(pd.Series.value_counts).sum(axis=1)

# ���ʂ�\��
permission_counts.to_csv('permission_counts.csv')