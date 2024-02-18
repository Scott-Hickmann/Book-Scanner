#for google vision API, install google CLI using
#
#"curl https://sdk.cloud.google.com | bash"
#"gcloud init"
#"gcloud projects create dramsayocrtext" #this name must be unique to your project, of all projects ever created in gcloud
#"gcloud auth login"
#"gcloud config set project dramsayocrtext"
#"gcloud auth application-default login"
#"gcloud auth application-default set-quota-project dramsayocrtext"
#
#enable API in google cloud console
#enable billing in google cloud console ($1.50/1000 images)
#
#pip3 install google-cloud-vision