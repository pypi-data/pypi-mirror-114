# geli-python-common #

Library for sharing common code among Python projects


### Virtualenv setup ###

 
Setup the virtual enviroment and install the necessary tools and packages 
```
    $ bash setup_venv.sh
```
    
    
Run the script below to manually build and upload the python-common package to the pypi server.
url of the pypi server: https://pypi.geli.net/pypi/

NOTE: This step will be not be required, once it is automated via the Jenkins pipeline
```
    $ bash build_and_upload_package_to_pypi.sh
```    


### How to use the geli-python-common package from a client app ###

Create virtual environment
```
    $ python3 -m venv venv
    $ source  ./venv/bin/activate
```


Install the geli-python-common package
```
    Add geli-python-common==1.0.0 to requirements.in.
    
    Run pip-compile, which outputs requirements.txt
    
    $ pip-compile requirements.in
    
    Add --extra-index-url https://developer:jellypunsaregreat@pypi.geli.net/simple/ to requirements.txt
    
    Run pip install
    
    $ pip install -r requirements.txt
```


