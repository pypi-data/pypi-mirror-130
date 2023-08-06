[![PyPI version](https://badge.fury.io/py/pycert.svg)](https://badge.fury.io/py/pycert)

# Certificate

The cross-platform tool to get certificate info (including self-signed).

## Installation

For most users, the recommended method to install is via pip:

```cmd
pip install pycert
```

## Import

```python
from pycert import CertClient
```

---

## Usage

#### Command from usual user:

```python
from pycert import CertClient

client = CertClient(host="172.16.0.124")
print(client.get_all_info())

```

```python
from pprint import pprint
from pycert import CertClient

cert = CertClient('google.com')

pprint(cert.get_all_info())

```

```
{'alternative_name': ['DNS:*.google.com',
                      'DNS:*.appengine.google.com',
                      'DNS:*.bdn.dev',
                      'DNS:*.cloud.google.com',
                      'DNS:*.crowdsource.google.com',
                      'DNS:*.datacompute.google.com',
                      'DNS:*.google.ca',
                      'DNS:*.google.cl',
                      'DNS:*.google.co.in',
                      'DNS:*.google.co.jp',
                      'DNS:*.google.co.uk',
                      'DNS:*.google.com.ar',
                      'DNS:*.google.com.au',
                      'DNS:*.google.com.br',
                      'DNS:*.google.com.co',
                      'DNS:*.google.com.mx',
                      'DNS:*.google.com.tr',
                      'DNS:*.google.com.vn',
                      'DNS:*.google.de',
                      'DNS:*.google.es',
                      'DNS:*.google.fr',
                      'DNS:*.google.hu',
                      'DNS:*.google.it',
                      'DNS:*.google.nl',
                      'DNS:*.google.pl',
                      'DNS:*.google.pt',
                      'DNS:*.googleadapis.com',
                      'DNS:*.googleapis.cn',
                      'DNS:*.googlevideo.com',
                      'DNS:*.gstatic.cn',
                      'DNS:*.gstatic-cn.com',
                      'DNS:googlecnapps.cn',
                      'DNS:*.googlecnapps.cn',
                      'DNS:googleapps-cn.com',
                      'DNS:*.googleapps-cn.com',
                      'DNS:gkecnapps.cn',
                      'DNS:*.gkecnapps.cn',
                      'DNS:googledownloads.cn',
                      'DNS:*.googledownloads.cn',
                      'DNS:recaptcha.net.cn',
                      'DNS:*.recaptcha.net.cn',
                      'DNS:widevine.cn',
                      'DNS:*.widevine.cn',
                      'DNS:ampproject.org.cn',
                      'DNS:*.ampproject.org.cn',
                      'DNS:ampproject.net.cn',
                      'DNS:*.ampproject.net.cn',
                      'DNS:google-analytics-cn.com',
                      'DNS:*.google-analytics-cn.com',
                      'DNS:googleadservices-cn.com',
                      'DNS:*.googleadservices-cn.com',
                      'DNS:googlevads-cn.com',
                      'DNS:*.googlevads-cn.com',
                      'DNS:googleapis-cn.com',
                      'DNS:*.googleapis-cn.com',
                      'DNS:googleoptimize-cn.com',
                      'DNS:*.googleoptimize-cn.com',
                      'DNS:doubleclick-cn.net',
                      'DNS:*.doubleclick-cn.net',
                      'DNS:*.fls.doubleclick-cn.net',
                      'DNS:*.g.doubleclick-cn.net',
                      'DNS:doubleclick.cn',
                      'DNS:*.doubleclick.cn',
                      'DNS:*.fls.doubleclick.cn',
                      'DNS:*.g.doubleclick.cn',
                      'DNS:dartsearch-cn.net',
                      'DNS:*.dartsearch-cn.net',
                      'DNS:googletraveladservices-cn.com',
                      'DNS:*.googletraveladservices-cn.com',
                      'DNS:googletagservices-cn.com',
                      'DNS:*.googletagservices-cn.com',
                      'DNS:googletagmanager-cn.com',
                      'DNS:*.googletagmanager-cn.com',
                      'DNS:googlesyndication-cn.com',
                      'DNS:*.googlesyndication-cn.com',
                      'DNS:*.safeframe.googlesyndication-cn.com',
                      'DNS:app-measurement-cn.com',
                      'DNS:*.app-measurement-cn.com',
                      'DNS:gvt1-cn.com',
                      'DNS:*.gvt1-cn.com',
                      'DNS:gvt2-cn.com',
                      'DNS:*.gvt2-cn.com',
                      'DNS:2mdn-cn.net',
                      'DNS:*.2mdn-cn.net',
                      'DNS:googleflights-cn.net',
                      'DNS:*.googleflights-cn.net',
                      'DNS:admob-cn.com',
                      'DNS:*.admob-cn.com',
                      'DNS:*.gstatic.com',
                      'DNS:*.metric.gstatic.com',
                      'DNS:*.gvt1.com',
                      'DNS:*.gcpcdn.gvt1.com',
                      'DNS:*.gvt2.com',
                      'DNS:*.gcp.gvt2.com',
                      'DNS:*.url.google.com',
                      'DNS:*.youtube-nocookie.com',
                      'DNS:*.ytimg.com',
                      'DNS:android.com',
                      'DNS:*.android.com',
                      'DNS:*.flash.android.com',
                      'DNS:g.cn',
                      'DNS:*.g.cn',
                      'DNS:g.co',
                      'DNS:*.g.co',
                      'DNS:goo.gl',
                      'DNS:www.goo.gl',
                      'DNS:google-analytics.com',
                      'DNS:*.google-analytics.com',
                      'DNS:google.com',
                      'DNS:googlecommerce.com',
                      'DNS:*.googlecommerce.com',
                      'DNS:ggpht.cn',
                      'DNS:*.ggpht.cn',
                      'DNS:urchin.com',
                      'DNS:*.urchin.com',
                      'DNS:youtu.be',
                      'DNS:youtube.com',
                      'DNS:*.youtube.com',
                      'DNS:youtubeeducation.com',
                      'DNS:*.youtubeeducation.com',
                      'DNS:youtubekids.com',
                      'DNS:*.youtubekids.com',
                      'DNS:yt.be',
                      'DNS:*.yt.be',
                      'DNS:android.clients.google.com',
                      'DNS:developer.android.google.cn',
                      'DNS:developers.android.google.cn',
                      'DNS:source.android.google.cn'],
 'is_valid': True,
 'issuer': {'common_name': 'GTS CA 1C3',
            'country_name': 'US',
            'email': None,
            'organizational_name': 'Google Trust Services LLC',
            'organizational_unit_name': None,
            'state_or_province_name': None},
 'serial_number': 253313921569656977963420505972474990984,
 'signature_algorithm': 'sha256WithRSAEncryption',
 'subject': {'common_name': '*.google.com',
             'country_name': None,
             'email': None,
             'organizational_name': None,
             'organizational_unit_name': None,
             'state_or_province_name': None},
 'valid_from': datetime.datetime(2021, 11, 1, 2, 19, 52),
 'valid_to': datetime.datetime(2022, 1, 24, 2, 19, 51),
 'version': 'v3'}
```

## Changelog:

##### 1.0.0 (8.12.2021)

- New method added: get_fingerprint()
- get_all_info() extended with thumbprint, added params (fp_brief=True, signature_algorithm_brief=True)
- get_signature_algorithm() updated to return full or brief signature info

##### 0.0.12 (30.11.2021)

- example added

##### 0.0.1 (30.11.2021)

- initial commit