from django.template import Library

register = Library()

@register.filter
def photo_url(photo):
    """ Given a 'photo' dict from the Flickr API, return the URL of the image file. """
    return "https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_o.jpg".format(**photo)
