## Preprocessing images.
Radiometric calibration, DLS correction, and panel correction are performed by preprocess.py.

### Default project directory tree

```ruby
Project/
├── images
├── panels
└── raw_images
```
Input
- raw_images: all images excluding panel 
- panel: panel images
Output
- images: preprocessed images (radiometric calibration + DLS + panel correction)

### 1. Set environment variables

```ruby
source setvars.sh
```

### 2. Check panel images
When QR code can be read panels are detected and read automatically. The program needs to see QR code to locate a panel. If QR code is not visible panel will not be detected and you will need to read it manually. In some cases QR code is visible, but panel albedo QR item may be clipped. It such case program will locate and read panel data, but you will need to provide albedo manually.

```ruby
(env-micasense) [gnorris@narval1 ImageProcessing]$ python check_panels.py ../Rockland_November_2020/panels/ -fIMG_0773_

...
Error: could not read albedo from 1 panel(s)
Error: 1 panel(s) failed:

Reflectance:
0.5326, 0.5311, 0.5291, 0.5259, 0.5282, 0.5332, 0.5316, nan, 0.5284, 0.5278, 
Irradiance:
0.2345, 0.2206, 0.1904, 0.1232, 0.1651, 0.2120, 0.2223, nan, 0.1672, 0.1560, 
```

In the example above QR code was clipped and albedo of the panel 8 was missing. In this case you will need to provide albedos of all panels manually. 

If there is a message "Panel not found" you will need to read it manually as described in step 3. Otherwise, skip it and proceed to step 4.

### 3. Read panel manually (if needed)
To read a panel you need to provide two panel corners and albedo (options -c and -a).

```ruby
python read_panel.py data/panels_0/IMG_0000_1.tif -c 874 784 704 615 -a 0.53
```

### 4. Preprocess images

Script needs panel albedo and panel image to calculate panel irradiance:

<irradiance> = <radiance> * pi / albedo

Radiance is the energy per unit solid angle,  W/(sr·m^2). It is determined from images using radiometric calibration parameters stored in metadata. 

Irradiance is the radiant flux received by a surface per unit area (W/m^2).

If all panels are OK, script will do it automatically.

If some albedo's can not be read but panels are detected you need to pass a list of albedos in the command line.

```ruby
python preprocess.py -n773 -d${PROJECT_DIR}  -e773 \
-a 0.5326 0.5311 0.5291 0.5259 0.5282 0.5332 0.5316 0.5294 0.5284 0.5278 
```

If some panels are not detected, you need to pass a list of panel irradiances in the command line. You can obtain irradiances of undetected panels with read_panel.py. 

## Installing Micasense image processing libraries
### Create and activate a python virtual environment

module load python/3.10.2
virtualenv env-micasense
source env-micasense/bin/activate

### Install zbar
```ruby
LIBZBAR_INSTALL_DIR=$HOME/projects/def-svassili/svassili/ODM/libzbar
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
export PATH=$PATH:$HOME/projects/def-svassili/svassili/ODM/Image-ExifTool-12.67
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

### Install Micasense imageprocessing
```ruby
git clone https://github.com/micasense/imageprocessing
cd imageprocessing
module load gcc/9.3.0 opencv/4.8.0 gdal/3.5.1
pip install pysolar pyexiftool==0.4.13 pyzbar
pip install --no-index .
```
### Run Panels.py
cd /home/svassili/projects/def-svassili/svassili/ODM/ImageProcessing
module load gcc/9.3.0 opencv/4.8.0 gdal/3.5.1
source ../env-micasense/bin/activate
export PATH=$PATH:$HOME/projects/def-svassili/svassili/ODM/Image-ExifTool-12.67
export LD_LIBRARY_PATH=$HOME/projects/def-svassili/svassili/ODM/libzbar/lib
python Panels.py

## MicaSense RedEdge-M bands:
'Blue', 'Green', 'Red', 'NIR', 'Red edge'  
'Blue-444', 'Green-531', 'Red-650', 'Red edge-705', 'Red edge-740'

increase:  
--feature-quality  
--min-num-features  
--matcher-neighbors   
--matcher-distance   
--min-num-features 60000  

https://community.opendronemap.org/t/hpc-scheduler-e-g-slurm-integration-for-clusterodm/3285/7

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

