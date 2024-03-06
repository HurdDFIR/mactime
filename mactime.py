import csv 
from datetime import datetime as dt
from pathlib import Path
from collections import defaultdict
import argparse
import time


class BodyFile:
    def __init__(self, bodyfile, outfile):
        self.bodyfile = Path(bodyfile).resolve()
        self.outfile = Path(outfile).resolve()
        #self.macb = 
        self.mactime()

    def write(self):
        pass 

    def mactime(self):
        
        with open(self.bodyfile, 'r', encoding='utf-8') as bodyfile:
            with open(self.outfile, 'w', encoding='utf-8', newline='') as csvfile:
                fieldnames = ["MD5","name","inode","mode_as_string","UID","GID","size","atime","mtime","ctime","crtime"]
                mactime_fieldnames = ["TimestampUTC","Size","ActivityType","UnixPermissions","UID","GID","inode","Name"]
                writer = csv.DictWriter(csvfile, fieldnames=mactime_fieldnames)
                writer.writeheader()

                for line in bodyfile:
                    line_list = line.replace('\ufeff','').replace('\n','').split("|")
                    line_dict = {}

                    i = 0 
                    for field in fieldnames:
                        if i <= len(line_list):
                            line_dict[field] = line_list[i]
                        i += 1
                    
                    mactime_atime = { "TimestampUTC": line_dict['atime'],"Size": line_dict['size'],"ActivityType": ".a..","UnixPermissions": line_dict['mode_as_string'],"UID": line_dict['UID'],"GID": line_dict['GID'],"inode": line_dict['inode'],"Name": line_dict['name'] }
                    mactime_mtime = { "TimestampUTC": line_dict['mtime'],"Size": line_dict['size'],"ActivityType": "m...","UnixPermissions": line_dict['mode_as_string'],"UID": line_dict['UID'],"GID": line_dict['GID'],"inode": line_dict['inode'],"Name": line_dict['name'] }
                    mactime_ctime = { "TimestampUTC": line_dict['ctime'],"Size": line_dict['size'],"ActivityType": "..c.","UnixPermissions": line_dict['mode_as_string'],"UID": line_dict['UID'],"GID": line_dict['GID'],"inode": line_dict['inode'],"Name": line_dict['name'] }
                    mactime_crtime = { "TimestampUTC": line_dict['crtime'],"Size": line_dict['size'],"ActivityType": "...b","UnixPermissions": line_dict['mode_as_string'],"UID": line_dict['UID'],"GID": line_dict['GID'],"inode": line_dict['inode'],"Name": line_dict['name'] }
                    
                    mactime_sorted_list = self._sort_mactime(mactime_atime, mactime_mtime, mactime_ctime, mactime_crtime)

                    for mactime in mactime_sorted_list:
                        writer.writerow(mactime)
       
    def _sort_mactime(self, mactime_atime, mactime_mtime, mactime_ctime, mactime_crtime):
        mactime_list = [
            mactime_atime, 
            mactime_mtime, 
            mactime_ctime, 
            mactime_crtime
        ] 
        
        activity_type = defaultdict(set)
        for mactime in mactime_list:
            activity_type[mactime['TimestampUTC']].add(mactime['ActivityType'])

        temp_results = []
        
        for k, v in activity_type.items():
            str = '....'
            for value in sorted(list(v)):
                if 'm' in value[0]:
                    str = 'm' + str[1:]
                if 'a' in value[1]:
                    str = str[0] + 'a' + str[2:]
                if 'c' in value[2]:
                    str = str[0:2] + 'c' + str[3]
                if 'b' in value[3]:
                    str = str[0:3] + 'b'

            temp_results.append({ 'TimestampUTC': k, 'ActivityType': str })

        results = []
        for result in temp_results:
            result = { "TimestampUTC": self._convert_timestamp(result['TimestampUTC']),"Size": mactime_atime['Size'],"ActivityType": result['ActivityType'],"UnixPermissions": mactime_atime['UnixPermissions'],"UID": mactime_atime['UID'],"GID": mactime_atime['GID'],"inode": mactime_atime['inode'],"Name": mactime_atime['Name'] }
            results.append(result)
        
        return results

    def _convert_timestamp(self, timestamp):
        return dt.fromtimestamp(int(timestamp))
    
def main():
    __version__ = '1.0.0'
    __author__ = 'Stephen Hurd | @HurdDFIR'
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='mactime is a tool that will convert the standard bodyfile format into a mactime formatted timeline (as csv).',
        epilog=f'v{__version__} | Author: {__author__}')
    parser.add_argument('-f', dest='body_file', action='store', type=str, default=None, required=True,
                        help='Bodyfile to process.')
    parser.add_argument('-o', dest='outfile', action='store', type=str, default=None, required=True,
                        help='File to save the output results to.')
    args = parser.parse_args()
    
    start = time.perf_counter()

    BodyFile(bodyfile=args.body_file, outfile=args.outfile)

    stop = time.perf_counter()
    print(f"mactime took {stop - start:0.6f} seconds")

if __name__ == "__main__":
    main()
