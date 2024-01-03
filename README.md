# py-adspower

py-adspower library implements AdsPower API specification. You can read the documentation 
in detail at the [link](https://localapi-doc-en.adspower.com/docs/overview).

Usage example:

```
import os

from adspower import AdsPower
from adspower.errors import ProfileLimitReached
from adspower.models import ProxyConfig, FingerprintConfig

adspower = AdsPower()

group_info = adspower.query_group_info(group_name="MyGroup")

try:
    profile_name = "MyProfile"
    user_id = adspower.create_profile(
        name=profile_name, 
        group_id=group_info.group_id,
        user_proxy_config=ProxyConfig.default(),
        fingerprint_config=FingerprintConfig.default()
    )
except ProfileLimitReached:
    print("Failed to create new profile!")
    os.exit(0)

profile_info = adspower.query_profile_info_by_name(profile_name)
print(f"IP address of {profile_info.user_id} is {profile_info.ip}")
```

---

Warning! This library is under development. Use it at your own risk!
Also I will be glad to receive any suggestions for improvement.