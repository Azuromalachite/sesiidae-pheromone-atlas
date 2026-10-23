# usage: s001.sh select | run [slug...]
export OMP_NUM_THREADS=4 PYSCF_TMPDIR=$HOME/pyscf_tmp_s001
mkdir -p $PYSCF_TMPDIR
S=/mnt/c/Users/user/AppData/Local/Temp/claude/C--Users-user-Documents-espmap/669a3716-c2cd-43c5-9905-c4ad082b6f87/scratchpad
cd $HOME && /home/austintw/.venvs/espmap/bin/python $S/s001_run.py "$@"
