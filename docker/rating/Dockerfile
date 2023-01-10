FROM python:3.8-slim-buster

# install python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# create user
ENV APP_USER=rating
RUN useradd -ms /bin/bash $APP_USER

# create the appropriate directories
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME && chown $APP_USER:$APP_USER -R $APP_HOME
WORKDIR $APP_HOME

# copy project
COPY --chown=$APP_USER:$APP_USER src/rating/ $APP_HOME/
COPY --chown=$APP_USER:$APP_USER .env $APP_HOME/

# change to the app user
USER $APP_USER

# run app
CMD gunicorn --bind 0.0.0.0:$PORT manage:app
