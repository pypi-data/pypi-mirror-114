# Copyright (C) 2019  Nexedi SA and Contributors.
#                     Romain Courteaud <romain@nexedi.com>
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.

import time
from .db import LogDB
from .configuration import createConfiguration, logConfiguration
from .status import logStatus, reportStatus
from .dns import (
    getReachableResolverList,
    expandDomainList,
    getDomainIpDict,
    reportDnsQuery,
    packDns,
)
from .http import (
    getRootUrl,
    getUrlHostname,
    checkHttpStatus,
    reportHttp,
    packHttp,
)
from .network import isTcpPortOpen, reportNetwork, packNetwork
import json
import email.utils
from collections import OrderedDict
from .ssl import (
    hasValidSSLCertificate,
    reportSslCertificate,
    packSslCertificate,
)
import datetime
from email.utils import parsedate_to_datetime


__version__ = "0.6.0"


class BotError(Exception):
    pass


def rfc822(date):
    return email.utils.format_datetime(date)


def filterWarningStatus(status_dict, interval, not_critical_url_list):
    now = datetime.datetime.utcnow()
    if interval < 60:
        interval = 60
    for i in range(len(status_dict["bot_status"]) - 1, -1, -1):
        status_date = parsedate_to_datetime(
            status_dict["bot_status"][i]["date"]
        )
        if (now - status_date).total_seconds() < (2 * interval):
            # Skip the bot status if it was recently triggerer
            del status_dict["bot_status"][i]
    if not status_dict["bot_status"]:
        del status_dict["bot_status"]

    for i in range(len(status_dict["dns_server"]) - 1, -1, -1):
        state = status_dict["dns_server"][i]["state"]
        if state == "open":
            del status_dict["dns_server"][i]
    if not status_dict["dns_server"]:
        del status_dict["dns_server"]

    for i in range(len(status_dict["dns_query"]) - 1, -1, -1):
        state = status_dict["dns_query"][i]["response"]
        if state != "":
            del status_dict["dns_query"][i]
    if not status_dict["dns_query"]:
        del status_dict["dns_query"]

    if not status_dict["missing_data"]:
        del status_dict["missing_data"]

    for i in range(len(status_dict["http_server"]) - 1, -1, -1):
        state = status_dict["http_server"][i]["state"]
        # Skip if all domains lead to not critical urls
        prefix = ""
        if status_dict["http_server"][i]["port"] == 80:
            prefix = "http://"
        elif status_dict["http_server"][i]["port"] == 443:
            prefix = "https://"
        domain_list = status_dict["http_server"][i]["domain"].split(", ")
        domain_list = [
            x
            for x in domain_list
            if "%s%s" % (prefix, x) not in not_critical_url_list
        ]
        if (state == "open") or (not domain_list):
            del status_dict["http_server"][i]
    if not status_dict["http_server"]:
        del status_dict["http_server"]

    for i in range(len(status_dict["ssl_certificate"]) - 1, -1, -1):
        not_after = status_dict["ssl_certificate"][i]["not_after"]
        if (
            (not_after is not None)
            and (
                (60 * 60 * 24 * 14)
                < (parsedate_to_datetime(not_after) - now).total_seconds()
            )
        ) or (
            ("https://%s" % status_dict["ssl_certificate"][i]["hostname"])
            in not_critical_url_list
        ):
            # Warn 2 weeks before expiration
            # Skip if we check only the http url
            del status_dict["ssl_certificate"][i]
        else:
            # Drop columns with too much info
            del status_dict["ssl_certificate"][i]["not_before"]
            del status_dict["ssl_certificate"][i]["issuer"]
            del status_dict["ssl_certificate"][i]["sha1_fingerprint"]
            del status_dict["ssl_certificate"][i]["subject"]
    if not status_dict["ssl_certificate"]:
        del status_dict["ssl_certificate"]

    for i in range(len(status_dict["http_query"]) - 1, -1, -1):
        http_code = status_dict["http_query"][i]["status_code"]
        if (http_code != 404) and (http_code < 500):
            del status_dict["http_query"][i]
        elif status_dict["http_query"][i]["url"] in not_critical_url_list:
            del status_dict["http_query"][i]
        else:
            # Drop columns with too much info
            del status_dict["http_query"][i]["http_header_dict"]
            del status_dict["http_query"][i]["total_seconds"]
    if not status_dict["http_query"]:
        del status_dict["http_query"]


class WebBot:
    def __init__(self, **kw):
        self.config_kw = kw
        self.config = createConfiguration(**kw)

    def closeDB(self):
        if hasattr(self, "_db"):
            self._db.close()

    def initDB(self):
        self._db = LogDB(self.config["SQLITE"])
        self._db.createTables()

    def calculateUrlList(self):
        return self.config["URL"].split()

    def calculateFullDomainList(self):
        # Calculate the full list of domain to check
        domain_list = self.config["DOMAIN"].split()

        # Extract the list of URL domains
        url_list = self.calculateUrlList()
        for url in url_list:
            domain = getUrlHostname(url)
            if domain is not None:
                domain_list.append(domain)
        domain_list = list(set(domain_list))

        # Expand with all parent domains
        return expandDomainList(
            domain_list,
            public_suffix_list=self.config["PUBLIC_SUFFIX"].split(),
        )

    def calculateNotCriticalUrlList(self):
        domain_list = self.config["DOMAIN"].split()
        url_list = self.config["URL"].split()
        not_critical_url_list = []
        for url in url_list:
            hostname = getUrlHostname(url)
            if hostname is not None:
                if hostname not in domain_list:
                    # Domain not explicitely checked
                    # Skip both root url
                    for protocol in ("http", "https"):
                        not_critical_url = "%s://%s" % (protocol, hostname)
                        if not_critical_url not in url_list:
                            not_critical_url_list.append(not_critical_url)
        return not_critical_url_list

    def iterateLoop(self):
        status_id = logStatus(self._db, "loop")

        if self.config["RELOAD"] == "True":
            self.config = createConfiguration(**self.config_kw)

        timeout = int(self.config["TIMEOUT"])
        elapsed_fast = float(self.config["ELAPSED_FAST"])
        elapsed_moderate = float(self.config["ELAPSED_moderate"])
        # logPlatform(self._db, __version__, status_id)

        # Calculate the resolver list
        resolver_ip_list = getReachableResolverList(
            self._db, status_id, self.config["NAMESERVER"].split(), timeout
        )
        if not resolver_ip_list:
            return

        # Get list of all domains
        domain_list = self.calculateFullDomainList()

        # Get the list of server to check
        # XXX Check DNS expiration
        server_ip_dict = getDomainIpDict(
            self._db, status_id, resolver_ip_list, domain_list, "A", timeout
        )

        # Check TCP port for the list of IP found
        # XXX For now, check http/https only
        server_ip_list = [x for x in server_ip_dict.keys()]
        url_dict = {}
        for server_ip in server_ip_list:
            # XXX Check SSL certificate expiration
            for port, protocol in [(80, "http"), (443, "https")]:
                if isTcpPortOpen(
                    self._db, server_ip, port, status_id, timeout
                ):
                    for hostname in server_ip_dict[server_ip]:
                        if port == 443:
                            # Store certificate information
                            if not hasValidSSLCertificate(
                                self._db,
                                server_ip,
                                port,
                                hostname,
                                status_id,
                                timeout,
                            ):
                                # If certificate is not valid,
                                # no need to do another query
                                continue
                        url = "%s://%s" % (protocol, hostname)
                        if url not in url_dict:
                            url_dict[url] = []
                        url_dict[url].append(server_ip)

        # XXX put back orignal url list
        for url in self.calculateUrlList():
            if url not in url_dict:
                root_url = getRootUrl(url)
                if root_url in url_dict:
                    url_dict[url] = url_dict[root_url]

        # Check HTTP Status
        for url in url_dict:
            for ip in url_dict[url]:
                checkHttpStatus(
                    self._db,
                    status_id,
                    url,
                    ip,
                    __version__,
                    timeout,
                    elapsed_fast,
                    elapsed_moderate,
                )
                # XXX Check location header and check new url recursively
                # XXX Parse HTML, fetch found link, css, js, image
                # XXX Check HTTP Cache

    def status(self):
        result_dict = OrderedDict()

        # Report the bot status
        result_dict["bot_status"] = []
        try:
            bot_status = reportStatus(self._db).get()
        except self._db.Status.DoesNotExist:
            result_dict["bot_status"].append(
                {"text": "", "date": rfc822(datetime.datetime.utcnow())}
            )
        else:
            result_dict["bot_status"].append(
                {"text": bot_status.text, "date": rfc822(bot_status.timestamp)}
            )

        # Report the list of DNS server status
        checked_resolver_ip_dict = {}
        query = reportNetwork(
            self._db,
            port="53",
            transport="UDP",
            ip=self.config["NAMESERVER"].split(),
        )
        resolver_ip_list = []
        result_dict["dns_server"] = []
        for network_change in query.dicts().iterator():
            checked_resolver_ip_dict[network_change["ip"]] = True
            if network_change["state"] == "open":
                resolver_ip_list.append(network_change["ip"])
            result_dict["dns_server"].append(
                {
                    "ip": network_change["ip"],
                    "state": network_change["state"],
                    "date": rfc822(network_change["status"]),
                }
            )

        domain_list = self.calculateFullDomainList()
        checked_domain_dict = {}
        # Report list of DNS query
        query = reportDnsQuery(
            self._db,
            domain=domain_list,
            resolver_ip=resolver_ip_list,
            rdtype="A",
        )
        server_ip_dict = {}
        result_dict["dns_query"] = []
        for dns_change in query.dicts().iterator():
            checked_domain_dict[dns_change["domain"]] = True
            result_dict["dns_query"].append(
                {
                    "domain": dns_change["domain"],
                    "resolver_ip": dns_change["resolver_ip"],
                    "date": rfc822(dns_change["status"]),
                    "response": dns_change["response"],
                }
            )
            for server_ip in dns_change["response"].split(", "):
                if not server_ip:
                    # drop empty response
                    continue
                if server_ip not in server_ip_dict:
                    server_ip_dict[server_ip] = []
                if dns_change["domain"] not in server_ip_dict[server_ip]:
                    server_ip_dict[server_ip].append(dns_change["domain"])

        result_dict["missing_data"] = []
        for resolver_ip in self.config["NAMESERVER"].split():
            if resolver_ip not in checked_resolver_ip_dict:
                result_dict["missing_data"].append(
                    {
                        "text": resolver_ip,
                        "date": result_dict["bot_status"][0]["date"],
                    }
                )
        for domain in domain_list:
            if domain not in checked_domain_dict:
                result_dict["missing_data"].append(
                    {
                        "text": domain,
                        "date": result_dict["bot_status"][0]["date"],
                    }
                )

        # Report the list of CDN status
        query = reportNetwork(
            self._db,
            port=["80", "443"],
            transport="TCP",
            ip=[x for x in server_ip_dict.keys()],
        )
        url_dict = {}
        result_dict["http_server"] = []
        for network_change in query.dicts().iterator():
            result_dict["http_server"].append(
                {
                    "ip": network_change["ip"],
                    "state": network_change["state"],
                    "port": network_change["port"],
                    "date": rfc822(network_change["status"]),
                    "domain": ", ".join(server_ip_dict[network_change["ip"]]),
                }
            )
            if network_change["state"] == "open":
                for hostname in server_ip_dict[network_change["ip"]]:
                    protocol = (
                        "http" if (network_change["port"] == 80) else "https"
                    )
                    url = "%s://%s" % (protocol, hostname)
                    if url not in url_dict:
                        url_dict[url] = []
                    url_dict[url].append(network_change["ip"])

        # Report the SSL status
        result_dict["ssl_certificate"] = []
        for ip_, domain_list_ in server_ip_dict.items():
            query = reportSslCertificate(
                self._db, ip=ip_, port=443, hostname=domain_list_,
            )
            for ssl_certificate in query.dicts().iterator():
                result_dict["ssl_certificate"].append(
                    {
                        "hostname": ssl_certificate["hostname"],
                        "ip": ssl_certificate["ip"],
                        "port": ssl_certificate["port"],
                        "sha1_fingerprint": ssl_certificate[
                            "sha1_fingerprint"
                        ],
                        "subject": ssl_certificate["subject"],
                        "issuer": ssl_certificate["issuer"],
                        "not_before": rfc822(ssl_certificate["not_before"])
                        if (ssl_certificate["not_before"] is not None)
                        else None,
                        "not_after": rfc822(ssl_certificate["not_after"])
                        if (ssl_certificate["not_after"] is not None)
                        else None,
                        "date": rfc822(ssl_certificate["status"]),
                    }
                )

        # XXX put back orignal url list
        for url in self.calculateUrlList():
            if url not in url_dict:
                root_url = getRootUrl(url)
                if root_url in url_dict:
                    url_dict[url] = url_dict[root_url]

        # map IP to URLs for less queries during fetching results
        ip_to_url_dict = {}
        for url, ip_list in url_dict.items():
            for ip in ip_list:
                ip_to_url_dict.setdefault(ip, [])
                if url not in ip_to_url_dict[ip]:
                    ip_to_url_dict[ip].append(url)

        # Get the list of HTTP servers to check
        result_dict["http_query"] = []
        for ip, url_list in ip_to_url_dict.items():
            query = reportHttp(self._db, ip=ip, url=url_list)
            for network_change in query.dicts().iterator():
                result_dict["http_query"].append(
                    {
                        "status_code": network_change["status_code"],
                        "http_header_dict": network_change["http_header_dict"],
                        "total_seconds": network_change["total_seconds"],
                        "url": network_change["url"],
                        "ip": network_change["ip"],
                        "date": rfc822(network_change["status"]),
                    }
                )

        return result_dict

    def stop(self):
        self._running = False
        logStatus(self._db, "stop")

    def crawl(self):
        status_id = logStatus(self._db, "start")
        logConfiguration(self._db, status_id, self.config)

        self._running = True
        try:
            while self._running:
                previous_time = datetime.datetime.utcnow()
                self.iterateLoop()
                next_time = datetime.datetime.utcnow()
                interval = int(self.config.get("INTERVAL"))
                if interval < 0:
                    self.stop()
                else:
                    time.sleep(
                        max(
                            0,
                            interval
                            - (next_time - previous_time).total_seconds(),
                        )
                    )
        except KeyboardInterrupt:
            self.stop()
        except:
            # XXX Put traceback in the log?
            logStatus(self._db, "error")
            raise

    def pack(self):
        logStatus(self._db, "packing")
        packDns(self._db)
        packHttp(self._db)
        packNetwork(self._db)
        packSslCertificate(self._db)
        self._db.vacuum()
        logStatus(self._db, "packed")

    def run(self, mode):
        status_dict = None
        if mode not in ["crawl", "pack", "status", "warning"]:
            raise NotImplementedError("Unexpected mode: %s" % mode)

        if self.config["SQLITE"] == ":memory:":
            # Crawl/report are mandatory when using memory
            if mode == "warning":
                mode = "wallwarning"
            else:
                mode = "all"

        self.initDB()

        try:
            if mode in ["crawl", "wallwarning", "all"]:
                self.crawl()
            if mode in ["status", "all", "wallwarning", "warning"]:
                status_dict = self.status()
            if mode == "pack":
                self.pack()
        except:
            self.closeDB()
            raise
        else:
            self.closeDB()

        if status_dict is not None:
            if mode in ("wallwarning", "warning"):
                filterWarningStatus(
                    status_dict,
                    int(self.config.get("INTERVAL")),
                    self.calculateNotCriticalUrlList(),
                )
            if self.config["FORMAT"] == "json":
                print(json.dumps(status_dict))
            else:
                for table_key in status_dict:
                    print("# %s" % table_key)
                    print("")
                    table = status_dict[table_key]
                    if table:
                        # Print the header
                        table_key_list = [x for x in table[0].keys()]
                        table_key_list.sort()
                        print(" | ".join(table_key_list))
                        for line in table:
                            print(
                                " | ".join(
                                    ["%s" % (line[x]) for x in table_key_list]
                                )
                            )
                        print("")


def create_bot(**kw):
    return WebBot(**kw)
