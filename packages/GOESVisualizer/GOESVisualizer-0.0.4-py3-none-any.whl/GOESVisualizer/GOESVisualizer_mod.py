# UTF-8
# Visualize GEOS16 (west+east) RGB (true) color for a given
# time and location
# Amir Souri (ahsouri@cfa.harvard.edu;ahsouri@gmail.com)
# July 2021


class GSVis(object):

    def __init__(self,eastorwest,year,month,day,hour,lon1,lon2,lat1,lat2,gamma):
            '''
            Initializing GSVis with the primary inputs
            ARGS: 
                eastorwest (char): 'east' or 'west' GEOS16/17
                year (int): year
                month (int): month
                day (int): day
                hour (int): hour
                lon1,lon2 (float): boundary longitudes (degree) lon2>lon1
                lat1,lat2 (float): boundary latitudes (degree) lat2>lat1
                gamma (float) : a gamma correction for brightness, for dark scenes
                                I recommend 2.5-3, for bright scenes, 1-2
                                
            '''   
            import xarray as xr
            import numpy as np
            import cv2
            from datetime import timedelta,datetime,date
            import requests
            import netCDF4
            import boto3
            import metpy
            from botocore import UNSIGNED
            from botocore.config import Config
            #preparing for the amazon cloud connection
            s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
            # east or west
            if eastorwest == 'east':
                bucket_name = 'noaa-goes16'
                self.sat = 'GOES16'
            elif eastorwest == 'west':
                bucket_name = 'noaa-goes17'
                self.sat = 'GOES17'
            else:
                print('the current program only supports east or west.')
                exit()
            # RGB colors are bands 2, 3 and 1
            Bands = [2,3,1]
            # converting date to doy
            day_of_year = date(year, month, day).timetuple().tm_yday
            # radiance product name
            product_name = 'ABI-L1b-RadC'
            Rads = []
            for band in Bands:
                # getting the data from the bucket
                fkeys = self.get_s3_keys(bucket_name,s3_client, \
                        prefix = f'{product_name}/{year}/{day_of_year:03.0f}/{hour:02.0f}/OR_{product_name}-M6C{band:02.0f}')
                key = [key for key in fkeys][0] 
                resp = requests.get(f'https://{bucket_name}.s3.amazonaws.com/{key}')
 
                fname = key.split('/')[-1].split('.')[0]
                # opening
                nc4_data = netCDF4.Dataset(fname, memory = resp.content)
                rad = nc4_data.variables['Rad'][:]
                # normalization
                Rads.append(cv2.normalize(rad,np.zeros(rad.shape, np.double),1.0,0.0,cv2.NORM_MINMAX))
                timesec = nc4_data.variables['t'][:]
                timesec = np.array(timesec)
                #seconds since 2000-01-01 12:00:00
                goesdate = datetime(2000,1,1,12,0,0) + timedelta(seconds=float(timesec))
                if band == 1:
                   '''
                   the red band (band == 2) has a different spatial resolution (500 m)
                   compared to others, so we'll take crs and x,y coordinates from the blue band
                   the red band will be resized later on.
                   '''
                   interm = xr.backends.NetCDF4DataStore(nc4_data)
                   interm = xr.open_dataset(interm)
                   interm = interm.metpy.parse_cf('Rad')
                   crs = interm.metpy.cartopy_crs
                   x = interm.x
                   y = interm.y
                # closing the file
                nc4_data.close()
            # sorting RGB
            R = np.power(np.array(Rads[0]),1/gamma)
            G = np.power(np.array(Rads[1]),1/gamma)
            B = np.power(np.array(Rads[2]),1/gamma)
            # upscaling the R band
            R = cv2.resize(R, dsize=(G.shape[1], G.shape[0]), interpolation=cv2.INTER_CUBIC)
            # apply an adaptive histogram eq to enhance the image contrast
            clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (100,100))
            R = clahe.apply(np.uint8(R*255))
            G = clahe.apply(np.uint8(G*255))
            B = clahe.apply(np.uint8(B*255))
            # cashing other variables
            self.RGB = np.dstack([R,G,B])
            self.goesdate = goesdate
            self.crs = crs
            self.x = x
            self.y = y
            self.lat1 = lat1
            self.lat2 = lat2
            self.lon1 = lon1
            self.lon2 = lon2

    def plotGS(self,is_save=False,fpng=None):
        '''
        Plotting GOES RGB image
        ARGS:
            is_save (bool): whether we should save it as a png file (True)
                            or plot it (False)
            fpng (char): file.png
        ''' 
        import matplotlib.pyplot as plt
        import cartopy.crs as ccrs
        import numpy as np
        # plate projection at the desired box
        pc = ccrs.PlateCarree()
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1, projection = pc)
        ax.set_extent([self.lon1, self.lon2, self.lat1, self.lat2], crs = pc)
        # plotting GEOS
        ax.imshow(self.RGB, origin='upper',
            extent=(self.x.min(), self.x.max(), self.y.min(), self.y.max()),
            transform=self.crs,
            interpolation='none',
        )
        # plotting costlines
        ax.coastlines(resolution='50m', color='black', linewidth = 2)
        ax.add_feature(ccrs.cartopy.feature.STATES)
        # plotting title
        plt.title(self.sat + ' True Color', loc='left', fontweight='bold', fontsize=16)
        plt.title('{}'.format(self.goesdate.strftime('%d %B %Y %H:%M UTC ')), loc='right')
        # if show or save
        if is_save:
           fig.savefig(fpng, format='png', dpi=300)
        else:
            plt.show()

    def get_s3_keys(self, bucket, s3_client, prefix = ''):
        '''
        Generate the keys in an S3 bucket.
        ARGS:
             param bucket: Name of the S3 bucket.
             param prefix: Only fetch keys that start with this prefix (optional).
             source: https://github.com/HamedAlemo/visualize-goes16
        '''
        
        kwargs = {'Bucket': bucket}

        if isinstance(prefix, str):
           kwargs['Prefix'] = prefix

        while True:
            resp = s3_client.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
               key = obj['Key']
               if key.startswith(prefix):
                  yield key

            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
               break


