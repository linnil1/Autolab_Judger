# Before
# clone Autolab
git clone https://github.com/autolab/Autolab.git
cd Autolab
git checkout a4563ea24d32d3efc9644e758b32fe4cbc138e71
cp config/autogradeConfig.rb.template config/autogradeConfig.rb

# Edit this three files(Run maually)
cp ../autolab/school.yml config/school.yml
cp ../autolab/database.yml config/database.yml
cp ../autolab/devise.rb config/initializers/devise.rb
cd ..

# build dockerfile
cd build
docker build . -f Dockerfile -t linnil1/autolab
cd ..

# Prepare data for mountint
cp -r Autolab/db autolab/
mkdir -p Autolab/tmp Autolab/courses Autolab/assessmentConfig Autolab/courseConfig Autolab/gradebooks Autolab/log

# Main
docker-compose up -d

# After
# Modify database (Run maually)
docker exec -it $(docker ps -q -f name=autolab_db_1) mysql -p
CREATE USER 'autolab'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
grant all privileges on autolab.* to 'autolab'@'%';
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
exit

# Update Database
docker exec -it $(docker ps -q -f name=autolab_autolab_1) bundle exec rake db:create
docker exec -it $(docker ps -q -f name=autolab_autolab_1) bundle exec rake db:reset
docker exec -it $(docker ps -q -f name=autolab_autolab_1) bundle exec rake db:migrate
docker exec -it $(docker ps -q -f name=autolab_autolab_1) bundle exec rake autolab:populate
