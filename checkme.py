#import pkg_resources
#print(pkg_resources.resource_filename('workstation', 'data/'))
import glob
print(glob.glob('config/.next/*'))
