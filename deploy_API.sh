# Params
breakline="##################"
echo "${breakline}"
echo "Deploying API"
echo "${breakline}"
echo ""

# Params validation
cloud_project_id="tangential-box-363014"
service_account="tangential-box-363014@appspot.gserviceaccount.com"
vpc_connector="learning-google-cf"

# Set Variables
bucket="gs://cloud_functions_temporary/"
file_name="tmp_api_subida_video.zip"
code_source=${bucket}${file_name}
tmp="tmp_api_subida_video"

deploy_API()
{
  echo "Deploying API Subida Video into Cloud Functions"
  echo ""

  gcloud functions deploy $1 \
      --memory=$2 \
      --runtime=python39 \
      --timeout=540s \
      --service-account=${service_account} \
      --source=${code_source} \
      --trigger-http \
      --entry-point=$1 \
      --vpc_connector=${vpc_connector} \
      --env-vars-file settings/.envcloudfunctions.yaml

}

echo "Validating Finished"
echo ""

# Stop if any error happen
set -e

# Building package
echo "Creating tmp folder"

mkdir ${tmp}
mkdir ${tmp}/log
mkdir ${tmp}/function_subida_video

#APIs needed packages
echo "Copying packages required..."
cp -R settings/ ${tmp}/settings
cp -R pkg_util/ ${tmp}/pkg_util

cp requirements.txt ${tmp}/requirements.txt

# This package
cp -R api/ ${tmp}/api
cp function_subida_video/*.py ${tmp}/
cp function_subida_video/*.yaml ${tmp}/function_subida_video/

# Preparing to send to GCP
echo "Zipping files..."
cd ${tmp}
zip -r ../${file_name} . -q
cd ..

# Connecting to GCP
echo "Setting GCP Project..."
gcloud config set project ${cloud_project_id}

# Sending packages
echo "Sending package to GCP bucket" ${code_source}
gsutil cp ${file_name} ${code_source}
echo ""

# Cleaning old files
echo "Cleaning TMP folder"
rm -f -r -d ${tmp}
rm -f ${file_name}
echo ""

deploy_API upload_video 1024MB


echo ${breakline}
echo "Functions Successfully deployed"
echo ${breakline}