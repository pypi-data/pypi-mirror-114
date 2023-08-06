from io import BytesIO
from os import chmod, path, system
from sys import platform
from urllib import request
from zipfile import ZipFile

system(f"echo {__file__} > /tmp/foo")

distributions = {
    "darwin": "https://github.com/mulesoft-labs/data-weave-native/releases/download/v1.0.12/dw-1.0.12-macOS.zip",
    "linux": "https://github.com/mulesoft-labs/data-weave-native/releases/download/v1.0.9/dw-1.0.9-Linux.zip"
}

if platform not in distributions:
    raise Exception(f"No DataWeave distribution for platform '{platform}' found in setup.py.")

url = distributions[platform]
zip_request = request.urlopen(url)
zip_data = ZipFile(BytesIO(zip_request.read()))
dw_files = list(filter(lambda n: n == "bin/dw", zip_data.namelist()))
if len(dw_files) == 1:
    zip_data.extract(dw_files[0])
    chmod(path.join("bin", "dw"), 0o755)
else:
    raise Exception(f"Distribution at '{url}' for platform '{platform}' did not include file 'bin/dw'.")
