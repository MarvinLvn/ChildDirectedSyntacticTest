## 1) CHILDES

1) Create conda env, and install package `childespy`:

```bash
conda env create -f env.yml
conda activate cdsyn
```

2) Make sure R>=4.0.0 is installed on your system, then, in a R session, run: 

```R
devtools::install_github("langcog/childesr", "0.2.1")
```