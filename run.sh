echo "DO NOT RUN THIS, This is just a buliding note"
exit
#
# Before
#

# generate self-host ssl
bash create_cert.sh

# clone tango
git clone https://github.com/autolab/Tango.git

# clone Autolab
git clone https://github.com/autolab/Autolab.git
cd Autolab
git checkout a4563ea24d32d3efc9644e758b32fe4cbc138e71
cp config/autogradeConfig.rb.template config/autogradeConfig.rb
cd ..

# Edit MANUALLY
cat web/nginx.conf
cp tango/config.py Tango/
cat docker-compose.yml
cp autolab/school.yml Autolab/config/school.yml
cp autolab/database.yml Autolab/config/database.yml
cp autolab/devise.rb Autolab/config/initializers/devise.rb

# build autolab
docker build build_autolab -f build_autolab/Dockerfile -t linnil1/autolab

# build tango
cp Tango/requirments.txt build_tango
docker build build_tango -f build_tango/Dockerfile -t linnil1/tango

# build grader
docker build build_judger -f build_judger/judger_python -t linnil1/judger_python
docker build build_judger -f build_judger/judger_java -t linnil1/judger_java

# Prepare data for mounting
cp -r Autolab/db autolab/
mkdir -p Autolab/tmp Autolab/courses Autolab/assessmentConfig Autolab/courseConfig Autolab/gradebooks Autolab/log

# Main
docker-compose up -d

# After
# Modify database (Run MANUALLY)
docker-compose exec db mysql -p
CREATE USER 'autolab'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
grant all privileges on autolab.* to 'autolab'@'%';
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
exit

# Update Database
docker-compose exec autolab bundle exec rake environment RAILS_ENV=production
docker-compose exec autolab bundle exec rake db:create
docker-compose exec autolab bundle exec rake db:reset
docker-compose exec autolab bundle exec rake db:migrate
docker-compose exec autolab bundle exec rake autolab:populate
