#!/usr/bin/env python

import sys
import argparse
import boto
import dns.resolver

def main():
    parser = argparse.ArgumentParser(description='dnscheck - checks Route 53 configuration')
    parser.add_argument('--rr', dest="rr")
    parser.add_argument('hosted_zone_id')
    args = parser.parse_args()

    hosted_zone_id = args.hosted_zone_id
    conn = boto.connect_route53()
    try:
        response = conn.get_hosted_zone(hosted_zone_id)['GetHostedZoneResponse']
    except boto.route53.exception.DNSServerError:
        print >> sys.stderr, 'Hosted zone with the given ID does not exist'
        sys.exit(-1)

    hosted_zone = response['HostedZone']
    delegation_set = set(response['DelegationSet']['NameServers'])

    if args.rr is None:
        check_delegation(hosted_zone, delegation_set)
        # TODO: also validate NS and SOA records
    else:
        check_record(hosted_zone, args.rr)

def check_record(hosted_zone, resource_record):
    # TODO: validation checks for resource records
    return

def check_delegation(hosted_zone, delegation_set):
    domain_name = hosted_zone['Name']
    answers = dns.resolver.query(domain_name, 'NS')
    delegated_set = set()
    for rdata in answers:
        delegated_set.add(rdata.target.to_unicode(omit_final_dot=True))

    if delegation_set != delegated_set:
        print "Your domain has not been delegated correctly to Route 53 DNS servers.\n" \
            + "Please check whether your domain registrar has the correct DNS servers.\n" \
            + "Current name servers: " + ", ".join(delegated_set) + "\n" \
            + "Route 53 name servers: " + ", ".join(delegation_set) + "\n"
    else:
        print "Domain %s has been delegated correctly to Route 53." % (domain_name)
    return

if __name__ == '__main__':
    main()