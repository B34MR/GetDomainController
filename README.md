![Supported Python versions](https://img.shields.io/badge/python-3.7-green.svg)

# GetDomainController
A python utility that leverages DNS to quickly discover windows domain controllers and exchange servers.

**Installation:**

    git clone https://github.com/NickSanzotta/GetDomainController.git
    pip install -r requirements.txt
    
**Menu:**
```
Usage:
  python getdc.py -d contoso.local
  python getdc.py -d contoso-a.local constoso-b.local
  python getdc.py -d contoso.local -n 8.8.8.8
  python getdc.py -d contoso.local -f host
  python getdc.py -d contoso.local -e

Required arguments:
  [-d, --domain] define domain, accepted values 'hostname', 'hostnames(seperate by a space)'

Optional arguments:
  [-n, --nameserver] define nameserver, accepted values 'hostname', 'ipaddress'
  [-f, --format] format output type, accepted values 'json(default)', 'host', 'ip', 'hostip', 'zerologon'
  [-v, --verbose] toggle debug meesages to stdout
  [-e, --exchange] additionally retrieve exchange hosts
```

**JSON Format (Domain Controller):**
```
# python getdc.py -d contoso.local
{
    "contoso.local": {
        "ad1.contoso.local.": "10.1.100.10",
        "ad2.contoso.lcoal.": "10.1.200.10",
        "ad3.contoso.local.": "10.1.300.10"
    }
}
```

**JSON Multi-Domain Format (Domain Controller):**
```
# python getdc.py -d contoso-a.local contoso-b.local
{
    "contoso-a.local": {
        "ad1.contoso-a.local.": "10.1.100.10",
        "ad2.contoso-a.lcoal.": "10.1.200.10",
        "ad3.contoso-a.local.": "10.1.300.10"
    },
    "contoso-b.local": {
        "ad1.contoso-b.local.": "10.2.100.10",
        "ad2.contoso-b.lcoal.": "10.2.200.10",
        "ad3.contoso-b.local.": "10.2.300.10"
    }
}
```

**JSON Format (Exchange Server):**
```
# python getdc.py -d contoso.local -e
{
    "contoso.local": {
        "autodiscover.contoso.local.": "10.1.100.150"
    }
}
```

**Hostname Format:**
```
# python getdc.py -d contoso.local -f host
ad1.contoso.local.
ad2.contoso.lcoal.
ad3.contoso.local.
```

**IP Address Format:**
```
# python getdc.py -d contoso.local -f ip
10.1.100.10
10.1.200.10
10.1.300.10
```

**Hostname + IP Address Format:**
```
# python getdc.py -d contoso.local -f hostip
ad1.contoso.local. 10.1.100.10
ad2.contoso.lcoal. 10.1.200.10
ad3.contoso.local. 10.1.300.10
```

**Zerologon Format:**
```
# python getdc.py -d contoso.local -f zerologon
ad1 10.1.100.10
ad2 10.1.200.10
ad3 10.1.300.10
```