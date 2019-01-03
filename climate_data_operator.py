from cdo import Cdo
cdo = Cdo()



import ftplib
from ftplib import FTP
import io
from os.path import join
import bz2
server = ftplib.FTP()

# DWD FTP server host name
server = "opendata.dwd.de"

# FTP server path for our files
serverpath = "/weather/nwp/icon-eu/grib/12/u_10m/"
# You don't have to print this, because this command itself prints dir contents 

user = "anonymous"
passwd = "guest@example.com"

ftp = FTP(server)
ftp.login(user, passwd)
ftp.cwd(serverpath)
#server.d11ir()#
path_data = "/media/data/owncloud/code/julian_magnus/J_and_M/grib2/ICON_GLOBAL2WORLD_025_EASY/data/"
path_grid = "/media/data/owncloud/code/julian_magnus/J_and_M/grib2/ICON_GLOBAL2WORLD_025_EASY"

file_grid = join(path_grid,'target_grid_world_025.txt' )
file_weight = join(path_grid, 'weight.nc')
for i,name in enumerate(ftp.nlst()):
	if i > 50000:
		break
	else:
	    # Create byte stream
	    f = io.BytesIO()
	    # Retrieve .bz2 file from ftp server
	    ftp.retrbinary("RETR " + name, f.write)
	    # Decompress .bz2 file
	    decompressed_file = bz2.decompress(f.getvalue())
	    #  write to folder
	    filename = join(path_data,name[:-4])
	    file1 = open(filename, 'wb')
	    file1.write(decompressed_file);

	   # cdo.remap(file_grid, file_weight,\
	    #	input = filename,\
	    #	output = filename[:-5]+'nc', options = '-f nc')
	    cdo.copy(\
	    	input = filename,\
	    	output = filename[:-5]+'nc', options = '-f nc')
	    cdo.merge( input = [filename[:-11]+'U_10M.nc',filename[:-11]+'V_10M.nc'],\
	    	output = filename[:-12]+'.nc')


