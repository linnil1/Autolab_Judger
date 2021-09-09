# Our Autolab docker-compose

I separate all the modules (especially tango part) into differnet containers


## Download and start

``` bash
git clone github:linnil1/Autolab_Judger.git autolab
cd autolab
git clone https://github.com/autolab/Tango.git
git clone https://github.com/autolab/Autolab.git
cp Tango/requirments.txt build_tango
cp Autolab/Gem* build_autolab
docker-compose up -d
```


## Build Judger

``` bash
cd build_judger
docker build  . -f judger.veryfree.dockerfile -t freejudger
cp autograde* ../autolab/courses/{class_name}/{assignment_name}/
cd ..
```


## Autolab setting

```
cp tango/config.py Tango/
cp autolab/school.yml Autolab/config/school.yml
cp autolab/database.yml Autolab/config/database.yml
cp autolab/devise.rb Autolab/config/initializers/devise.rb
```


## Init database

``` bash
docker exec autolab_main bundle exec rake db:create
docker exec autolab_main bundle exec rake db:reset
docker exec autolab_main bundle exec rake db:migrate
```
