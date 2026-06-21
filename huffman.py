import argparse
import os 
class Node:
    def __init__(self,str,freq,l=None,r=None) -> None:
        self.freq=freq
        self.char = str 
        self.l = l
        self.r = r
    def __lt__(self, other):
        return self.freq<other.freq
class Haffman:
    def __init__(self,root,code:dict[str,str]) -> None:
        self.root = root 
        self.code =code
    def encode(self,str):
        ans = ''.join([self.code[x] for x in str])
        return ans 
    def decode(self,str):
        ans =''
        p = self.root
        for v in str:
            if v=='0':
                p = p.l
            else:
                p = p.r
            if p.char!=None:
                ans = ans+p.char 
                p = self.root 
        return ans



def build(freq:list[tuple[str,int]])->Haffman:
    from heapq import heappush,heappop,heapify
    heap = [(x[1],Node(x[0],x[1])) for x in freq]
    code = {}
    heapify(heap)
    while len(heap)>1:
        tmp1 = heappop(heap)
        tmp2 = heappop(heap)
        newfreq = tmp1[0]+tmp2[0]
        newnode = Node(None,newfreq,tmp1[1],tmp2[1])
        tmp3 = (tmp1[0]+tmp2[0],newnode)
        heappush(heap,tmp3)
    _,root = heappop(heap)
    def dfs(u,str):
        if u==None:
            return 
        if u.char!=None:
            code[u.char] = str
        dfs(u.l,str+'0')
        dfs(u.r,str+'1')
    dfs(root,'')
    tree = Haffman(root,code)
    return tree 
def count_freq(s:str):
    m = dict()
    for c in s:
        v = m.get(c,0)
        m[c] = v+1
    return [x for x in m.items()]
def pack(bit_str: str) -> bytes:
    original_len = len(bit_str)                     
    padding = (8 - original_len % 8) % 8
    if padding:
        bit_str += '0' * padding                    
    data = bytearray()
    for i in range(0, len(bit_str), 8):
        byte = int(bit_str[i:i+8], 2)
        data.append(byte)
    header = bytes([padding]) + original_len.to_bytes(4, 'big')   
    return header + bytes(data)

def unpack(data: bytes) -> str:
    padding = data[0]
    original_len = int.from_bytes(data[1:5], 'big')
    full_bit_str = ''
    for b in data[5:]:
        full_bit_str += f'{b:08b}'
    return full_bit_str[:original_len] 

def compress(src_path: str, dst_path: str):
    with open(src_path, 'r', encoding='utf-8') as f:
        text = f.read()
    freq = count_freq(text)          
    tree = build(freq)
    bit_str = tree.encode(text)
    packed_data = pack(bit_str)      
    with open(dst_path, 'wb') as f:
      
        f.write(len(freq).to_bytes(2, 'big'))
        for ch, fr in freq:
            
            f.write(ord(ch).to_bytes(4, 'big'))
            
            f.write(fr.to_bytes(4, 'big'))
        f.write(packed_data)

def decompress(in_path: str, out_path: str):
    with open(in_path, 'rb') as f:
        freq_len = int.from_bytes(f.read(2), 'big')
        freq = []
        for _ in range(freq_len):
            code = int.from_bytes(f.read(4), 'big')
            ch = chr(code)                   
            fr = int.from_bytes(f.read(4), 'big')
            freq.append((ch, fr))

        tree = build(freq)
        compressed_data = f.read()

    bit_str = unpack(compressed_data)        
    original_text = tree.decode(bit_str)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(original_text)
def main():
    parser = argparse.ArgumentParser('encode or decode')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encode','-e',action='store_true')
    group.add_argument('--decode','-d',action='store_true')
    parser.add_argument('--input','-i',type=str,required=True)
    parser.add_argument('--output','-o',type=str,default=None)
    args = parser.parse_args()

    if args.encode:
        output_path = args.output if args.output else args.input[:-4]+'.huff'
        compress(args.input,output_path)
        print(f"The compressed file is in {output_path}")
    else:
        if args.output:
            output_path = args.output
        else:
            output_path = args.input[:-5]+'.txt'
        decompress(args.input,output_path)
        print(f"The decompressed file is in {output_path}")
if __name__ == '__main__':
    main()