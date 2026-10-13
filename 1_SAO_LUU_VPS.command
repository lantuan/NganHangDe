#!/bin/bash
# Bam dup (double-click) file nay tren Mac de chay.
cd "$(dirname "$0")" || exit 1
bash scripts/sao_luu_rieng.sh
echo
read -r -p "Xong. Bam Enter de dong cua so nay..." _
