#a class which stores all variable parameters for the model
class Config:

    city = 'chicago'  # string, which city to analyse from bounding box object
    mapsize = 'all_sizes'  # int, how many cells each axis of grid should have

    org_data = "Traffic_Crashes_-_Crashes Chicago.csv"
    clean_data = "chicago_crashes_cleaned_{}.csv".format(mapsize)
    data_folder = "data"

    #bounding box approximated with google maps [longitude, latitude]
    city_boundaries = {'chicago': {'ll': [-87.844455, 41.644586],
                                   'ul': [-87.844455, 42.016928],
                                   'ur': [-87.519110, 42.016928],
                                   'lr': [-87.519110, 41.644586]
                       },
            'chicago_not_working': {'ll': [-87.665359, 41.627714],
                                    'ul': [-87.82447, 41.971462],
                                    'ur': [-87.669784, 42.043062],
                                    'lr': [-87.510672, 41.699314]
                                    },
                       #add new cities here
                       }