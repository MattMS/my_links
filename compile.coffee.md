# Compile links

Compile the link files into a web page.

	path = require 'path'


	get_title_from_file_path = (full_path, base_path)->
		rel_path = path.relative base_path, full_path
	
		p = path.parse rel_path

		rel_path_no_ext = [p.dir, p.name].join path.sep
	
		rel_path_no_ext.replace path.sep, ' '
