This is an example `systemd` service and Python program for automatically
copying `.FIT` files from a Garmin smartwatch, then drawing the recorded GPS
tracks over corresponding map tile from OpenStreetMap.

In addition to some miscellaneous Python libraries (see `requirements.txt`),
this program also uses the official [Garmin FIT SDK for Python] to interact with the `.FIT`
files¹.

[Garmin FIT SDK for Python]: https://pypi.org/project/garmin-fit-sdk/

**NOTE**: This configuration assumes that you have exactly one Garmin
smartwatch device, that it is mounted to the same location every time, and
that `systemd` is responsible for mounts on the system. It also assumes the
presence of Python 3.9 or higher and the dependencies listed in
`requirements.txt`.

¹ I have made assumptions about what's in the file based on my own personal
needs, you may find that you need more sophisticated processing. I recommend
looking through the [Garmin examples] for deeper insight into the `FIT` format

[Garmin examples]: https://developer.garmin.com/fit/example-projects/

## Usage

To use this service for your own system/device:

* rename `path-to-GARMIN.mount.d` to correpond to the path your device is
  mounted on your own system (for me, this was `/media/$USER/GARMIN`),
  replacing slashes with hyphens (keep the `.mount.d` part).

* Edit `garmin-sync.service` and `garmin_sync.py` filling in the `TODO`s with
  the necessary details.

* Copy the renamed `.mount.d` directory to `/etc/systemd/system/`, and install
  the edited `garmin-sync.service`

You might also need to "prime the pump" and give the service its first start
manually. I dunno, `systemd` is a confusing labyrinth.

## Example output

![Map of the central Boston metropolitan area, with GPS traces overlaid](example_out.png)

