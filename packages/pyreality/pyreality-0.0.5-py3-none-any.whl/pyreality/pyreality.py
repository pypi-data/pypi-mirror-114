import requests
import pandas as pd
import qrcode
from IPython.display import IFrame

def pyRealityBar(df, title, encodingX, encodingY, encodingZ, encodingColor):
    dfList = df.to_dict(orient='records')
    payload = {
        "name": title,
        "config": {
            "title": title,
            "data": { "values": dfList },
            "mark": "bar",
            "encoding": {
                "x": encodingX,
                "y": encodingY,
                "z": encodingZ,
                "color": encodingColor 
            },
            "y": 0.2,
            "z": -0.5,
            "yrotation": 45
        }
    }
    endpoint = "https://pyreality.herokuapp.com/api/vis"
    response = requests.post(endpoint, json=payload).json()
    visurl = 'https://pyreality.herokuapp.com/mr/output/'+response['slug']
    visqr = qrcode.make(visurl)
    return IFrame(visurl, width='100%', height=550)

def pyRealityScatter(df, title, encodingX, encodingY, encodingZ, encodingColor):
    dfList = df.to_dict(orient='records')
    payload = {
        "name": title,
        "config": {
            "title": title,
            "data": { "values": dfList },
            "mark": "point",
            "encoding": {
                "x": encodingX,
                "y": encodingY,
                "z": encodingZ,
                "color": encodingColor 
            },
          "width": 0.5,
          "height": 0.5,
          "depth": 0.5,
          "x": 0.25,
          "y": 0.2,
          "z": -0.25
        }
    }
    endpoint = "https://pyreality.herokuapp.com/api/vis"
    response = requests.post(endpoint, json=payload).json()
    visurl = 'https://pyreality.herokuapp.com/mr/output/'+response['slug']
    visqr = qrcode.make(visurl)
    return IFrame(visurl, width='100%', height=550)

def pyRealityImmersiveScatter(df, title, encodingColor, size = 2):
    dfList = df.to_dict(orient='records')
    payload = {
        "name": title,
        "config": {
            "data": dfList,
            "color": encodingColor,
            "size": size
        }
    }
    endpoint = "https://pyreality.herokuapp.com/api/vis"
    response = requests.post(endpoint, json=payload).json()
    visurl = 'https://pyreality.herokuapp.com/mr/plotoutput/'+response['slug']
    visqr = qrcode.make(visurl)
    return IFrame(visurl, width='100%', height=550)
    # return response

def pyRealityPlot(config):
    payload = {
        "name": config['title'],
        "config": config
    }
    endpoint = "https://pyreality.herokuapp.com/api/vis"
    response = requests.post(endpoint, json=payload).json()
    visurl = 'https://pyreality.herokuapp.com/mr/output/'+response['slug']
    visqr = qrcode.make(visurl)
    return IFrame(visurl, width='100%', height=550)

if __name__ == "__main__": 
    pyRealityBar()
    pyRealityScatter()
    pyRealityImmersiveScatter()
    pyRealityPlot()