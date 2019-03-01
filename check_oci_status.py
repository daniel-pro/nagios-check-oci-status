from ocistatus import oci_status
import argparse



last_update_date = None
services_regions_status = None
incidents = None
opts = None

def init_argparse():
    global opts
    parser = argparse.ArgumentParser(description="Nagios check for Oracle Cloud Infrastructure (OCI)")
    parser.add_argument('--region', help='Filter for a specific region.', required=False)
    parser.add_argument('--service', help='Filter for a specific service.', required=False)
    opts = parser.parse_args()
    
def init_oci_api():    
    global global_status
    global services_regions_status
    global incidents
    global last_update_date
    
    current_status = oci_status.oci_status(opts.region, opts.service)
    last_update_date, services_regions_status, incidents = current_status.get_data()
    

if __name__ == "__main__":
    init_argparse()
    init_oci_api()
    critical = False
    for srs in services_regions_status:
        if srs['status'] != 'operational':
            print('CRITICAL - %s of %s is %s' % (srs['service'], srs['region'], srs['status']))
            critical = True
        else:
            print('OK - %s of %s is %s ' % (srs['service'], srs['region'], srs['status']))
    if critical:
        exit(2)
    else:
        exit(0)
            
