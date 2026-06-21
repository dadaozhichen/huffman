# 文件路径
INPUT="in3.txt"
COMPRESSED="temp.huff"
OUTPUT="out3.txt"

# 压缩
echo "压缩 $INPUT -> $COMPRESSED"
python huffman.py -e -i "$INPUT" -o "$COMPRESSED"

# 解压
echo "解压 $COMPRESSED -> $OUTPUT"
python huffman.py -d -i "$COMPRESSED" -o "$OUTPUT"

# 显示各文件大小（字节）
echo "==================================="
echo "原文件大小:     $(stat -c %s "$INPUT") 字节"
echo "压缩后大小:     $(stat -c %s "$COMPRESSED") 字节"
echo "解压后大小:     $(stat -c %s "$OUTPUT") 字节"
echo "==================================="

# 可选：对比原文件和解压后文件是否相同
if cmp -s "$INPUT" "$OUTPUT"; then
    echo "✅ 解压后的文件与原文件完全一致"
else
    echo "❌ 解压后的文件与原文件不同"
fi