import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
CHUNK_UPLOAD_SIZE = 600000 #600K
#IMG_UPLD_PREFIX_URL = 'http://localhost:5000/api/'
#IMG_UPLD_PREFIX_URL = 'https://localhost:44335/api/'
IMG_UPLD_PREFIX_URL = 'https://services.simulo.ai/imgdataupload/api/'
BASE_IMG_UPLD_URL = IMG_UPLD_PREFIX_URL + 'Upload/'
#ACCT_MGMT_PREFIX_URL = 'http://localhost:5010/api/'
#ACCT_MGMT_PREFIX_URL = 'https://localhost:44334/api/'
ACCT_MGMT_PREFIX_URL = 'https://services.simulo.ai/acctmgmt/api/'
BASE_ACCT_MGMT_URL = ACCT_MGMT_PREFIX_URL + 'account/'
BASE_USR_PROF_MGMT_URL = ACCT_MGMT_PREFIX_URL + 'userprofile/'
VERIFY_CERTIFICATE = True