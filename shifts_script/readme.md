# ShiftOrganizer (Shifter) script

This is built with Selenium (Chrome headless mode), Tkinter, Google-Calendar API.

### Can only work with your own google credentials file!

This script connects to [ShiftOrganizer](https://www.shiftorganizer.com/) and retrieves employees Shifts for current week.
User can choose between getting current week shifts or next week shifts, after retrieving the data it automatically connects to your google calendar
(after authentication) and writes shifts. It avoids re-entering same shifts twice.


