import torch
import argparse

if __name__ == '__main__':
	# 引数の解析
	parser = argparse.ArgumentParser()
	parser.add_argument(
        '--a',
        type=int
    )    
    parser.add_argument(
        '--b',
        type=int
    )
    args = parser.parse_args()
    
    # テンソルの足し算
    ans = torch.tensor(args.a) + torch.tensor(args.b)
    print(ans)