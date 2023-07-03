
DIM_LOGIN_CAM = (200, 150)
DIM_CAM = (640, 480)

from PyQt5.QtGui import QFont
CUSTOM_FONT = QFont("Poppins")


class CSS:
    score_item_label = """
        padding: 5px; 
        border-style: none; 
        font-size:18px; 
        font-weight: bold;
    """

    score_value_label = """
        padding: 5px; 
        font-size:18px; 
        border-style: none;
    """

    card_div = """
        background-color: #1E1E1E; 
        color: white; 
        border-radius: 9px; 
        padding: 5px; 
        border: 2px solid #2fa572;
    """

    card_header = """
        background-color: #2fa572; 
        color: white; 
        border-top-left-radius: 9px; 
        border-top-right-radius: 9px; 
        border-bottom-left-radius: 0px; 
        border-bottom-right-radius: 0px; 
        padding-top: 20px;
        padding-bottom: 20px;
        max-height: 80px;
        border-style: none;
        font-size: 16px;
        font-weight: bold;
        qproperty-alignment: 'AlignVCenter | AlignHCenter';
    """

    canvas ="""
        border: 2px solid #2fa572;
        border-radius: 9px;
    """

    danger_btn = """
        QPushButton {
            /*height: 15px;*/
            border: none;
            padding: 5px 10px;
            background-color: #A52F2F;
            color: #fff;
        }
        QPushButton:hover {
            border-style: solid;
            border-width: 1px;
            border-color: #A52F2F;
            background-color: #371F1F;
        }
    """

    disabled_btn ="""
        QPushButton {
            border: none;
            padding: 5px 10px;
            background-color: #375447;
            color: white;
        }
    """

    btn = """
        QPushButton {
            border: none;
            padding: 5px 10px;
            background-color: #2fb572;
            color: white;
        }
        QPushButton:hover {
            border-style: solid;
            border-width: 1px;
            border-color: #2fa572;
            background-color: #1f372d;
            color: #2fa572;
        }
    """