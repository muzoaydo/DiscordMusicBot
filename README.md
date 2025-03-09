# Discord Music Bot

## Setup

1) Install dependencies:

    > I would suggest creating a virtual environment before installing dependencies.

    ```
    pip install -r requirements.txt
    ```

2) Setup your token

    You need to get a token from Discord and set it by using 'DISCORD_TOKEN' environment variable or just simply adding it to the run method at the last line of MusicBot.py.

## Usage

```
python MusicBot.py
```

    -join //Your bot should join your voice channel
    
    -play {youtube_url} // This should play the given song in url.

## Issues

1) I tried hosting this on an Azure Web Service to have it available all the time but i couldn't pass the Youtube's bot protection. Feel free to contribute on this matter or any other suggestions.