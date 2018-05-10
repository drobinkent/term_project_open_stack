


class Disk:
    
    def __init__ (self,driver = None, size = None, name = None ,location = None  ):
        self.size = size
        self.name = name 
        self.location = location
       
    def start_disk (self, driver):
        # #print("Location is ",self.location)
        # self.gce_hdd= driver.create_volume(self.size, self.name, location=self.location, snapshot=None, 
        # image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
        return self.gce_hdd
    
    

    def stop_disk(self, driver) :
        # result = driver.destroy_volume(self.gce_hdd)
        return result
        return 