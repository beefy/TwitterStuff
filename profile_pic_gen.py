import pylab as plt
import numpy as np
from random import randint, choice
from TwitterAPI import TwitterAPI
import json
import base64

def gen_colors():
    # get current colors
    f = open('colors.csv','r')
    colors = f.readlines()[0].strip().split(',')
    colors = [int(color) for color in colors]
    #colors = [randint(0,255) for i in range(4)]
    # change a color
    square = randint(0,3)
    colors[square] = randint(0,255)
    # save colors
    f = open('colors.csv','w')
    f.write(','.join([str(color) for color in colors]))
    f.close()
    # return colors
    return colors

def get_data_from_colors(colors, pic_size):
    full_data = []
    half_pic_size = pic_size/2
    for i in range(pic_size):
        data_row = []
        for y in range(pic_size):
            if i < half_pic_size and y < half_pic_size:
                corner_num = 0
            elif i >= half_pic_size and y < half_pic_size:
                corner_num = 1
            elif i < half_pic_size and y >= half_pic_size:
                corner_num = 2
            elif i >= half_pic_size and y >= half_pic_size:
                corner_num = 3

            data_row.append(colors[corner_num])
        full_data.append(data_row)
    return full_data

# credentials file (cred.csv) format:
# consumer_key, consumer_secret, access_token_key, access_token_secret
def read_credentials():
    f = open('cred.csv','r')
    creds = f.readlines()[0].strip().split(',')
    creds = [cred.strip() for cred in creds]
    return {
        'consumer_key': creds[0],
        'consumer_secret': creds[1],
        'access_token_key': creds[2],
        'access_token_secret': creds[3]
    }

def make_pic():
    colors = gen_colors()
    full_data = get_data_from_colors(colors, 100)
    plt.imshow(full_data)
    plt.xticks([])
    plt.yticks([])
    plt.savefig('pic.png')


make_pic()
creds = read_credentials()
api = TwitterAPI(
        creds['consumer_key'],
        creds['consumer_secret'],
        creds['access_token_key'],
        creds['access_token_secret']
        )

#pic_file = open('pic.png','rb')
#pic_data = pic_file.read()

with open('pic.png','rb') as image_file:
    #encoded_string = base64.b64encode(image_file.read())
    data = image_file.read()
#data = data.encode('base64')

image_dict = {
    'image': 
        {
            'media': data
            #'media_data': data.encode('base64')
        }
}

req = api.request('account/update_profile_image', image_dict)
print req.status_code
print 'SUCCESS' if req.status_code == 200 else 'FAILURE'
print req.response.__dict__
