CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {'default':
    {
        'toolbar': 'None'
        , 'height': '100%'
        , 'width': '100%'
    },
    'extraPlugins': ','.join([
        'uploadimage',  # the upload image feature
        # your extra plugins here
        'div',
        'autolink',
        'autoembed',
        'embedsemantic',
        'autogrow',
        # 'devtools',
        'widget',
        'lineutils',
        'clipboard',
        'dialog',
        'dialogui',
        'elementspath',
        'youtube'
    ]),
}