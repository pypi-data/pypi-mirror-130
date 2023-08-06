ATLIGATOR is created to analyse protein-protein or protein-peptide interactions.


For the compilation of scipy and numpy you might need to install the compilers first 
(or try to use only wheel files, see below! This might depend on your OS environment):
sudo apt-get install gfortran libopenblas-dev liblapack-dev
Additionally, if installation fails because of the build process of dependencies use the '--only-binary=:all:' flag:
python -m pip install --only-binary=:all: atligator