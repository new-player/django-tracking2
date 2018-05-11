import os
import gzip
import urllib
import urlparse

from django.core.management.base import BaseCommand, CommandError
import tracking

download_folder = tracking.geoip_data_download_location()


class Command(BaseCommand):
    help = 'Updates GeoIP data in %s' % download_folder
    base_url = 'http://www.maxmind.com/download/geoip/database/'
    files = ['GeoLiteCity.dat.gz', 'GeoLiteCountry/GeoIP.dat.gz']

    def handle(self, *args, **options):
        try:
            self.stdout.write('Creating path %s ...\n' % (download_folder,))
            os.makedirs(download_folder)
        except OSError:
            if not os.path.isdir(download_folder):
                raise
            else:
                self.stdout.write('Path %s already created.\n' % (download_folder,))

        for path in self.files:
            root, filepath = os.path.split(path)
            dowloadpath = os.path.join(download_folder, filepath)
            downloadurl = urlparse.urljoin(self.base_url, path)
            self.stdout.write('Downloading %s to %s\n' % (downloadurl, dowloadpath))
            urllib.urlretrieve(downloadurl, dowloadpath)
            outfilepath, ext = os.path.splitext(dowloadpath)
            if ext != '.gz':
                raise CommandError('Something went wrong while '
                                   'decompressing %s' % dowloadpath)
            self.stdout.write('Extracting %s to %s\n' % (dowloadpath, outfilepath))
            infile = gzip.open(dowloadpath, 'rb')
            outfile = open(outfilepath, 'wb')
            try:
                outfile.writelines(infile)
            finally:
                infile.close()
                outfile.close()
            self.stdout.write('Deleting %s\n' % dowloadpath)
            os.remove(dowloadpath)
            self.stdout.write('Done with %s' % path)
