import os
htmls = [
    '<div id="links">',
]
for root, dirs, paths in os.walk(os.path.join(os.path.dirname(__file__), 'gallery')):
    for path in paths:
        if 'web' not in path and 'thumb' not in path and path.endswith('.jpg'):
            htmls.append('  <a href="/{}/{}" title="{}">'
                              '<img src="/{}/{}" alt="{}" height="80" />'
                            '</a>'.format(
                                root,
                                path.replace('.', '.web.'),
                                path,
                                root,
                                path.replace('.', '.thumb.'),
                                path
                            ))
htmls.append('</div>')

print '\n'.join(htmls)
                        
