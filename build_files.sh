##updating pip
#python3.9 -m pip install --upgrade pip
#
##installing virtual machinea
#pip install virtualenv
#
##creating a new virtual environment
#virtualenv venv
#
##Activating virtual machine
#source venv/bin/activate
#
#
#
## Install dependencies from requirements.txt
#pip install -r requirements.txt
#
## Run collectstatic (assuming you have it defined in your Django project)
#python3.9 manage.py collectstatic



# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear