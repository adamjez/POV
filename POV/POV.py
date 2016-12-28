import os
import sys
import json
from football import Football

###################
# Run Information #
###################
#
# ./POV.py -i image_name.png // Loads and Analyze Image
# ./POV.py -v video_name.mp4 // Loads and Analyze video

####################
# Field Parameters #
####################

default_options = {
    "PlayGround": [
        # game_02+
        [85, 15],  # Specifies corner for playground rectangle
        [790, 520]  # Specifies corner for playground rectangle
    ],

    'Lines': {
        'XPos': [105, 273, 438, 605],  # Specifies lines distance in pixels from left
        'Width': 40,  # Width of line in pixels for line segmentations
        'Belongs': [1, 2, 1, 2]  # Specifies who owns players on given line indexed from left to right
    },

    "Goals": {
        "HistoryLength": 5,
        "Gates": [
            [(0, 190), (15, 318)],
            [(690, 185), (705, 315)]
        ],
        "ScoreXPos": [
            295, 355
        ]
    },

    'Players': {
        'Count': [3, 3, 3, 3],  # Specifies players count on each line indexed from left to right
        'Player1Color': (180, 242, 140),  # Color of player 1 dummys in HSV
        'Player2Color': (221, 211, 27)  # Color of player 2 dummys in HSV
    },

    'Dummy': {
        'FeetDetectionTolerance': 1700,  # Bigger value more feet detection with more false alarams
        'DistanceBetween': 145,  # Specifies distance between dummys on lines
        'Height': 40,
        'ColorTolerance': 40,  # Tolerance for segmentation by color
        'Strip': (75, 10)
    },

    'Ball': {
        'HSV': [121, 193, 164],
        'MinContourSize': 10,
        'MinRadius': 9,
    },

    "Touch": {
        "ToleranceDetection": 40,
        "BufferSize": 5
    },
}


################
# MAIN PROGRAM #
################

def dict_merge(a, b, path=None):
    """
    Merges B into A
    Base on http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge
    :param a:
    :param b:
    :param path:
    :return:
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                dict_merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def load_options(inputConfigFile):
    """
    Overrides default options from config file
    :param inputConfigFile:
    :return:
    """
    try:
        with open(inputConfigFile) as config_data:
            custom_cfg = json.load(config_data)
            return dict_merge(default_options, custom_cfg)
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Exception", str(e))
        print("Problem with parsing custom config data", "(" + inputConfigFile + ")", "using default")

    return default_options


if __name__ == "__main__":
    args_count = len(sys.argv)

    if args_count < 3:
        print("Incorrect number of parameters given")
        sys.exit(1)

    inputType = sys.argv[1]
    inputName = sys.argv[2]
    isLooping = args_count >= 4 and sys.argv[3] == "-l"
    inputConfig = os.path.splitext(inputName)[0] + ".json"

    options = load_options(inputConfig)
    football = Football(options)

    if inputType == "-i":
        football.processImage(inputName)
    elif inputType == "-v":
        football.processVideo(inputName, isLooping)
    else:
        print("Unkown parameter given")
        sys.exit(1)
