from pydantic import BaseModel

"""
ex:
{
  "ppodIntent": {
    "ppodIntentName": "9 digit ISP Name",
    "refCpodIntentName": "9 digit ISP Name",
    "refBuhmName": "Philadelphia",
    "refHubName": "GAL1",
    "refDaasIntentNames": [
      "9 digit ISP Name"
    ]
  },
  "leafUplink": {
    "leafA": {
      "lag": {
        "ipv4": {
          "local": "string",
          "remote": "string",
          "subnet": "string"
        },
        "ipv6": {
          "local": "string",
          "remote": "string",
          "subnet": "string"
        }
      },
      "ethernetInterfaces": [
        {
          "localInterface": "string",
          "remoteInterface": "string"
        }
      ],
      "remoteHost": "string"
    },
    "leafB": {
      "lag": {
        "ipv4": {
          "local": "string",
          "remote": "string",
          "subnet": "string"
        },
        "ipv6": {
          "local": "string",
          "remote": "string",
          "subnet": "string"
        }
      },
      "ethernetInterfaces": [
        {
          "localInterface": "string",
          "remoteInterface": "string"
        }
      ],
      "remoteHost": "string"
    }
  },
  "dhcpServers": {
    "ipv4": [
      "string"
    ],
    "ipv6": [
      "string"
    ]
  },
  "vault": {
    "cmSharedSecret": {
      "path": "string",
      "lastUpdated": "string"
    },
    "ripKey": {
      "path": "string",
      "lastUpdated": "string"
    }
  },
  "maggConnections": {
    "ethernetInterfaces": [
      {
        "localInterface": "string",
        "remoteInterface": "string"
      }
    ]
  },
  "custIpScopeConfiguration": {
    "vrfIPScopes": {
      "vrf": [
        {
          "vrfType": "",
          "cm_v4_net": [
            "100.75.170.0/26"
          ],
          "cm_v6_net": [
            "2001:558:40a1::/64"
          ]
        },
        {
          "vrfType": "",
          "cpe_v4_net": [
            "68.35.2.0/23",
            "68.35.30.0/23",
            "21.60.9.0/24",
            "21.60.21.0/24"
          ],
          "cpe_v6_net": [
            "2001:558:6032::/64",
            "2603:27c0:8800::/40"
          ]
        }
      ],
      "anIpscopes": {
        "cm_scope_v4_net": [
          "100.75.170.0/26"
        ],
        "cm_scope_v6_net": [
          "2001:558:40a1:e::/64"
        ],
        "cpe_scope_v4_net": [
          "68.35.2.0/23",
          "68.35.30.0/23"
        ],
        "cpe_scope_v6_net": [
          "2001:558:6032:e::/64"
        ],
        "mta_scope_v4_net": [
          "21.60.9.0/24",
          "21.60.21.0/24",
          "21.60.139.0/24"
        ],
        "mta_scope_v6_net": [
          "2001:558:800a:e::/64"
        ],
        "stb_scope_v6_net": [
          "2603:27c0:8800::/40"
        ],
        "resi_pd_scope_v6_net": [
          "2601:7c0:c800::/40"
        ]
      }
    }
  },
  "refScnProfileName": "Partner East"
}
"""


d = {
    "ppodIntent": {
        "ppodIntentName": "9 digit ISP Name",
        "refCpodIntentName": "9 digit ISP Name",
        "refBuhmName": "Philadelphia",
        "refHubName": "GAL1",
        "refDaasIntentNames": ["9 digit ISP Name"],
    },
    "leafUplink": {
        "leafA": {
            "lag": {
                "ipv4": {"local": "string", "remote": "string", "subnet": "string"},
                "ipv6": {"local": "string", "remote": "string", "subnet": "string"},
            },
            "ethernetInterfaces": [
                {"localInterface": "string", "remoteInterface": "string"}
            ],
            "remoteHost": "string",
        },
        "leafB": {
            "lag": {
                "ipv4": {"local": "string", "remote": "string", "subnet": "string"},
                "ipv6": {"local": "string", "remote": "string", "subnet": "string"},
            },
            "ethernetInterfaces": [
                {"localInterface": "string", "remoteInterface": "string"}
            ],
            "remoteHost": "string",
        },
    },
    "dhcpServers": {"ipv4": ["string"], "ipv6": ["string"]},
    "vault": {
        "cmSharedSecret": {"path": "string", "lastUpdated": "string"},
        "ripKey": {"path": "string", "lastUpdated": "string"},
    },
    "maggConnections": {
        "ethernetInterfaces": [
            {"localInterface": "string", "remoteInterface": "string"}
        ]
    },
    "custIpScopeConfiguration": {
        "vrfIPScopes": {
            "vrf": [
                {
                    "vrfType": "",
                    "cm_v4_net": ["100.75.170.0/26"],
                    "cm_v6_net": ["2001:558:40a1::/64"],
                },
                {
                    "vrfType": "",
                    "cpe_v4_net": [
                        "68.35.2.0/23",
                        "68.35.30.0/23",
                        "21.60.9.0/24",
                        "21.60.21.0/24",
                    ],
                    "cpe_v6_net": ["2001:558:6032::/64", "2603:27c0:8800::/40"],
                },
            ],
            "anIpscopes": {
                "cm_scope_v4_net": ["100.75.170.0/26"],
                "cm_scope_v6_net": ["2001:558:40a1:e::/64"],
                "cpe_scope_v4_net": ["68.35.2.0/23", "68.35.30.0/23"],
                "cpe_scope_v6_net": ["2001:558:6032:e::/64"],
                "mta_scope_v4_net": ["21.60.9.0/24", "21.60.21.0/24", "21.60.139.0/24"],
                "mta_scope_v6_net": ["2001:558:800a:e::/64"],
                "stb_scope_v6_net": ["2603:27c0:8800::/40"],
                "resi_pd_scope_v6_net": ["2601:7c0:c800::/40"],
            },
        }
    },
    "refScnProfileName": "Partner East",
}


class PpodIntentBase(BaseModel):
    pass
