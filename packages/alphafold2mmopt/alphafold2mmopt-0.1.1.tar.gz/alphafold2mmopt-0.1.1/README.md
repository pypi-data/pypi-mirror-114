# alphafold2mmopt

`alphafold2mmopt` is a 2nd minimal developed tool forfine-tuning train of generated protein structures using `alphafold2` strategy

## dependence

```shell
pip install openmm
pip install dm-tree
pip install biopython
pip install dm-haiku
pip install --upgrade "jax[cpu]" -i https://pypi.tuna.tsinghua.edu.cn/simple
conda install -c omnia pdbfixer
```

## installation and run

* install

```shell
pip install alphafold2mmopt
```

* run: for a given any `*.pdb` file

```shell
alphafold2mmopt *.pdb
```



