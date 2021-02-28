import numpy as np
from config import Config

class MapGrid:
    """
    This class stores the rotation logic.
    If ll, ul, lr and ur are input the city boundaries  dict is not used for construction.
    """
    def __init__(self, city, city_boundaries, x_grid_count, y_grid_count, ll=None, ul=None, lr=None, ur=None):
        self.city = city
        self.x_grid_count = x_grid_count
        self.y_grid_count = y_grid_count

        if city:
            self.ll = np.matrix(city_boundaries[city]['ll'])
            self.lr = np.matrix(city_boundaries[city]['lr'])
            self.ul = np.matrix(city_boundaries[city]['ul'])
            self.ur = np.matrix(city_boundaries[city]['ur'])
        else:
            self.ll = np.matrix(ll)
            self.lr = np.matrix(lr)
            self.ul = np.matrix(ul)
            self.ur = np.matrix(ur)

        self.centerx = (self.lr[0,0] + self.ul[0,0]) / 2
        self.centery = (self.lr[0,1] + self.ul[0,1]) / 2
        self.ll_c = self.ll - np.matrix([[self.centerx, self.centery]])
        self.ul_c = self.ul - np.matrix([[self.centerx, self.centery]])
        self.ur_c = self.ur - np.matrix([[self.centerx, self.centery]])
        self.lr_c = self.lr - np.matrix([[self.centerx, self.centery]])

        self.theta = np.arctan(abs(self.ll_c[0,1] - self.lr_c[0,1]) / abs(self.ll_c[0,0] - self.lr_c[0,0]))
        self.cos_theta = np.cos(self.theta)
        self.sin_theta = np.sin(self.theta)
        self.rot_matrix = np.matrix([[self.cos_theta, -self.sin_theta],
                                     [self.sin_theta, self.cos_theta]])
        self.reverse_rot_matrix = np.matrix([[self.cos_theta, self.sin_theta],
                                             [-self.sin_theta, self.cos_theta]])

        self.ur_norm = self.rot_matrix @ self.ur_c.T
        self.ul_norm = self.rot_matrix @ self.ul_c.T
        self.ll_norm = self.rot_matrix @ self.ll_c.T
        self.lr_norm = self.rot_matrix @ self.lr_c.T
        #self.ul_norm[0,0], self.ll_norm[0,0] = -0.034, -0.034
        #self.lr_norm[0,0], self.ur_norm[0,0] = 0.034, 0.034
        self.x_dist = 2 * (self.lr_norm[0, 0])
        self.y_dist = 2 * (self.ul_norm[1, 0])

    def get_grid(self, lon, lat):
        """

        :param lon: longitude - float
        :param lat: latitude - float
        :return: locations in the grid for the lon lat pair as non-negative integers. (xgrid, ygrid), if grid not within
                 scope returns None.
        """
        lon_norm = (lon - self.centerx) * self.rot_matrix[0, 0] + (lat - self.centery) * self.rot_matrix[0, 1]
        lat_norm = (lon - self.centerx) * self.rot_matrix[1, 0] + (lat - self.centery) * self.rot_matrix[1, 1]
        gridx = np.floor(((lon_norm - self.ll_norm[0,0]) / self.x_dist) * self.x_grid_count)
        gridy = np.floor(((lat_norm - self.ll_norm[1,0]) / self.y_dist) * self.y_grid_count)
        if gridx < 0 or gridx >= self.x_grid_count or gridy < 0 or gridy >= self.y_grid_count:
            return None
        return (gridx, gridy)

    def get_grid_center(self, gridx, gridy):
        """

        :param gridx: (0 - (x_grid_count -1))
        :param gridy: (0 - (y_grid_count -1))
        :return: (lat, lon)
        """
        lon_norm = (gridx + 0.5) * self.x_dist / self.x_grid_count -  self.x_dist / 2
        lat_norm = (gridy + 0.5) * self.y_dist / self.y_grid_count -  self.y_dist / 2
        coord =   np.matrix([[lon_norm, lat_norm]]) @ self.rot_matrix + np.matrix([[ self.centerx,  self.centery]])
        return (coord[0, 0], coord[0, 1])

def main():
    m = MapGrid(Config.city, Config.city_boundaries, Config.mapsize, Config.mapsize)
    print(m.get_grid_center(0, 0))
    print(m.get_grid(-87.732081736, 41.9536468999999))
    #print(m.theta)
    #print(m.cos_theta)
    #print(m.rot_matrix)

if __name__ == '__main__':
    main()