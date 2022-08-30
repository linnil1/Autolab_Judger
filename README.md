# Autolab docker-compose

The setup of DSA course judge system for our lab.


## Setup

Setup all services: autolab, tango, database

``` bash
git clone github:linnil1/Autolab_Judger.git autolab
cd autolab

git clone https://github.com/autolab/Tango.git
git clone https://github.com/autolab/Autolab.git
cp Tango/requirements.txt build_tango
cp Autolab/Gem* build_autolab
cp tango/config.py Tango/
cp autolab/school.yml Autolab/config/school.yml
cp autolab/database.yml Autolab/config/database.yml
cp Autolab/config/autogradeConfig.rb.template Autolab/config/autogradeConfig.rb
cp Autolab/config/environments/production.rb.template Autolab/config/environments/production.rb
sed -i "s/config.assets.compile.*/config.assets.compile = true/g" Autolab/config/environments/production.rb
```

and change this lines in `docker-compose.yml`
* `DOCKER_TANGO_HOST_VOLUME_PATH=/home/linnil1/autolab/tango/volume`  (change to `$PWD/tango/volume`)
* `DEVISE_SECRET_KEY: "changeThisSecret"`
* ALL SMTP fields


## Start

Note: I separate Tango into differnet containers (one for api server, one for resource manager)

``` bash
# start
docker-compose up -d

# init db (run this after started if it's first time)
docker exec autolab_main bundle exec rake db:create
docker exec autolab_main bundle exec rake db:reset
docker exec autolab_main bundle exec rake db:migrate

# restart main autolab
docker-compose restart autolab && rm -f autolab/tmp/pids/server.pid

# restart all
docker-compose restart

# stop all
docker-compose stop
```

Then, open [localhost:3000](http://localhost:3000) in browser


## Disable Registeration (Optional)

If you want create/modify the accounts manually and 
don't want to setup SMTP email service,
you can disable registeration and forgeting password serivce shown in below.

(Not all configs writen in `Autolab/config`)

e.g. Remove Register page

In `Autolab/app/models/user.rb`
```
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable,
         :confirmable
```

to

```
  devise :database_authenticatable, :rememberable, :trackable, :validatable
```


## Add user

### admin
```
docker exec autolab_main bundle exec rails admin:create_root_user[email,password,first_name,last_name]
```

### user
It's recommended to add user in the webpage (Manage Course > Manage students)

### Add user by command line (Optional)
```
docker run -it --rm -v $PWD:/app --network autolab_judger_default linnil1/tango python user_manage.py list
docker run -it --rm -v $PWD:/app --network autolab_judger_default linnil1/tango python user_manage.py add "email" "username"
docker run -it --rm -v $PWD:/app --network autolab_judger_default linnil1/tango python user_manage.py passwd "email" "password"
```


## Build Judger (for example)

Setup your own customized judger


### setup
``` bash
cd build_judger

# build dockerfile (fill the name `judger_python` in `VM Image` field (Edit Assessment > Autograder))
docker build . -f judger_python.dockerfile -t judger_python

# prepare required judger files
# autograde-Makefile and autograde.tar
cd autograde
tar cvf autograde.tar autograde

# copy the desitnation (for skiping uploading)
cp autograde* ../autolab/courses/{class_name}/{assignment_name}/

cd ../..
```

The core of judge is written in `runJob` in `Tango/vmms/localDocker.py`,

which is mostly equivalent to `args = args + ['cp -r mount/* autolab/; bash -c "cd autolab; make"; cp output/feedback mount/feedback']` (unsafe).


### Result

The output of judger look like this
```
...
{"scores": {"Q1": 10}}
```

The autolab will read the last line,
and automatically calculate the final score of all the problems in this assessment (see `Edit Assessment > PROBLEMS`)


## Some bugs (I think)

Overwrite the hostname by `hostname = "http://autolab:3000"` in `Autolab/app/helpers/assessment_autograde_core.rb`.
