# Floto Flame

A web application for displaying photos from Flickr as a photo frame.  It is intended to be run on a Raspberry Pi, but is not platform-specifc and could be used on almost any computer.

This application includes 2 pages:

* A web page which displays the photos - this is intended to be displayed on your TV/monitor in full-screen.
* A web page which allows you to control the display page (e.g. skip forward/back, etc) - this is intended to be accessed from other devices (e.g. your phone/tablet/laptop) to control the display.

The application also includes a proxy for serving the images.  This allows your computer (web server) to have a local cache of (some of) the images in order to reduce the bandwidth usage.

## Requirements

* Python 2.7.

