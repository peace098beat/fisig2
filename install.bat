pip uninstall -y fisig2
python -m unittest discover ./fisig2/
rm -rf ./fisig2/*.pyc
rm -rf ./fisig2/lib/*.pyc
rm -rf ./fisig2/utilities/*.pyc
rm -rf ./fisig2/__pycache__
python setup.py install
pip list | grep -i fisig2
python -m unittest discover ./tests/
python -m unittest discover
rm -rf ./fisig2/*.pyc
rm -rf ./fisig2/lib/*.pyc
rm -rf ./fisig2/utilities/*.pyc
rm -rf ./fisig2/__pycache__
rm -rf ./fisig2/lib/__pycache__
rm -rf ./fisig2/utilities/__pycache__
