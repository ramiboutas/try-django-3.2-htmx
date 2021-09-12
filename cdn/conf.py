import os

AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME='myspaces_name'
AWS_S3_ENDPOINT_URL="https://s3.amazonaws.com/whatever"

# more settings -> check docs django storages
# AWS_LOCATION
# AWS_S3_OBJECT_PARAMETERS

DEFAULT_FILE_STORAGE = "trydjango.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "trydjango.cdn.backends.StaticRootS3Boto3Storage"
