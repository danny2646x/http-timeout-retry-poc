FROM ruby:3.0

ARG APP_NAME

# No need to freeze the Gemfile.lock. This is just a POC
# throw errors if Gemfile has been modified since Gemfile.lock
# RUN bundle config --global frozen 1

WORKDIR /usr/src/${APP_NAME}

# Install gems
# Even though volume has been mounted, Gemfiles need to be copied for installation
COPY Gemfile Gemfile.lock ./
RUN bundle install

# No need to run COPY because volume has been mounted
# COPY . .

ENTRYPOINT ["ruby", "main.rb"]