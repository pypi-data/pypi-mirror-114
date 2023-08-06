import socket
from typing import Set, Iterable, Optional

import logging
import requests
import requests.packages.urllib3.util.connection as urllib3_cn
from google.cloud import dns
from google.oauth2 import service_account

IPV4_6 = (socket.AddressFamily.AF_INET, socket.AddressFamily.AF_INET6)
IPV4 = (socket.AddressFamily.AF_INET,)
IPV6 = (socket.AddressFamily.AF_INET6,)


def resolve_addresses(dns_name: str, kind: Iterable[socket.AddressFamily] = IPV4_6) -> Set[str]:
    """
    Resolve the addresses associated with a DNS record
    :param dns_name: the DNS record to resolve
    :param kind: an iterable of the types of IP address to return
    :return: a set of IP address strings
    """
    try:
        return set((item[-1][0] for item in socket.getaddrinfo(dns_name, None) if item[0] in kind))
    except socket.gaierror:
        return set()


def my_ip(kind: Iterable[socket.AddressFamily] = IPV4_6, query_host: str = "ifconfig.co") -> Set[str]:
    """
    Uses a service such as https://ifconfig.co/ to resolve the current hosts IP addresses as they appear
    from the internet.
    :param kind: an iterable ot the tyoes of IP address to return
    :param query_host: the host to use for querying
    :return: a set of IP address strings
    """
    ip_addresses = set()
    _allowed_gai_family = urllib3_cn.allowed_gai_family
    for _kind in kind:
        # Temporarily monkey patches urllib3 so that requests uses only the type of IP address requested
        urllib3_cn.allowed_gai_family = lambda: _kind
        ip_addresses.add(requests.get("https://{}/ip".format(query_host)).content.strip().decode())
    urllib3_cn.allowed_gai_family = _allowed_gai_family
    return ip_addresses


def update_dns(logger: logging.Logger, zone_name: str, dns_name: str, ttl: int = 60, force_update: bool = False,
               project_id: Optional[str] = None, credentials: Optional[str] = None):
    """
    Updates a GCP Cloud DNS zone with the host's current IP as it appears from the internet
    :param zone_name: the name of the zone in your GCP project
    :param dns_name: the DNS name, e.g. `www.example.com`, to update
    :param ttl: the ttl of the new record
    :param force_update: if True, the records will be updated even if they are not different
    :param project_id: the GCP project id
    :param credentials: GCP service account credentials dict
    :return: the applied change set
    """

    if not dns_name.endswith("."):
        dns_name = "%s." % dns_name

    addresses = my_ip()
    logger.info("Found these external IP addresses: [%s]" % ", ".join(addresses))

    existing_addresses = resolve_addresses(dns_name)
    logger.info("Found these IP addresses corresponding to domain '%s': [%s]" % (dns_name, ", ".join(existing_addresses)))

    if len(existing_addresses.symmetric_difference(addresses)) == 0 and not force_update:
        logger.info("Exiting early because IP addresses did not change and force_update is not specified.")
        return None

    if credentials is not None:
        logger.info("Service account data is provided specifically. Resolving credentials...")
        credentials = service_account.Credentials.from_service_account_info(credentials)

    client = dns.Client(project = project_id, credentials = credentials)
    zone = client.zone(zone_name)

    ipv4_addresses = set(filter(lambda _ip: len(_ip.split(".")) == 4, addresses))
    ipv6_addresses = addresses - ipv4_addresses

    changes = zone.changes()
    for record in zone.list_resource_record_sets():
        if record.name == dns_name and record.record_type in ("A", "AAAA"):
            changes.delete_record_set(record)
            logger.info("Removed DNS record type %s for domain name '%s'" % (record.record_type, record.name))

    if len(ipv4_addresses) > 0:
        changes.add_record_set(zone.resource_record_set(dns_name, "A", ttl, list(ipv4_addresses)))
        logger.info("Added DNS records type %s for domain name '%s': [%s]" % ("A", dns_name, ", ".join(list(ipv4_addresses))))

    if len(ipv6_addresses) > 0:
        changes.add_record_set(zone.resource_record_set(dns_name, "AAAA", ttl, list(ipv6_addresses)))
        logger.info("Added DNS records type %s for domain name '%s': [%s]" % ("AAAA", dns_name, ", ".join(list(ipv6_addresses))))

    changes.create()
    return changes
