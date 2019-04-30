# WebBasedDMBC
Repo for COMP 383/483 project

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'

sudo apt update

sudo apt install r-base r-base-dev

sudo flask db init

sudo flask db migrate -m "update db"
