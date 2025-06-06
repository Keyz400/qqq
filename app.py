import os
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Greeting (Resource):
    def get(self):
        return "Bot is Up & Running!"

api.add_resource(Greeting, '/')
app.run(host="0.0.0.0", port=os.environ.get("PORT", 7860))


# from flask import Flask, request

# app = Flask(__name__)

# rawhtml = """
# <html>
#   <head>
#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Play Videos via Links</title>
#     <link rel="icon" href="https://i.slow.pics/vBpClAQI.webp">
#     <link rel="stylesheet" href="https://cdn.plyr.io/3.7.3/plyr.css" />
#     <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous" />
#     <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
#     <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
#     <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
#     <style>
#         .button-85 {
#           padding: 0.6em 2em;
#           border: none;
#           outline: none;
#           color: rgb(255, 255, 255);
#           background: #111;
#           cursor: pointer;
#           position: relative;
#           z-index: 0;
#           border-radius: 10px;
#           user-select: none;
#         }

#         .button-85:before {
#           content: "";
#           background: linear-gradient(
#             45deg,
#             #ff0000,
#             #ff7300,
#             #fffb00,
#             #48ff00,
#             #00ffd5,
#             #002bff,
#             #7a00ff,
#             #ff00c8,
#             #ff0000
#           );
#           position: absolute;
#           top: -2px;
#           left: -2px;
#           background-size: 400%;
#           z-index: -1;
#           filter: blur(5px);
#           -webkit-filter: blur(5px);
#           width: calc(100% + 4px);
#           height: calc(100% + 4px);
#           animation: glowing-button-85 20s linear infinite;
#           transition: opacity 0.3s ease-in-out;
#           border-radius: 10px;
#         }

#         @keyframes glowing-button-85 {
#           0% {
#             background-position: 0 0;
#           }
#           50% {
#             background-position: 400% 0;
#           }
#           100% {
#             background-position: 0 0;
#           }
#         }

#         .button-85:after {
#           z-index: -1;
#           content: "";
#           position: absolute;
#           width: 100%;
#           height: 100%;
#           background: #222;
#           left: 0;
#           top: 0;
#           border-radius: 10px;
#         }
#     </style>
#   </head>
#   <body style = "background-color: black;">
#     <div class = "container-fluid">
#         <div class = "row">
#             <div style="background-color: #19232d;" class = "col-12 fixed-top">
#                 <h1 class = "text-center p-3" style = "color: yellow;background-color: #19232d; font-weight: bold;">
#                     𝚁𝚞𝚜𝚑𝚒𝚍𝚑𝚊𝚛
#                 </h1>
#             </div>
#             <div class = "col-12 p-5" style = "background-color: black;"></div>
#             <div class = "col-12 mt-5 mb-5">
#                 <video id="player" playsinline controls data-poster="https://cdn.jsdelivr.net/npm/@googledrive/index@2.2.3/images/poster.jpg">
#                   <source src="{video_url}" type="video/mp4">
#                   <source src="{video_url}" type="video/webm">
#                 </video>
#                 <script src="https://cdn.plyr.io/3.7.3/plyr.js"></script>
#                 <script>const player = new Plyr('#player');</script>
#             </div>
#             <div class = "col-12 text-center">
#                 <button class="button-85 mb-3 mt-3" role="button">
#                     <a href="{video_url}" style = "text-decoration: none; color: yellow;font-weight: bold;font-size: 20px;">
#                         Download Video
#                     </a>
#                 </button>
#             </div>
#             <div class = "col-12 text-center">
#                 <button class="bg-primary pl-2 pr-2 pt-1 pb-1 m-2 shadow" style = "border-radius :50px; border-width: 0px; width: 220px; height: 60px;" width = "200px">
#                     <a href="intent:{video_url}#Intent;package=com.mxtech.videoplayer.ad;end">
#                         <img src="https://i.slow.pics/qeem0Xni.png" alt="mx_logo" width="150px">
#                     </a>
#                 </button>
#             </div>
#             <div class = "col-12 text-center">
#                 <button class="pl-2 pr-2 pt-1 pb-1 m-2" style = "border-radius :50px; border-width: 0px; width: 220px; height: 60px; background-color: #7400FF;">
#                     <a href="intent:{video_url}#Intent;package=org.videolan.vlc;end">
#                         <img src="https://i.slow.pics/lP6ygVnl.png" alt="vlc_logo" width="100px" height="40px"/>
#                     </a>
#                 </button>
#             </div>
#             <div class = "col-12 text-center">
#                 <button class="pl-2 pr-2 pt-1 pb-1 m-2" style = "border-radius :50px; border-width: 0px; background-color: lightblue; width: 220px; height: 60px;">
#                     <a href="intent:{video_url}#Intent;action=com.young.simple.player.playback_online;package=com.young.simple.player;end">
#                         <img src="https://i.slow.pics/ZKTgV9HV.png" alt="s_player_logo" width="170px">
#                     </a>
#                 </button>
#             </div>
#             <div class = "col-12 text-center">
#                 <button class="bg-warning pl-2 pr-2 pt-1 pb-1 m-2" style = "border-radius :50px; border-width: 0px; width: 220px; height: 60px;">
#                     <a href="intent:{video_url}#Intent;package=com.playit.videoplayer;end">
#                         <img src="https://i.slow.pics/c0C4vnAa.png" alt="playit_logo" width="170px">
#                     </a>
#                 </button>
#             </div>
#             <div class = "col-12 p-5" style = "background-color: black;"></div>
#             <div style="background-color: #19232d;" class = "col-12 p-2 fixed-bottom">
#                 <p class = "text-center" style = "color: white; font-size: 20px;">
#                 Made with plyr
#                 </p>
#             </div>
#         </div>
#     </div>
#   </body>
# </html>
# """

# @app.route('/stream')
# def player():
#   vid_url = request.args.get('url')
#   return rawhtml.replace("{video_url}", f"{vid_url}")

# @app.route('/')
# def hello_world():
#     return "<h1>Site Running</h1>"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=os.environ.get("PORT", 7860))
