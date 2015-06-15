web: sh -c "NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python run.py"

worker: celery worker --app worker -B --config=celeryconfig --loglevel=info # -B = beat

# This is better for production, but it would need two Heroku workers
#worker: celery worker --broker=$REDIS_URL --config=celeryconfig --loglevel=info
#beat: celery beat --app worker --broker=$REDIS_URL --config=celeryconfig --loglevel=info
