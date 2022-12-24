# osu! time tracker
### Tracks the amount of time spent playing the actual game.
osu! time tracker is a tool that allows you to track the amount of time you spend playing the popular rhythm game osu!. It utilizes the osu! API to retrieve information about your recent plays and the beatmaps you played.

## Summary
The program runs in an infinite loop, checking for new plays every 2 seconds. If a new play is detected, it retrieves the beatmap information and calculates the time spent playing. If the play was a full completion of the beatmap, it adds the total length of the beatmap to the total time spent playing. If the play was a failure, it parses the beatmap file to find the amount of time spent on the beatmap.

## Usage
1. Obtain an osu! API key from `https://osu.ppy.sh/p/api/`.
2. Rename the `sample.config.py` file to `config.py` and replace the placeholders in the file with your osu! API key, osu! username, and desired osu! game mode.
3. Install the required packages from the `requirements.txt` file using `pip install -r requirements.txt`.
4. Run the `main.py` file to start the time tracker.
    ```
    python main.py
    ```