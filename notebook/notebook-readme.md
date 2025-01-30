- ~/.local/bin/python3.10 is the python interpreter

## install Dependencies

```bash
cd $HOME/projects/github/notebook-gena
#generate one-time requirements.txt
uv pip freeze > requirements.txt
#install requirements.txt
uv pip install -r requirements.txt
# in pyenv 3.10 of notebook-kernel
# uv pip install --system peek-python (if doing in already present pyenv o rpython install)
```
