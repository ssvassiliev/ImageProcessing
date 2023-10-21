
## Installing Micasense image processing libraries
### Create directories where you want to install packages
```ruby
INSTALL_DIR=/project/def-mbarbeau/gnorris/MicaSense
LIBZBAR_INSTALL_DIR=${INSTALL_DIR}/libzbar
mkdir -p ${INSTALL_DIR}
cd ${INSTALL_DIR}
```
### Create and activate a python virtual environment
```ruby
module load python/3.10.2
virtualenv env-micasense
source env-micasense/bin/activate
```

### Install zbar
```ruby
git clone https://github.com/mchehab/zbar   
cd zbar && autoreconf -vfi  
./configure --prefix=${LIBZBAR_INSTALL_DIR} --without-dbus 
make install  
cd ..
export LD_LIBRARY_PATH=${LIBZBAR_INSTALL_DIR}/lib 
```

### Install exiftool
```ruby
wget https://exiftool.org/Image-ExifTool-12.67.tar.gz
tar -xf Image-ExifTool-12.67.tar.gz && cd Image-ExifTool-12.67
perl Makefile.PL 
make
cd ..
export PATH=$PATH:${INSTALL_DIR}/Image-ExifTool-12.67
```

### Install GDAL in a virtual environment
- On the Alliance systems python bindings are included in the GDAL module, no installation is required.
```
module load gcc/9.3.0 opencv/4.8.0 gdal/3.5.1
```
- On other systems first install GDAL, then install python module:
```
pip install GDAL==$(gdal-config --version)
```

### Install MicaSense imageprocessing
```ruby
git clone https://github.com/micasense/imageprocessing
cd imageprocessing
module load gcc/9.3.0 opencv/4.8.0 gdal/3.5.1
pip install pysolar pyexiftool==0.4.13 pyzbar
pip install --no-index .
```
### Run check_panels.py
```ruby
module load gcc/9.3.0 opencv/4.8.0 gdal/3.5.1
INSTALL_DIR=/home/svassili/projects/def-svassili/svassili/ODM
cd ${NSTALL_DIR}/ImageProcessing
source ../env-micasense/bin/activate
export PATH=$PATH:${INSTALL_DIR}/Image-ExifTool-12.67
export LD_LIBRARY_PATH=${INSTALL_DIR}/libzbar/lib
python check_panels.py
```

## MicaSense RedEdge-M bands:
'Blue', 'Green', 'Red', 'NIR', 'Red edge'  
'Blue-444', 'Green-531', 'Red-650', 'Red edge-705', 'Red edge-740'

## Building NodeODM container 
```ruby
apptainer build --fakeroot node_ODM.sif apptainer.def  
apptainer overlay create --fakeroot --size 32000 ${SLURM_TMPDIR}/NodeODM.ovl
apptainer run --fakeroot --overlay NodeODM.ovl NodeODM.sif
```

```ruby
--- File: nodeodm.def ---
Bootstrap: docker
From: opendronemap/odm:latest

%setup
mkdir -p ${APPTAINER_ROOTFS}/var/www

%files
/home/svassili/ODM/NodeODM/* /var/www/

%post
su - root
apt update && apt install -y curl telnet git
curl --silent --location https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs gdal-bin unzip p7zip-full && npm install -g nodemon && \
ln -s /code/SuperBuild/install/bin/entwine /usr/bin/entwine && \
ln -s /code/SuperBuild/install/bin/entwine /usr/bin/untwine && \
ln -s /code/SuperBuild/install/bin/pdal /usr/bin/pdal

cd /var/www
npm install --production && mkdir -p tmp

%runscript
/bin/bash <<EOF
cd /var/www
node index.js
```

## Building ClusterODM container
```ruby
apptainer build --fakeroot ClusterODM.sif  ClusterODM.def
apptainer overlay create --fakeroot --size 3000 ClusterODM.ovl
apptainer run --fakeroot --overlay ClusterODM.ovl  ClusterODM.sif 
```

```ruby
--- File: clusterodm.def ---
Bootstrap: docker
From: node:lts

%post
su - root
apt update && apt install -y curl telnet git
git clone https://github.com/OpenDroneMap/ClusterODM 
cd ClusterODM
npm install
mv config-default.json config-default.json.org
cat config-default.json.org | sed 's/"admin-pass": "",/"admin-pass": "12345!",/g' > config-default.json 

%runscript
/bin/bash <<EOF
cd /ClusterODM
node index.js
EOF
```

### Using cluster ODM CLI:
```ruby
telnet nc11125 8080
LOGIN 12345!
NODE ADD 10.82.90.29 3000
NODE LIST
```

## Building WebODM container
```ruby
sudo snap install docker  
git clone https://github.com/OpenDroneMap/WebODM --config core.autocrlf=input --depth 1
cd WebODM
./webodm.sh start 
```

Currently ODM recognized images with up to 8 bands as multispectral.

Types.py can be patched for a 10-band camera: 

```ruby
sed 's/bands_count <= 8:/bands_count <= 10:/g' /code/opendm/types.py
```

1. Build sandbox
2. Edit types.py
3. Build production image from sandbox

