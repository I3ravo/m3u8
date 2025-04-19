
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PLAYIDTV MPD PLAYER</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0px;
        }

        .jwplayer {
            position: absolute !important;
        }

        .jwplayer.jw-flag-aspect-mode {
            min-height: 100%;
            max-height: 100%;
        }
    </style>
</head>
<body>
    <div id="jwplayerDiv"></div>
    <script src="//content.jwplatform.com/libraries/SAHhwvZq.js"></script>
    <script type="text/javascript">
        // Use the PHP configuration directly within the JavaScript
        var config = {"file":"https://pop5clustera00de07172379a62d6189.hypp.tv:443/PLTV/88888888/224/3221227971/3221227971.mpd?rrsip=web.hypp.tv:443&zoneoffset=0&servicetype=1&icpid=&accounttype=1&limitflux=-1&limitdur=-1&accountinfo=U0v281lovZMLWzqtXjPtYuOXwQCoIQRk449J%2BBUCcawgQY43Tg5eLk6%2BKHkOBbkVv%2FaciHRqnNnDuZfWMEk6l0rcymHBIhx5oJP4jv2fPK0%3D%3A20230206101746%3AUTC%2C1003663983%2C115.164.187.20%2C20230206101746%2Curn:Huawei:liveTV:XTV59922231%2C1003663983%2C-1%2C0%2C1%2C%2C%2C2%2C593%2C%2C%2C2%2C1343117%2C0%2C248412%2C47562943%2C%2C%2C2%2C1%2CEND&GuardEncType=2&it=H4sIAAAAAAAAADWPQU-EMBSE_02PDX2LUA49rdnExKDJolcztI9KttC1ZTfx3wuKc3wz38vMkmD56dEMKEB1rQlDX6raNWh6TfqAinRflVZk_mqjIWERwjj7NroNez8fP1QhC0mkpCLRbe9OAX5Ptrep52QO_9iZ0320bFwe5B1ZwvvEHssYZ_ka8P2Wwh4R3O3VVFU_VE1RriItlu3aIV9WR3wiH-N0RWL3HP0vsC4JmcUV9gLPLSY28y2EP-4lubXND5_xMYT0AAAA&tenantId=6001","drm":{"clearkey":{"keyId":"f7b1d6556850b472f4f683519f4e41f7","key":"1c983e5a03b0f8adde686ef20497e2b4"}}};

        jwplayer("jwplayerDiv").setup({
            file: config.file,
            position: 'bottom',
            autostart: true,
            stretching: "",
            width: "100%",
            type: "dash",
            drm: {
                clearkey: {
                    keyId: config.drm.clearkey.keyId,
                    key: config.drm.clearkey.key
                }
            }
        });
    </script>
</body>

</html>
