# Записки

TCP port 49 - encrypts all, authentication on author

## Firewalls
packer filter - access control принцип, така наречения прост firewall тип, на 4ти слой от OSI модела (транспортен)

proxy - app - взимате се под внимание информацията, а не само Source / Destination IP или порт, повече ресурси

stateless inspection (static packet filtering) - подобен на Transmission Control Protocol (TCP) and similar protocols, може да поддържа и UDP

stateful inspection (dynamic packet filtering) -  следи състоянието на активните връзки и използва тази информация, за да определи кои мрежови пакети да допусне през защитната стена, над Data Link слоя

NGFW (New Generation Firewall) - все едно stateful firewall + IRS/IDS и други неща(med filtering, antivirus), identity management (разпознаване на различни хора (роли)), изисква много ресурси

MDZ - има достъп, но той е ограничен и не може ако стане бедствие там да се навреди основната мрежа 

Zone-based Policy Firewall (ZPF) -  changes the firewall from the older interface-based model to a more flexible, more easily understood zone-based configuration model. Interfaces are assigned to zones, and an inspection policy is applied to traffic moving between the zones.


## IP Tables