import os

#
# Dynamically calculate proper upload path for screenshots
#
# TODO: at some point need to just have a separate table for screenshots
#
def get_screenshot_upload_path(instance, filename, field_number):
    name, ext = os.path.splitext(filename)

    return os.path.join(
        'levels/screenshots/{}_{}{}'.format(instance.id, field_number, ext)
    )


def get_screenshot_1_upload_path(instance, filename):
    return get_screenshot_upload_path(instance, filename, 1)


def get_screenshot_2_upload_path(instance, filename):
    return get_screenshot_upload_path(instance, filename, 2)
