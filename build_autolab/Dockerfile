FROM ruby:2.6.8

WORKDIR /opt
ADD Gemfile /opt/
ADD Gemfile.lock /opt/

RUN gem install bundler && \
    bundle install

WORKDIR /app
CMD bundle exec rails server -p 3000 --binding=0.0.0.0
